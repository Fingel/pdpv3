from django.contrib.syndication.views import Feed
from django.utils import timezone

from blog.models import Post


class LatestPostsFeed(Feed):
    title = "Pedal Driven Programming"
    link = "/post/"
    description = "A personal website about bikes and code."

    def items(self):
        return Post.objects.filter(date__lt=timezone.now())[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt
