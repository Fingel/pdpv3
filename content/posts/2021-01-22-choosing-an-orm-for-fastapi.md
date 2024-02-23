---
title: "Choosing the Right ORM for FastAPI" # Title of the blog post.
date: 2021-01-22T14:18:28-08:00 # Date of post creation.
description: "Decide which ORM is right for you and your project." # Description used for search engine.
featured: false # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.

categories:
  - code
  - python
  - FastAPI
# comment: false # Disable comment if false.
---

When developing a large database backed application, using an ORM (Object Relational Manager) can really benefit your project. There are quite a few ORMs for Python, but which work best with FastAPI?

<!--more-->

You must be careful with considering which ORM to use. If your project relies heavily on interacting with a database you will end up writing a lot of code that relies on the ORM.

There are many ORMs that work with Python and they all have their strengths and weaknesses. If you are writing an application with FastAPI, there are constraints that need to be considered - mainly using an ORM that supports Python3 async.

## ORMs Compared

TL;DR: use the following table to help you decide which ORMs might be worth looking in to.

 ORM | Async | Migrations | Multi Database | Easy to Learn| Feature Complete
-----|-------|------------|----------------|--------------|-----------------
[SqlAlchemy](https://www.sqlalchemy.org)|✅|✅|✅|⛔️|✅
[Tortoise](https://tortoise-orm.readthedocs.io)|✅|✅|✅|✅|⛔️
[Pewee](http://docs.peewee-orm.com)|⛔️|✅|✅|✅|✅
[Pony](https://ponyorm.org)|⛔️|⛔️|✅|✅|✅


## SqlAlchemy
[SqlAlchemy](https://www.sqlalchemy.org) is probably the most well known ORMs for Python. The library is very established which makes it easy to find information online. It has over [17,000](https://stackoverflow.com/questions/tagged/sqlalchemy) questions on Stack Overflow. It also supports a wide variety of use cases and 3rd party integrations,.

Recently, the library's author has been working a large version update. SqlAlchemy2 will have full Async support as well as improved syntax. This makes it a solid choice for use with FastAPI moving forward.

SqlAlchemy is not perfect however. Out of all the ORMs it is possibly the hardest to learn. The syntax is very verbose and the documentation is very difficult to navigate. Once you get past these hurdles though, you'll be using a very powerful library.

## Tortoise
[Tortoise ORM](https://tortoise-orm.readthedocs.io) is one of the new ORMs on the scene. It was designed from the beginning to fully take advantage of Python Aysnc, so it's a great choice for use with frameworks like FastAPI.

Tortoise's syntax also very closely mirrors that of the [Django ORM](https://docs.djangoproject.com/en/3.1/topics/db/queries/) meaning developers coming from Django will feel right at home. It's concise syntax is also very easy to understand a learn.

Unfortunately because Tortoise has not been around long, it is missing some features. There is no support for queryable JSON fields, for example. This could be a deal breaker for some projects. However, if your needs are basic, Tortoise could be the best choice.

## Pewee
[Pewee](http://docs.peewee-orm.com) Pewee is another mature ORM with a very clean and simple syntax. It also supports a variety of use cases, being fairly mature.

Unfortunately the project has no Aysnc support, making it not a great choice for Async frameworks. In fact author of the project actually appears to [openly despise](https://github.com/coleifer/peewee/issues/2189#issuecomment-633756883) Python's approach to Async and has [shut down](https://github.com/coleifer/peewee/pull/2072) several attempts to add support to Pewee.

## Pony
[Pony](https://ponyorm.org) is another Python ORM with a really unique syntax that appears to be a real joy to use. Whereas most ORMs either use manager objects or query builders, Pony attempts to keep your interaction with the database as close to plain Python as possible. Here is an example from the docs:

```python
query = select(c for c in Customer
               if sum(o.total_price for o in c.orders) > 1000)
```

Beautiful!

Unfortunately, Pony does not have Async support, giving it the same problem as Pewee (though the maintainers don't seem as vehemently opposed to it).

The other big ding against Pony is that it's the only ORM on this list without a solution for database migrations. While not having a migrations system might be OK for small applications with 1 or 2 tables, as soon as your project grows and you need to be able to modify your schemas without destroying them in the process, a good migration system in essential.



## Conclusion

If you are starting a new project with FastAPI or a similar framework and need an ORM, at this time I feel like there are really only 2 options.

If your project is using basic features of the database then Tortoise looks to be the winner. This is probably most projects.

If you know your project is going to need to take advantage of special or niche features of the database like queryable JSON or Gis fields, then you probably want to go with SqlAlchemy and take the hit on simplicity for flexibility.
