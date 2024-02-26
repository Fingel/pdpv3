from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="base/index.html"), name="index"),
    path(
        "projects/",
        TemplateView.as_view(template_name="base/projects.html"),
        name="projects",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="base/contact.html"),
        name="contact",
    ),
]
