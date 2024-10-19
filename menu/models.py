# menu_app/models.py

import uuid

from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify

from menu.utils import get_s3_client


# Custom User Model with GUID
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


# Menu Model
class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    show_on_catalog = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)

    def generate_logo_presigned_url(self):
        s3_client = get_s3_client()
        menu_id = self.id
        object_name = f"menus/{menu_id}/logo.jpg"

        try:
            # Generate a presigned URL for reading the logo
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': object_name},
                ExpiresIn=3600  # URL expires in 1 hour
            )
            return presigned_url
        except ClientError as e:
            return None

    def clean(self):
        if self.logo:
            if self.logo.size > 5 * 1024 * 1024:
                raise ValidationError("Logo file size should be under 5MB.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CuisineType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DietaryOption(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.OneToOneField(Menu, related_name='detail', on_delete=models.CASCADE)
    operating_hours = models.TextField(blank=True, null=True, max_length=300)
    location = models.TextField(blank=True, null=True, max_length=300)
    cuisine_type = models.ManyToManyField(CuisineType, blank=True)
    dietary_options = models.ManyToManyField(DietaryOption, blank=True)
    delivery_options = models.CharField(
        max_length=20,
        choices=[
            ('pickup', 'Pickup'),
            ('delivery', 'Delivery'),
            ('both', 'Both'),
            ('none', 'None')
        ],
        blank=True,
        null=True,
        default='none'
    )

    def __str__(self):
        return f"Details for {self.menu.name}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    menus = models.ManyToManyField(Menu, blank=True, related_name='categories')

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
                                          ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='menu_items')
    menus = models.ManyToManyField(Menu, blank=True, related_name='menu_items')
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    def generate_access_presigned_url(self):
        s3_client = get_s3_client()

        menu_id = self.menus.first().id
        menu_item_id = self.id
        object_name = f"menus/{menu_id}/menu_items/{menu_item_id}/photo.jpg"

        try:
            # Generate a presigned URL for reading the image
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': object_name},
                ExpiresIn=3600  # URL expires in 1 hour
            )
            return presigned_url
        except ClientError as e:
            return None
