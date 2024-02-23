import logging
from pathlib import Path

import frontmatter
from django.conf import settings
from django.utils.text import slugify
from zoneinfo import ZoneInfo

from blog.models import Post

logger = logging.getLogger(__name__)

TIME_ZONE = ZoneInfo(settings.TIME_ZONE)


def import_post(path: Path) -> tuple[Post, bool]:
    slug = slugify(path.stem[11:])
    with path.open() as f:
        post = frontmatter.load(f)
        title = post["title"]
        categories = post["categories"]
        date = post["date"]
        content = post.content

    # Try setting timezone to west coast if not supplied
    if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
        date = date.replace(tzinfo=TIME_ZONE)

    post, created = Post.objects.update_or_create(
        slug=slug,
        defaults={
            "title": title,
            "categories": categories,
            "date": date,
            "content": content,
        },
    )
    return post, created
