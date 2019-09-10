# AX3 Model Extras

## Validate image size

If you want to validate the dimension and file size for images:

```
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

```
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

```
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

```
from ax3_model_extras.fields import OptimizedImageField


class Post(models.Model):
    title = models.CharField()

    slug = models.SlugField()

    image = OptimizedImageField()

```


If want to set the size of the image using the 'cover' method do:

```
image = OptimizedImageField(
    optimized_image_output_size=(1920, 800),
)
```


If want to set the size of the image using the 'thumbnail' method do:

```
image = OptimizedImageField(
    optimized_image_output_size=(1920, 800),
    optimized_image_resize_method='thumbnail',
)
```

Resize is done using https://pypi.org/project/python-resize-image/

Made by Axiacore.
