from io import BytesIO

from django.db.models import ImageField

from PIL import Image
from resizeimage import resizeimage


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

    def save_form_data(self, instance, data):
        # Are we updating an image?
        updating_image = True if data and getattr(instance, self.name) != data else False

        if updating_image:
            data = self.optimize_image(
                image_data=data,
                output_size=self.optimized_image_output_size,
                resize_method=self.optimized_image_resize_method
            )

        super().save_form_data(instance, data)

    def optimize_image(self, image_data, output_size, resize_method):
        """Optimize an image that has not been saved to a file."""
        image = Image.open(image_data)
        bytes_io = BytesIO()

        # If output_size is set, resize the image with the selected resize_method.
        if output_size:
            output_image = resizeimage.resize(resize_method, image, output_size)
        else:
            output_image = image

        # If the file extension is JPEG, convert the output_image to RGB
        if image.format == 'JPEG':
            output_image = output_image.convert('RGB')

        output_image.save(bytes_io, format=image.format, optimize=True)

        image_data.seek(0)
        image_data.file.write(bytes_io.getvalue())
        image_data.file.truncate()

        return image_data
