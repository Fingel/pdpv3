---
title: "Shell Plus for SqlAlchemy" # Title of the blog post.
date: 2021-01-29T14:52:46-08:00 # Date of post creation.
description: "Creating a REPL for SqlAlchemy" # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
# featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
# thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
# shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 0 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: true # Override global value for showing of line numbers within code block.
categories:
  - code
  - python
# comment: false # Disable comment if false.
---

If you've ever used Django, you might be familiar with [Django Extensions Shell Plus](https://django-extensions.readthedocs.io/en/latest/shell_plus.html). It allows you to execute `$ ./manage.py shell_plus` for a very handy iPython REPL with all your ORM models pre-imported. This snippet will allow us to accomplish the same with FastAPI or Flask.

<!--more-->

The key is to use iPython's `embed` feature to create the shell, and the SqlAlchemy class registry to auto import our models. Create a new file `shell.py`:

```python {hl_lines=[3,"5-7"]}
from IPython import embed

from app.database import Base

banner = 'Additional imports:\n'
from app.main import app
banner = f'{banner}from app.main import app\n'

for clzz in Base.registry._class_registry.values():
    if hasattr(clzz, '__tablename__'):
        globals()[clzz.__name__] = clzz
        import_string = f'from {clzz.__module__} import {clzz.__name__}\n'
        banner = banner + import_string

embed(colors='neutral', banner2=banner)
```

In this snippet, you will want to **replace line 3** with the correct import path to your applications `Base` metadata class. I've also demonstrated how to add custom imports that might be handy: you'll want to **replace or remove lines 5-7** with the correct import path for your project's "app" object.

Start it with `python shell.py`

And you should see something like this:
```
$ python shell.py
Python 3.9.1 (default, Jan  8 2021, 17:17:43)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.19.0 -- An enhanced Interactive Python. Type '?' for help.

Additional imports:
from app.main import app
from app.sources.models import Source
from app.sources.models import Comment
from app.auth.models import User

In [1]:
```

In this example, the models `Source`, `Comment`, and `User` are available for me to use and query with normally.
