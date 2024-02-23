from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from watchfiles import watch

from blog.build import import_post


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        watch_dir = settings.CONTENT_DIR / "posts"
        self.stdout.write(f"Watching {watch_dir} for changes.")
        try:
            for changes in watch(watch_dir):
                for change in changes:
                    _, p = change
                    path = Path(p)
                    self.stdout.write(f"Reloading {path}")
                    import_post(path)
        except KeyboardInterrupt:
            self.stdout.write("Exiting...")
