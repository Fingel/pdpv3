from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.filter(is_safe=True)
def convert_markdown(value):
    extensions = [
        "markdown.extensions.smarty",
        "markdown.extensions.tables",
        "fenced_code",
        "codehilite",
    ]
    return mark_safe(markdown(value, extensions=extensions))
