---
title: "A Not so Dramatiq Change: A Celery Alternative"
date: 2018-07-13T10:48:51-07:00
categories:
    - code
    - astronomy
---

Both [Celery](http://www.celeryproject.org/) and [Dramatiq](https://dramatiq.io/) are asynchronous task
processing libraries. You'd use them when you want to be able to parallelize Python code,
and you need more than the [`multiprocess`](https://docs.python.org/3.4/library/multiprocessing.html?highlight=process) module offers, like persistent distributes queues, automatic
retries, and result handling.

I've been using Celery for almost my entire career, and it's treated me well. Recently I've started
to become frustrated with it. There have been [numerous](https://github.com/celery/celery/issues/4731)
[regressions](https://github.com/celery/celery/issues/4753) that have broken my code, as well as some
[totally inexplicable](https://github.com/celery/celery/issues/4341) issues in the last few months
(that last one is the reason I started looking for alternatives).

I know Celery is an open source project maintained by volunteers, and I am grateful for all the hard work
that has been put into it over the years. I just can no longer in good faith recommend it for new projects.

I recently started [a new project](https://mars.lco.global) of my own in which I need to process and store
millions of images of transient astronomical phenomena from a stream of alerts coming from the
[Zwicky Transient Facility](https://www.ztf.caltech.edu/). A perfect use case for a task queue.

Enter Dramatiq: _"a distributed task processing library for Python with a focus on simplicity, reliability and performance"_. A quick look at the [User Guide](https://dramatiq.io/guide.html) gives the impression
that the library is easy to use.

Setting up Dramatiq is indeed simple. You'll need a broker though, either Rabbitmq or Redis. I chose Redis
as it is in general a kickass piece of software that has many other uses. Unfortunately the Dramatiq
docs assume you are using Rabbitmq and it took me some sleuthing to figure out how to hook it up to Redis.
Fortunately, it's pretty easy. To use a Redis broker with Dramatiq:

{{< highlight python >}}
import dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(url=f'redis://{REDIS_HOST}:6379/0')
dramatiq.set_broker(redis_broker)

{{< / highlight >}}

You like that [format string literal](https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep498)
I threw in there? Guess what, Dramatiq only supports Python >= 3.5.

All that was left to do was add the `@dramatiq.actor` annotation to my ingest method, start a worker,
and boom, I was processing tasks in parallel. Even the [default error handling](https://dramatiq.io/guide.html#error-handling) is to retry the task with an exponential backoff, which is exactly what I
wanted. Amazing what you can do with 3 lines of code.

Once I was processing tasks I did notice one issue: the logging. By default Dramatiq logs all arguments
to all tasks received. That's fine if all you're doing is sending an email now and then, but not if you're
processing millions of images with huge arguments.

This is where some lack of documentation and "internet history" for Dramatiq shows. I could not find
a clear method for disabling or reducing the logging. Luckily the [api reference](https://dramatiq.io/guide.html#error-handling) shows that you can directly access the logger on an Actor. Here is an
example of the method I used to disable logging from Dramatiq actors:

{{< highlight python >}}

@dramatiq.actor
def do_stuff():
    print('Im a task!')

do_stuff.logger.setLevel(logging.CRITICAL)

{{< / highlight >}}


Setting the level of the Actor logger to CRITICAL quiets anything less than critical, and I think the
logs I were seeing were either INFO or DEBUG. Not the cleanest solution, but it works.


Despite not being an exhaustive test, I'm so far impressed with Dramatiq.
It's chugging away nicely as I write this. Assuming development continues, I'll probably continue to use
it instead of Celery for future projects.
