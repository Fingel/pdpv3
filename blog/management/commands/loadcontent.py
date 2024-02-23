import pathlib

from django.core.management.base import BaseCommand

from blog.build import import_post


class Command(BaseCommand):
    help = "Load content in the given directory."

    def add_arguments(self, parser):
        parser.add_argument("dir", type=pathlib.Path)

    def handle(self, *args, **options):
        path = options["dir"]
        self.stdout.write(f"Importing content from {path}")
        num_created = 0
        num_updated = 0
        files = [f for f in path.iterdir()]
        for file in files:
            _, created = import_post(file)
            self.stdout.write(".", ending="")
            self.stdout.flush()
            if created:
                num_created += 1
            else:
                num_updated += 1
        self.stdout.write("\n")
        self.stdout.write(f"{num_created} posts created.")
        self.stdout.write(f"{num_updated} posts updated.")
        self.stdout.write("✨✨✨")
