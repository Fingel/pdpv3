from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="base/index.html"), name="index"),
    path(
        "projects/",
        TemplateView.as_view(template_name="base/projects.html"),
        name="projects",
    ),
]
