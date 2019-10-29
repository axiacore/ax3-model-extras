from io import BytesIO
import os.path
import subprocess

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import ImageField

from PIL import Image
from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError


class OptimizedImageField(ImageField):
    def __init__(self, *args, **kwargs):
        """
        `optimized_image_output_size` must be a tuple and `optimized_image_resize_method` can be
        'crop', 'cover', 'contain', 'width', 'height' or 'thumbnail'.
        """
        self.optimized_image_output_size = kwargs.pop('optimized_image_output_size', None)
        self.optimized_image_resize_method = kwargs.pop('optimized_image_resize_method', 'cover')

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        # we just remove the arguments from the kwargs dict.
        kwargs.pop('optimized_image_output_size', None)
        kwargs.pop('optimized_image_resize_method', None)

        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)

        webp_path = f'{os.path.splitext(file.path)[0]}.webp'
        if not file.storage.exists(webp_path):
            # https://developers.google.com/speed/webp/docs/cwebp
            if file.name.lower().endswith('.png'):
                args = ['cwebp', '-quiet', '-lossless', file.path, '-o', '-']
            else:
                args = ['cwebp', '-quiet', file.path, '-o', '-']

            try:
                bytes_output = subprocess.check_output(args, timeout=30)
                file.storage.save(webp_path, ContentFile(bytes_output))
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                pass

        return file

    def save_form_data(self, instance, data):
        updating_image = True if data and getattr(instance, self.name) != data else False
        if updating_image:
            try:
                data = self.optimize_image(
                    image_data=data,
                    output_size=self.optimized_image_output_size,
                    resize_method=self.optimized_image_resize_method
                )
            except ImageSizeError:
                raise ValidationError({self.name: ['Imagen demasiado pequeña para ser escalada']})

        super().save_form_data(instance, data)

    def optimize_image(self, image_data, output_size, resize_method):
        """Optimize an image that has not been saved to a file."""
        image = Image.open(image_data)

        if image.format not in ('JPEG', 'PNG'):
            raise ValidationError({self.name: ['Imagen debe ser tipo JPEG o PNG']})

        # If output_size is set, resize the image with the selected resize_method.
        if output_size:
            output_image = resizeimage.resize(resize_method, image, output_size)
        else:
            output_image = image

        # If the file extension is JPEG, convert the output_image to RGB
        if image.format == 'JPEG':
            output_image = output_image.convert('RGB')

        bytes_io = BytesIO()
        output_image.save(bytes_io, format=image.format, optimize=True)

        image_data.seek(0)
        image_data.file.write(bytes_io.getvalue())
        image_data.file.truncate()

        return image_data
