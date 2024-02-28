from django.urls import path

from photos.views import PhotoList

app_name = "photos"
urlpatterns = [
    path("", PhotoList.as_view(), name="index"),
]
