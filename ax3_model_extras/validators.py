import magic
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _


class FileSizeValidator(BaseValidator):
    """Validate a file size. Size must be given in KB.
    """
    message = _('The weight of the file must be less than the maximum allowed size')
    code = 'file_size'

    def compare(self, a, b):
        return a.size > 1024 * b


class ImageDimensionValidator(BaseValidator):
    """Validate an image dimensions. Should receive a tuple like (width, height).
    """
    message = _('The image must have the specified dimensions')
    code = 'file_dimension'

    def compare(self, a, b):
        width, height = b
        if width == 0:
            return a.height != height

        if height == 0:
            return a.width != width

        return a.width != width or a.height != height


class ImageMinDimensionValidator(BaseValidator):
    """Validate an image dimensions. Should receive a tuple like (width, height).
    """
    message = _('The image must have at least the specified dimensions')
    code = 'file_dimension'

    def compare(self, a, b):
        width, height = b
        if width == 0:
            return a.height < height

        if height == 0:
            return a.width < width

        return a.width < width or a.height < height


class MimetypeValidator(BaseValidator):
    """
    Validate a file mimetype.
    """
    message = _('The document does not have the correct format')
    code = 'file_mimetype'

    def compare(self, a, b):
        try:
            mime = magic.from_buffer(a.read(), mime=True)
            return mime not in b
        except AttributeError:
            return True
