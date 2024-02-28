from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image, ImageOps


class PdpImage(models.Model):
    image = models.ImageField(upload_to="images/")
    thumb = models.ImageField(upload_to="images/thumb/", blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, default="")
    private = models.BooleanField(blank=True, default=True)
    hidden = models.BooleanField(blank=True, default=False)
    date = models.DateTimeField(auto_now_add=True)

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
                "",
                image_file.tell(),
                "",
            ),
            save=False,
        )

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        return super().save(*args, **kwargs)
