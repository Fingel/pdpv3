---
categories:
- code
date: 2016-11-17 20:53:42
title: Preserve GET parameters using django-bootstrap3 pagination
---

This one got me for a bit. If you are using [django-bootstrap3](https://github.com/dyve/django-bootstrap3) and
also want to use it's handy [bootstrap_pagination](https://django-bootstrap3.readthedocs.io/en/latest/templatetags.html#bootstrap-pagination) template tag for generating pagination links, you may be in for an
unplesant surprise if your view uses any GET parameters. While the [django-bootstrap-pagination](https://github.com/jmcclell/django-bootstrap-pagination) project handles this by default, django-bootstrap3 will not persist GET paramters between pages.

The key to using the `bootstrap_pagination` tag is the `extra` argument, which takes a string and appends it to each page. If you
have the `request_context` context processor installed, you can pass in this string using the [QueryDict urlencode()](https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.QueryDict.urlencode) method. For example:

`{% bootstrap_pagination page_obj extra=request.GET.urlencode %}`

Voila. Pagination in django with bootstrap working as it should.

<!--more-->
