from django.views.generic.list import ListView

from photos.models import PdpImage


class PhotoList(ListView):
    model = PdpImage
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset().exclude(hidden=True)
        if not self.request.user.is_authenticated:
            qs = qs.exclude(private=True)
        return qs

    def get_template_names(self, *args, **kwargs):
        if self.request.headers.get("HX-Request"):
            return ["photos/gallery_row.html"]
        else:
            return ["photos/gallery.html"]
