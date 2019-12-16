import os.path
import subprocess

from django.core.files.base import ContentFile

from PIL import Image


def generate_webp(image_field):
    """Generates a webp file. Supports PNG, JPEG and GIF files. If filepath is
    `uploads/home/sunset.png` the generated file will be `uploads/home/sunset.webp`.
    """
    try:
        img = Image.open(image_field)
        if img.format == 'PNG':
            cmd_args = ['cwebp', '-quiet', '-lossless', image_field.path, '-o', '-']
        elif img.format == 'JPEG':
            cmd_args = ['cwebp', '-quiet', image_field.path, '-o', '-', '-q', '85']
        elif img.format == 'GIF':
            cmd_args = ['gif2webp', '-quiet', image_field.path, '-mixed', '-o', '-']
        else:
            return

        webp_path = f'{os.path.splitext(image_field.path)[0]}.webp'
        bytes_output = subprocess.check_output(cmd_args, timeout=30)
        image_field.storage.save(webp_path, ContentFile(bytes_output))
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
