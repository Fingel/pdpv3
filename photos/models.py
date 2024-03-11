import secrets
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image, ImageOps


def image_upload_salt(instance, filename):
    return f"images/{instance.image_salt}-{filename}"


def thumb_upload_salt(instance, filename):
    return f"images/thumb/{instance.image_salt}-{filename}"


class PdpImage(models.Model):
    image = models.ImageField(upload_to=image_upload_salt)
    thumb = models.ImageField(upload_to=thumb_upload_salt, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, default="")
    private = models.BooleanField(blank=True, default=True)
    hidden = models.BooleanField(blank=True, default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_salt = secrets.token_urlsafe(8)

    def __str__(self):
        return self.image.name

    def create_thumbnail(self):
        if not self.image:
            return

        image = Image.open(self.image)
        ImageOps.exif_transpose(image, in_place=True)
        image.thumbnail((800, 800))
        image_file = BytesIO()
        image.save(image_file, image.format)
        self.thumb.save(
            self.image.name,
            InMemoryUploadedFile(
                image_file,
                None,
                None,
                f"image/{image.format}",
                image_file.tell(),
                None,
            ),
            save=False,
        )

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        return super().save(*args, **kwargs)
