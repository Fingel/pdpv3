---
title: A Humble Makefile
date: 2021-06-24T10:18:39-07:00
categories:
    - code
---

I've been adding [GNU Makefiles](https://www.gnu.org/software/make/) to all my projects recently and it's not because I've suddenly become a C programmer.

<!--more-->

Make was designed to be a build tool to make compiling complex programs with lots of source files easier. It does stuff like provide you with a way to describe dependencies between files and define tasks for compiling your program. It's one of those legendary Unix programs that is still available on every Linux and Mac OS but most probably never use.

But I don't use it for describing long chained build instructions. I just use it so I don't have to remember commands.

I work on a larger set of projects now and they all do the same things, but just slightly different. A great example of this is starting up the dev server.

For Django:

    python3 manage.py runserver

For Flask:

    env FLASK_APP=src/api.py FLASK_ENV=development flask run

Even Docker:

    docker run web -p8080:8080

Instead of trying to remember how to start each project, I've just started writing Makefiles. Now I have something like this for each project

```Makefile
run:
    python3 manage.py runserver

test:
    pyhton3 manage.py test

```

The other projects share the same command names. Now when I want to start a dev server for any project, I just `cd` to the directory and simply `make run`.
