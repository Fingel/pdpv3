from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ["slug", "title", "date"]
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(Post, PostAdmin)
