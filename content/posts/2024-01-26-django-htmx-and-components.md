---
title: The Power of Django, HTMX and django-components
date: 2024-01-26T14:22:28-08:00
categories:
    - code
    - django
    - python
---

In this post, I'm going to explore using Django, [HTMX](https://htmx.org/),
[django-components](https://github.com/EmilStenstrom/django-components)
and a slick project layout to build the best todo app you've ever seen that doesn't require React.

<!--more-->

HTMX seems to be having a moment and not just because the X account is a [top-tier
meme factory](https://twitter.com/htmx_org).
It seems to fill a nice somewhere between full luddite server side
rendering and the insanity of whatever is currently going on in the frontend land
(it's Next.js right? Or are we already on to the next... js? 😮‍💨)

Django seems like a perfectly fine framework to use with HTMX and there are plenty
of tutorials out there already on this subject. Enter
[django-components](https://github.com/EmilStenstrom/django-components), a neat
little library I was recently turned on to that promises to deliver some of
the nice parts of modern web dev: isolated, re-usable UI components, but for
Django.

The source code for this demo is located in the [Github repo](https://github.com/Fingel/django-todo-htmx-components).

One last thing to note: I'm using a simplified django project layout which is ideal for little demo purposes like this. No need to create an app when you know
there will only be one. The project layout looks like this:

```
../dj_super_todo/
├── asgi.py
├── db.sqlite3
├── dj_super_todo
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── settings.py
├── urls.py
└── wsgi.py
```

First create the simplest TODO model possible:

```python
# models.py
from django.db import models


class Todo(models.Model):
    done = models.BooleanField(blank=True, default=False)
    content = models.CharField(max_length=500)
```

Create the migrations and seed the database with a few TODOs using the normal
Django methods.

```text
./manage.py makemigrations
./manage.py migrate
./manage.py shell
>>> Todo.objects.create(content="Get better at speaking to my dog.")
<Todo: Todo object (1)>
>>> Todo.objects.create(content="Get up, get up, and get down.")
<Todo: Todo object (2)>
```

Next install django-components and follow the
[installation instructions.](https://github.com/EmilStenstrom/django-components#installation)

Now create the simplest todo component possible:

The template: `components/todo/todo.html`

```html
<div class="todo" id="todo-{{ todo.id }}">
    {{ todo.content }}
    <button>Done</button>
</div>
```

The CSS: `components/todo/todo.css`

```css
.todo {
    width: 300px;
    background: skyblue;
    border: 1px solid;
    margin: 2px 0px;
    padding: 2px;
}
```

And register the component in `components/todo/todo.py`

```python
from django_components import component


@component.register("todo")
class Todo(component.Component):
    template_name = "todo/todo.html"

    def get_context_data(self, todo):
        return {"todo": todo}

    class Media:
        css = "todo/todo.css"
```

Now that the todo component is defined we can use it in a template that lists all todos. Add `BASE_DIR / "templates"` to `settings.TEMPLATES.DIRS`
so we can add `templates/index.html` that lists our todos:

```html
<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Best TODO app</title>
        {% component_css_dependencies %}
        <script
            src="https://unpkg.com/htmx.org@1.9.10"
            integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5xLSi8nO7UC"
            crossorigin="anonymous"
        ></script>
    </head>
    <body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
        <div id="todos">
            {% for todo in todos %} {% component "todo" todo=todo %} {% endfor
            %}
        </div>
        {% component_js_dependencies %}
    </body>
</html>
```

Notice the for loop which uses our `todo` component and passes in the single todo object.

In `views.py`, we define a very simple view that renders this template:

```python
def index(request):
    todos = Todo.objects.all()
    return render(request, "index.html", {"todos": todos})
```

And add this view to `urls.py`:

```python
urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
]
```

Now upon running and visiting our new django app this should appear:

[![Image](https://pedaldp.s3-us-west-2.amazonaws.com/images/2024-01-26-django-htmx-and-components/thumb-todos.png)](https://pedaldp.s3-us-west-2.amazonaws.com/images/2024-01-26-django-htmx-and-components/todos.png)

Nice! Already we begin to see the power of django-components. But a todo app isn't
very useful if you can't add new ones on which you can perpetually procrastinate.

Components defined with django-components have an interesting feature in that
they inherit from Django's `View` class. Which means they can respond to HTTP
requests. Add a `post` method to the todo component which creates a new Todo
object. It then returns itself as rendered HTML in the response which turns
out to be perfect for consumption with HTMX as demonstrated further on.

Also a `delete` method is added.

```python
from django.http import HttpResponse
from django_components import component

from dj_super_todo.models import Todo


@component.register("todo")
class TodoComponent(component.Component):
    template_name = "todo/todo.html"

    def get_context_data(self, todo):
        return {"todo": todo}

    def post(self, request, *args, **kwargs):
        todo = Todo.objects.create(content=request.POST["content"])
        return self.render_to_response({"todo": todo})

    def delete(self, request, pk, *args, **kwargs):
        Todo.objects.get(pk=pk).delete()
        return HttpResponse()

    class Media:
        css = "todo/todo.css"
```

Edit `urls.py` to make routes for these new views. As a `Component` is a
subclass of a Django `View` it is possible to use their `as_view()` functions:

```python
from django.contrib import admin
from django.urls import path

from components.todo.todo import TodoComponent
from dj_super_todo.views import index

urlpatterns = [
    path("components/todo", TodoComponent.as_view(), name="todos"),
    path("components/todo/<int:pk>/", TodoComponent.as_view(), name="todo"),
    path("", index, name="index"),
    path("admin/", admin.site.urls),
]
```

Finally modify both `index.html` and `todo.html` with some HTMX to
create new Todo and delete them, respectively.

```html
<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Best TODO app</title>
        {% component_css_dependencies %}
        <script
            src="https://unpkg.com/htmx.org@1.9.10"
            integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5xLSi8nO7UC"
            crossorigin="anonymous"
        ></script>
    </head>
    <body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
        <div id="todos">
            {% for todo in todos %} {% component "todo" todo=todo %} {% endfor
            %}
        </div>
        <form
            hx-post="{% url 'todos' %}"
            hx-swap="beforeend"
            hx-target="#todos"
        >
            {% csrf_token %}
            <input type="text" name="content" />
            <button type="submit">Add Todo</button>
        </form>
        {% component_js_dependencies %}
    </body>
</html>
```

Notice the form. The `hx-post` attribute points to our view that calls the `post`
method on our Todo Component. `hx-target` tells HTMX to place the response
content in the `#todos` div, and `htx-swap=beforeend` instructs HTMX to put the
content after the last child element of the target. This adds another Todo to the
list without a page refresh.

In `todo.html` we add some HTMX to the individual component to call the delete
view:

```html
<div class="todo" id="todo-{{ todo.id }}">
    {{ todo.content }}
    <button
        hx-delete="{% url 'todo' pk=todo.id %}"
        hx-target="#todo-{{todo.id}}"
        hx-swap="outerHTML"
    >
        Done
    </button>
</div>
```

Similar to the markup for post, `hx-delete` attribute points to the delete
view, `hx-target` defines which element to replace, and `hx-swap="outerHTML`
tells HTMX to replace the entire element with the response, which is nothing.

That's it! We now have a TODO app that feels like something written with a
traditional JS framework, but in fact we didn't have to write any Javascript
at all (though we could have if we wanted). Coupled with Django-components and their ability to act as views, we have a nice model for isolated and re-usable
components that feels quite elegant.

To view the source code as a complete project, check out the [Github repo](https://github.com/Fingel/django-todo-htmx-components).
