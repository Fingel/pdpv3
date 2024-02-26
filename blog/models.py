from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils import timezone


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

    @property
    def excerpt(self) -> str:
        splitter = "<!--more-->"
        if splitter in self.content:
            return self.content.split("<!--more-->")[0]
        else:
            return self.content.split("\n")[0]

    def __str__(self):
        return self.slug


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, blank=True)
    commenter = models.CharField(max_length=200, blank=True, default="")
    content = models.TextField()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.commenter} on {self.post}"
