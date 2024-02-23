from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ["slug", "title", "date"]


admin.site.register(Post, PostAdmin)
