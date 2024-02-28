from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from blog.models import Post


class BlogSiteMap(Sitemap):
    def items(self):
        return Post.objects.filter(date__lt=timezone.now())

    def lastmod(self, obj):
        return obj.date


class StaticViewSitemap(Sitemap):
    def items(self):
        return ["index", "projects", "talks", "photos:index"]

    def location(self, item):
        return reverse(item)


sitemaps = {"blog": BlogSiteMap, "static": StaticViewSitemap}
