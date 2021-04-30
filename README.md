# AX3 Model Extras

## Installation
AX3 Model Extras is easy to install from the PyPI package:

```bash
$ pip install ax3-model-extras
```

To enable ax3_model_extras in your project you need to add it to INSTALLED_APPS in your projects settings.py file:

```python
INSTALLED_APPS = (
    ...
    'ax3_model_extras',
    ...
)
```

## Validate image size

If you want to validate the dimension and file size for images:

```python
from ax3_model_extras.validators import FileSizeValidator, ImageDimensionValidator


class Post(models.Model):
    title = models.CharField()

    slug = models.SlugField()

    image = models.ImageField(
        validators=[ImageDimensionValidator([1920, 800]), FileSizeValidator(350)],
        help_text='JPG. 1920x800px. 350kb max.',
    )
```

If you want to validate one dimension, you have to send the other dimension with 0

```python
from ax3_model_extras.validators import FileSizeValidator, ImageDimensionValidator


class Post(models.Model):
    title = models.CharField()

    slug = models.SlugField()

    image = models.ImageField(
        validators=[ImageDimensionValidator([1920, 0]), FileSizeValidator(350)],
        help_text='JPG. width=1920px. 350kb max.',
    )
```



## Improve file storage

If you want to improve the local file storage or use S3 upload:

```python
from ax3_model_extras.storages import get_storage, get_upload_path


class Post(models.Model):
    title = models.CharField()

    slug = models.SlugField()

    image = models.ImageField(
        upload_to=get_upload_path,
        storage=get_storage(),
    )
```


## Optimize images before upload them.

Use as:

```python
from ax3_model_extras.fields import OptimizedImageField


class Post(models.Model):
    title = models.CharField()

    slug = models.SlugField()

    image = OptimizedImageField()

```


If want to set the size of the image using the 'cover' method do:

```python
image = OptimizedImageField(
    optimized_image_output_size=(1920, 800),
)
```


If want to set the size of the image using the 'thumbnail' method do:

```python
image = OptimizedImageField(
    optimized_image_output_size=(1920, 800),
    optimized_image_resize_method='thumbnail',
)
```


If want to restrict the file format do (If not set it supports JPEG, PNG and GIF):

```python
image = OptimizedImageField(
    optimized_image_output_size=(1920, 800),
    optimized_image_resize_method='thumbnail',
    optimized_file_formats=['PNG'],
)
```


If want to specific quality of the image (If not set it default =  75):

```python
image = OptimizedImageField(
    optimized_image_output_size=(1920, 800),
    optimized_image_resize_method='thumbnail',
    optimized_file_formats=['PNG'],
    optimized_image_quality=85.5,
)
```

Resize is done using https://pypi.org/project/python-resize-image/

Made by Axiacore.
