from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy


def page_not_found(request, *args, **kwargs):
    return render(request, "base/404.html", status=404)


def internal_server_error(request, *args, **kwargs):
    return render(request, "base/500.html", status=500)


class BabyLoginView(LoginView):
    template_name = "base/login.html"
    next_page = reverse_lazy("photos:index")

    def get_initial(self):
        initial = super().get_initial()
        initial["username"] = "babyuser"
        return initial
