---
title: Essential Django Apps for Every Project
date: 2020-03-22T15:17:18-07:00
categories:
    - code
    - django
    - python
---


Django projects have the ability to install [apps](https://djangopackages.org),
which are analogous to plugins in other frameworks.

Some of these apps provide simple functionality:
[django-gravatar](https://github.com/twaddington/django-gravatar) installs a
template tag for displaying a user's gravatar in a template. Other apps are
large, like [Mezzanine](https://github.com/stephenmcd/mezzanine) which provides an
entire CMS framework to your project.

No matter what you are building, you should consider the following apps. I use
them in almost all of my projects.

<!--more-->

## 1. Django Extensions
[django-extensions](https://github.com/django-extensions/django-extensions) is a
collection of custom extensions for Django, most in the form of extra management
commands. Importantly by installing django-extensions you incur *no functional
changes* so it should be safe to add to almost any project. Here
are some of it's best features:

`./manage.py shell_plus`: Like the reugular `shell` management command, but uses
[ipython](https://ipython.org) instead of the standard python shell. So much more
powerful and easy to use. Essential.

`./manage.py show_urls`: Display the full list of URL routes. Honestly I'm surprised
Django doesn't have a built in command for this, frameworks like Ruby on Rails
have had it for years in the form of `rails routes`.

`./manage.py runserver_plus`: Launches a development server using
[Werkzeug](https://palletsprojects.com/p/werkzeug/) instead of the built in one.
Werkzeug has some very cool features, like the ability to interactively debug
stack traces directly in the browser.

`./manage.py generate_secret_key`: Does what it says.

These are just a few of the many features django-extensions brings to your
project. Check out the full
[documentation](https://django-extensions.readthedocs.io/en/latest/index.html) for
more.


## 2. Django Filter
[django-filter](https://github.com/carltongibson/django-filter) allows you to
declaratively add dynamic QuerySet filtering from URL parameters. If you want your
users to be able to order, search or filter results on a page, Django Filter is
going to be a huge help. You write Filter classes which define how objects can be
filtered then add them to your views where they will automatically modify your
queryset for you. They even generate their own forms that you can use if you want.

This might sound a little confusing, so let's use an example. Suppose you have a
`Widget` model defined in your project:

```python
class Widget(models.Model):
    price = models.IntegerField()
    description = models.CharField(max_length=2000)
    listed = models.DateTimeField()
```

You have a view where you list these widgets:

```python
class WidgetList(ListView):
    model = Widget
```

And now you want users on that page to be able to sort by price, search by
description, or view all widgets newer than a certain date. You would write a
filter that looks like this:

```python
class WidgetFilter(fitlers.FilterSet):
    order = filters.OrderingFilter(fields=['price'])
    description = filters.CharFilter()
    newer_than = filters.DateTimeFilter(field_name='listed', lookup_expr='gt')
```

Now edit your view to take advantage of your filter:

```python
class WidgetList(FilterView):
    model = Widget
    filterset_class = WidgetFilter
```

If you want, you can now use the generated form in your template:

```html
<p>Filter results:</p>
{{ filter.form.as_p }}
```

Regardless, if your view is passed url parameters like this:

`http://localhost:8080/widgets/?order=-price&newer_than=2019-03-01&description=foo`


The queryset will be filtered accordingly and your user will see the results they
expect.

This is just a taste of what you can do with Django Filter. See the full
[documentation](https://django-filter.readthedocs.io/en/master/index.html) for
more features.

## 3. Django AllAuth

Not every project requires user registration and social authentication
capabilities, but many do.
[django-allauth](https://www.intenct.nl/projects/django-allauth/) is an extremely
comprehensive package that provides a project with the functions that most users
would expect:

* User sign up flow, including using OAuth providers like Google or Facebook
* Login/Logout
* Email confirmation
* Forgotten password resets
* "Remember me" session control

This is not stuff most of us want to be hand rolling in our projects. Thankfully
Django AllAuth exists and is high quality so we don't have to.


## Notable mentions

[django-rest-framework](https://www.django-rest-framework.org) If you're writing
an API, look no further than Rest Framework.

[django-storages](https://github.com/jschneier/django-storages) For projects that
need to store static files and media on cloud providers like Amazon S3.
Django Storages makes it easy.


