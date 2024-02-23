---
title: "Dynamic Module Loading in Python"
date: 2018-08-23T10:48:51-07:00
draft: true
categories:
    - code
    - python
---

There are some cases where dynamically loading code that your application
doesn't know about ahead of time can be useful. For example, perhaps you're
writing a text editor and you want it to be extendible via plugins. Or you are
writing a library and you'd like your users to be able to provide their own
integrations for 3rd party services. In any case, this pattern is very
achievable in python.

For this post, let's write a program that collects the latest top stories from
various news aggregator sites like Reddit, Hacker News, etc. Let's call it
`ubernews.py`. We want to make it super easy for anyone who downloads UberNews
to add their own modules for their favorite news sites. So UberNews needs to
be able to access modules which aren't part of it's own codebase.

Since UberNews is pretty lame, it's only going to ship with Reddit support
by default. Once we have Reddit working, we'll write a module for Hacker News
(as if we were another developer) and load it into the main application.

First, some requirements. We'll be making some http calls and
since I'm not a masochist, we'll be using the `requests` library, so make
sure you install it into a virtualenv or have access to it globally.

Additionally, we're going to explore some cool new features of Python 3.7,
specifically [Data Classes](https://docs.python.org/3/library/dataclasses.html)
so make sure you are running at least Python 3.7.

Ok, let's get started with a boilerplate `ubernews.py`:

{{< highlight python >}}

#!/bin/env python3
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsItem():
    score: int
    title: str
    url: str
    time: datetime


class RedditNews:
    def get_news(self):
        return [
            NewsItem(score=1, title='test', url='example.com', time=datetime.now())
        ]


def main():
    print('Top news for today:')
    reddit = RedditNews()
    for news_item in reddit.get_news():
        print(news_item)


if __name__ == '__main__':
    main()

{{< / highlight >}}

And the output:

	$ ./ubernews.py
        Top news for today:
        NewsItem(score=1, title='test', url='example.com', time=datetime.datetime(2018, 8, 23, 17, 24, 8, 417234))

Let's go through the members of this module.

First, we have the NewsItem dataclass. If you are not familiar with Python
Data Classes, basically they are syntatic sugar for generating classes with
auto generated methods, like `__init__()` and `__repr__`. Here we are simply
using it do define a class with a few attributes, without needing to write
a boilerplate `__init__()` function. We'll get into some of the more useful
features of Data Classes later.

Next we have the `RedditNews` class. It has a single method, `get_news()`.
All it does is return a list of `NewsItems`, and for now a single, fake one.

Next, our `main()` function simply prints out a banner message and all of
`redditNews`'s news items.

Let's make this program actually do something:


