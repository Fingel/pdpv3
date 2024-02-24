from django import forms
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.dates import (
    ArchiveIndexView,
    MonthArchiveView,
    YearArchiveView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.models import Comment, Post


class BlogIndex(ArchiveIndexView):
    model = Post
    date_field = "date"
    paginate_by = 10
    template_name = "blog/list.html"


class YearArchive(YearArchiveView):
    model = Post
    date_field = "date"
    paginate_by = 20
    make_object_list = True
    template_name = "blog/list_short.html"


class MonthArchive(MonthArchiveView):
    model = Post
    date_field = "date"
    month_format = "%m"
    paginate_by = 20
    make_object_list = True
    template_name = "blog/list_short.html"


class CommentForm(forms.Form):
    commenter = forms.CharField(required=False, label="Name (optional)")
    content = forms.CharField(label="Comment", widget=forms.Textarea(attrs={"rows": 5}))
    post = forms.CharField(widget=forms.HiddenInput)
    # honeypot email field
    comment_email = forms.EmailField(required=False, label="Email (required)")
    # Math challenge
    challenge = forms.IntegerField(label="What is four plus two?")

    def clean_comment_email(self):
        email = self.cleaned_data["comment_email"]
        if email:
            raise forms.ValidationError("This is a honeypot")
        return email

    def clean_challenge(self):
        answer = self.cleaned_data["challenge"]
        if answer != 6:
            raise forms.ValidationError("This is a bot")
        return answer


class BlogPost(DetailView):
    model = Post
    template_name = "blog/post.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        comment_form = CommentForm(initial={"post": self.get_object().pk})
        context["comment_form"] = comment_form
        return context


class CommentView(View):
    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk=form.cleaned_data["post"])
            comment = Comment.objects.create(
                post=post,
                commenter=form.cleaned_data["commenter"],
                content=form.cleaned_data["content"],
            )
        else:
            # Make it look like a comment was posted but don't save it.
            comment = Comment(
                post=Post.objects.get(pk=request.POST["post"]),
                commenter=request.POST["commenter"],
                content=request.POST["content"],
            )
        return render(request, "blog/_comment.html", {"comment": comment})


class CategoryIndex(ListView):
    model = Post
    paginate_by = 20
    template_name = "blog/list_short.html"

    def get_queryset(self):
        category = self.kwargs["category"]
        return super().get_queryset().filter(categories__contains=[category])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["category"] = self.kwargs["category"]
        return context
