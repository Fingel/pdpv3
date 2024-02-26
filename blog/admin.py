from django.contrib import admin

from blog.models import Comment, Post


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ["commenter", "content", "post", "date"]
    search_fields = ["commenter", "content"]


class InlineCommentAdmin(admin.StackedInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ["slug", "title", "date"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [InlineCommentAdmin]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
