from django.shortcuts import render


def page_not_found(request, *args, **kwargs):
    return render(request, "base/404.html", status=404)


def internal_server_error(request, *args, **kwargs):
    return render(request, "base/500.html", status=500)
