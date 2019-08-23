import os
import uuid

from django.conf import settings
from django.core.files.storage import DefaultStorage
from django.utils.text import slugify


def get_upload_path(instance, filename):
    """Return a path for a remote file storage.
    Allows a file path up to 100 characters.
    """
    name, ext = os.path.splitext(filename)
    path = os.path.join(
        instance._meta.object_name.lower(),
        uuid.uuid4().hex,
        slugify(name),
    )
    return f'{path[:90]}{ext[:10]}'


def get_storage():
    """Get the custom storage for files.
    """
    if getattr(settings, 'AWS_ACCESS_KEY_ID', None):
        from storages.backends.s3boto3 import S3Boto3Storage
        return S3Boto3Storage()

    return DefaultStorage()
