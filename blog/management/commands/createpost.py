from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from frontmatter import Post, dump


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("title")
        parser.add_argument("categories", nargs="+")

    def handle(self, *args, **options):
        title = options["title"]
        date = timezone.localtime(timezone.now())

        post = Post(content="Insert words here.")
        post["title"] = title
        post["date"] = date
        post["categories"] = options["categories"]

        date_segment = date.strftime("%Y-%m-%d")
        slug = slugify(title)
        filename = f"{date_segment}-{slug}.md"
        path = settings.CONTENT_DIR / "posts" / filename
        with open(path, "wb") as f:
            dump(post, f)

        self.stdout.write(f"New post created at {path}")
