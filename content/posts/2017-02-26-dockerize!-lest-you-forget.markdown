---
categories:
- code
date: 2017-02-26 18:25:02
title: Dockerize! Lest you forget
---

<img class="img-fluid" src="http://s3-us-west-2.amazonaws.com/pedaldp/images/2017-02-dockerize!-lest-you-forget/docker_logo.png" alt="2017-02-26-dockerize!-lest-you-forget.markdown">

I host quite a few sideprojects on my VPS. They range from static Jekyll sites (like this one) to
[large web applications](http://astrochallenge.com). There's even some wordpress hiding in a corner,
disgraced and neglected.

Despite the fact that none of these sites are actually
useful for anything, they still need some poor bastard to keep then running. Over the years I've
collected quite the assortment of nginx, uwsgi, php, apache, supervisor, and other configs. All
of them written at various levels of understanding, none of them tracked anywhere, all of them confusing
and terrible.

<!--more-->

Docker to the rescue
--------------------
One of the most under-spoken benefits of using docker is that a Dockerfile is literally a
*document describing how to get your garbage apps up and running.* Ever forget a
system dependency for some niche third part library? Have junky code that only runs with
old versions of programming languages? It is nearly impossible to remember the myriad of caveats
that come with deploying software.

If you're like me, and you don't write a ton of documentation, these are the kinds of things
that can really bite you in the ass in the future when you have to modify or redeploy something.

Dockerizing your stuff is an excellent way of documenting what it actually takes to get something
running. Plus you get all the other benefits of containerizing your apps, but there is
nothing I can say here that hasn't been said before about that.

I've gone all in. I'm even using a [jekyll docker image](https://hub.docker.com/r/jekyll/jekyll/) to
generate this site now. As the only ruby application I ever actually use, I always forget the gems
and other dependencies I need in order to run it - no longer.

It's all just a container away.
