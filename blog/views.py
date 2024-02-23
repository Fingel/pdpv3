from django.views.generic.dates import (
    ArchiveIndexView,
    MonthArchiveView,
    YearArchiveView,
)
from django.views.generic.detail import DetailView

from blog.models import Post


class BlogIndex(ArchiveIndexView):
    model = Post
    date_field = "date"
    paginate_by = 20
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
