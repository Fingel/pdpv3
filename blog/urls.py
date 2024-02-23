from django.urls import path

from blog.views import BlogIndex, BlogPost, MonthArchive, YearArchive

app_name = "blog"
urlpatterns = [
    path("post/", BlogIndex.as_view(), name="index"),
    path("<int:year>/", YearArchive.as_view(), name="archive-year"),
    path("<int:year>/<int:month>/", MonthArchive.as_view(), name="archive-month"),
    path("<int:year>/<int:month>/<slug:slug>/", BlogPost.as_view(), name="detail"),
]
