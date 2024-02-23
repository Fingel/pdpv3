---
categories:
- code
date: 2015-10-08 20:59:14
title: Sane Django Development with Docker
---

Recently I started a new Django project, and this time
I decided to go all in on Docker. No virtualenvs,
no local databases - containers all the way.

There are about a million and ten articles about how to
dockerize webapps by now. However, none of them seem to
address one simple fact: we don't simply want to
dockerize our applications, we want to _develop_ them too!


[sane-django-docker](https://github.com/Fingel/sane-django-docker.git) 
contains a sample django project `webapp` as well as the necessary
config files to run both a development and production server.

<!--more-->

Checkout and Go®
----------------

One of my goals was to make the codebase **development**
first. One should be able to checkout the codebase and run at most two or three commands
to have a real development environment set up. This
means we should have a live-reloading Django development
server, debug mode on, and a postgresql database. I also can't stand logic
in my `settings.py` files, so it is left as vanilla as possible. It
will import a `local_settings.py` file at the end, but besides that it is 100%
constants. No `os.getenv()` to be found.

To start the development server simply run:

    docker-compose up

Django will complain about the postgres database not existing so we'll create one:

    docker exec sanedjangodocker_db_1 createdb -Upostgres webapp

Sweet Jane! We now have a Django development server running at `http://localhost:8000` along with a postgresql database! Make a code
change and watch it reload. This is how code was meant to be written.

So what's the secret sauce? A super simple [Dockerfile](https://github.com/Fingel/sane-django-docker/blob/master/Dockerfile) and an equally simple [docker-compose.yml](https://github.com/Fingel/sane-django-docker/blob/master/docker-compose.yml) file.


Deployment ain't that much harder
---------------------------------

So getitng a dev environment up and running is all well and good,
but we are going to have to deploy our code at some point. Deployment takes a few additional steps, but then again deployment probably should.

Let's take a look at what we have:

    .
    ├── deploy
    │   ├── docker-compose.yml
    │   ├── local_settings.py
    │   ├── nginx-app.conf
    │   ├── supervisor-app.conf
    │   ├── uwsgi.ini
    │   └── uwsgi_params
    ├── docker-compose.yml
    ├── Dockerfile
    ├── Dockerfile.prod
    ├── manage.py
    ├── README.md
    ├── requirements.txt
    └── webapp
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py


The `deploy/` directory contains all our server configuration files.
The directory also includes our `local_settings.py` which contains our
production config. It is included in `.gitignore` and should **not** be
included in source control!

`Dockerfile.prod` is our production dockerfile. It is based on Python:3.5,
installs nginx, uwsgi and supervisord, copies our config files and finally
runs `manage.py collectstatic`.

Let's build an image from it:

    docker build -f Dockerfile.prod -t webapp:latest .

That's it! our production image is ready to go. To test it out locally first,
we can run it:


    cd deploy/ && docker-compose up

This should start our project in production mode, using the image we just built. Again, we need to initially create the database,
and we should probably run migrations too:

    docker exec sanedjangodocker_db_1 createdb -Upostgres webapp
    docker exec sanedjangodocker_web_1 python3 manage.py migrate

Navigate to `localhost:8700` and see your production-ready application
being served!


Where to go from here
---------------------

There are probably a few things you want to tweak for a real project such as
the postgresql data volume in `deploy/docker-compose.yml`, and
your `ALLOWED_HOSTS` setting in `local_settings.py`.

Of course, the nginx, uwsgi and supervisord config files are pretty basic, and
probably should be scrutinized before a real life deploy.


Conclusions
-----------

All in all, I've found this to be a pretty frictionless workflow. The one
annoyance I have is that both dockerfiles have to be in the top level
directory, due to how Docker sends the build context to the server.
Besides that there isn't much to complain about - I'll probably use this as
a base for my future projects.