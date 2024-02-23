from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse


class Post(models.Model):
    slug = models.SlugField(primary_key=True, db_index=True, max_length=100)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(db_index=True)
    categories = ArrayField(models.CharField(max_length=50), blank=True)
    content = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-date"]

    def get_absolute_url(self):
        return reverse(
            "blog:detail",
            kwargs={
                "year": self.date.strftime("%Y"),
                "month": self.date.strftime("%m"),
                "slug": self.slug,
            },
        )

    def __str__(self):
        return self.slug
