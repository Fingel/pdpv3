from django.contrib import admin

from blog.models import Comment, Post


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ["commenter", "content", "post", "date"]
    search_fields = ["commenter", "content"]


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ["slug", "title", "date"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
