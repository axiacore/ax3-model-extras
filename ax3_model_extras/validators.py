import magic
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
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
            mime = magic.from_buffer(a.open().read(2048), mime=True)
            return mime not in b
        except AttributeError:
            return True


@deconstructible
class PhoneNumberValidator:
    message = _('Invalid phone number.')
    code = 'invalid_phone_number'

    def __init__(self, iso_code, message=None, code=None):
        self.iso_code = iso_code

        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        try:
            mobile_number = phonenumbers.parse(str(value), self.iso_code)

            if not phonenumbers.is_valid_number(mobile_number):
                raise ValidationError(self.message, code=self.code)

        except phonenumbers.NumberParseException as exc:
            raise ValidationError(str(exc), code=self.code) from exc

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and self.iso_code == other.iso_code
            and self.message == other.message and self.code == other.code
        )
