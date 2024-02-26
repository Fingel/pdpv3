import json
import urllib.request
from datetime import datetime

from django.core.management.base import BaseCommand

from blog.models import Comment, Post


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("url")

    def handle(self, *args, **options):
        with urllib.request.urlopen(options["url"]) as response:
            comment_dump = json.loads(response.read())
        commenters = {}
        for commenter in comment_dump["commenters"]:
            commenters[commenter["commenterHex"]] = {**commenter}

        comments = {}

        def create_comment(comment_hex: str):
            if comments.get(comment_hex):
                return comments[comment_hex]
            for comment in comment_dump["comments"]:
                if comment["markdown"] == "[deleted]":
                    continue
                if comment["commentHex"] == comment_hex:
                    if comment["parentHex"] != "root":
                        parent = create_comment(comment["parentHex"])
                    else:
                        parent = None

                    slug = comment["url"][9:-1]
                    try:
                        post = Post.objects.get(slug=slug)
                    except Post.DoesNotExist:
                        self.stdout.write(f"\n could not find post with slug {slug}")
                        continue
                    if comment["commenterHex"] != "anonymous":
                        commenter_name = commenters[comment["commenterHex"]]["name"]
                    else:
                        commenter_name = "anonymous"
                    comment_obj = Comment.objects.create(
                        post=post,
                        parent=parent,
                        date=datetime.fromisoformat(comment["creationDate"]),
                        commenter=commenter_name,
                        content=comment["markdown"],
                    )
                    comments[comment_hex] = comment_obj
                    return comment_obj

        for comment in comment_dump["comments"]:
            self.stdout.write(".", ending="")
            self.stdout.flush()
            create_comment(comment["commentHex"])
