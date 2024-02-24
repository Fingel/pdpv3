from django.views.generic.dates import (
    ArchiveIndexView,
    MonthArchiveView,
    YearArchiveView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.models import Post


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


class BlogPost(DetailView):
    model = Post
    template_name = "blog/post.html"


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
