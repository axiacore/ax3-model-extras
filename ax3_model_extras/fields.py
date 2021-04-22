from io import BytesIO

from django.core.exceptions import ValidationError
from django.db.models import ImageField
from django.utils.translation import gettext_lazy as _
from PIL import Image
from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError

from .webp import generate_webp


class OptimizedImageField(ImageField):
    def __init__(self, *args, **kwargs):
        """
        `optimized_image_output_size` must be a tuple and `optimized_image_resize_method` can be
        'crop', 'cover', 'contain', 'width', 'height' or 'thumbnail'.
        """
        self.optimized_image_output_size = kwargs.pop('optimized_image_output_size', None)
        self.optimized_image_resize_method = kwargs.pop('optimized_image_resize_method', 'cover')
        self.optimized_file_formats = kwargs.pop('optimized_file_formats', ['JPEG', 'PNG', 'GIF'])
        self.optimized_image_quality = kwargs.pop('optimized_image_quality', 75)

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        # Remove the arguments from the kwargs dict.
        kwargs.pop('optimized_image_output_size', None)
        kwargs.pop('optimized_image_resize_method', None)
        kwargs.pop('optimized_file_formats', None)
        kwargs.pop('optimized_image_quality', None)

        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        image_field = super().pre_save(model_instance, add)

        if image_field:
            generate_webp(image_field=image_field, quality=str(self.optimized_image_quality))

        return image_field

    def save_form_data(self, instance, data):
        updating_image = data and getattr(instance, self.name) != data
        if updating_image:

            if self.optimized_image_quality < 0 or self.optimized_image_quality > 100:
                raise ValidationError({self.name: [_('The allowed quality is from 0 to 100')]})

            try:
                data = self.optimize_image(
                    image_data=data,
                    output_size=self.optimized_image_output_size,
                    resize_method=self.optimized_image_resize_method,
                    quality=self.optimized_image_quality,
                )
            except ImageSizeError:
                raise ValidationError({self.name: [_('Image too small to be scaled')]})
            except OSError:
                raise ValidationError({self.name: [_('The image is invalid or corrupted')]})

        super().save_form_data(instance, data)

    def optimize_image(self, image_data, output_size, resize_method, quality):
        """Optimize an image that has not been saved to a file."""
        img = Image.open(image_data)

        if img.format not in self.optimized_file_formats:
            raise ValidationError({self.name: [_('Image format unsupported')]})

        # GIF files needs strict size validation
        if img.format == 'GIF' and output_size and output_size != (img.width, img.height):
            raise ValidationError({self.name: [_('GIF image size unsupported')]})

        # Check if is a supported format for optimization
        if img.format not in ['JPEG', 'PNG']:
            return image_data

        # If output_size content 0.
        if output_size and output_size[0] == 0:
            output_size = (img.width, output_size[1])
        elif output_size and output_size[1] == 0:
            output_size = (output_size[0], img.height)

        # If output_size is set, resize the image with the selected resize_method.
        if output_size and output_size != (img.width, img.height):
            output_image = resizeimage.resize(resize_method, img, output_size)
        else:
            output_image = img

        # If the file extension is JPEG, convert the output_image to RGB
        if img.format == 'JPEG':
            output_image = output_image.convert('RGB')

        bytes_io = BytesIO()
        output_image.save(bytes_io, format=img.format, optimize=True, quality=quality)

        image_data.seek(0)
        image_data.file.write(bytes_io.getvalue())
        image_data.file.truncate()

        return image_data
