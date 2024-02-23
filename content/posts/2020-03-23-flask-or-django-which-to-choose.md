---
title: Flask or Django? Which to Choose for your Project
date: 2020-03-23T10:38:35-07:00
categories:
    - code
    - django
    - flask
    - python
---

Often I get asked by fellow python developers why I chose Django/Flask for a
particular project (usually by someone who prefers the framework I _didn't_ choose
😉). I think both frameworks are excellent and are well suited for a variety of
use cases.

So how do I decide which to use for a new project? I found a simple heuristic to
get 90% of the way to a final decision, and it's pretty easy to follow:


<!--more-->


Decide what features your project needs:

* User accounts
* An Object Relational Manager (ORM)
* Database Migrations
* User registration/social authentication
* An admin site

Does your project require 2 or more of these features?

If **Yes**  => Choose Django

If **No**   => Choose Flask


Flask is great for small, focused projects. Think microservices, APIs, or very
small websites. But once you have to start hunting down and installing extensions
like [Flask Sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and
[Flask User](https://flask-user.readthedocs.io/en/latest/) you quickly enter a
situation where the "batteries included" approach of Django makes more sense. You
are basically spending time re-implementing stuff that larger frameworks like
Django ship with out the box, and that are very well integrated.

On the other hand, Django can be a huge overkill for some projects. Think of an
API that accepts image uploads and returns thumbnails. You _could_ use Django for
such a task, but the amount of boilerplate and setup required would be ridiculous.
One of the great things about Flask is the fact that an entire webapp can be
[written in a single
file](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application).

Of course like I said this heuristic only gets you 90% of the way. Every project
has unique use cases and design constraints that must be taken into account before
making a large decision like which tech stack to use.
