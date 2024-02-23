---
title: Switching from Disqus to Commento 
date: 2020-09-01T12:12:38-07:00
categories:
    - code 
---

This website has been following the blog software hype train [since it's inception](https://www.pedaldrivenprogramming.com/2006/11/second-day-in-auckland/). The progression went like so:

1. Facebook "posts" (discontinued)
2. Blogger
3. [Blosxom](http://blosxom.sourceforge.net) - a very early static site generator, way ahead of it's time.
4. Wordpress
5. Jekyll
6. Hugo (current)

At the transition between Wordpress and Jekyll, like many others, I needed a solution for comments on a static site and Disqus was the clear choice. But then many of us learned that by using Disqus, we were allowing [ads to be placed](https://blog.disqus.com/our-plans-for-2017) on our own pages. We were bogging down our websites with [loads of third party trackers](https://notes.ayushsharma.in/2017/09/im-killing-disqus-comments-on-my-blog-heres-why) and possibly even [violating our own reader's privacy](https://replyable.com/2017/03/disqus-is-your-data-worth-trading-for-convenience/).

<!--more-->

I started looking for alternatives recently (late, I know) and found [Commento](https://commento.io). It seems to cater to people who want to leave Disqus for the reasons I outlined above: privacy, performance and no ads.

Commento can be used as a service or it can be self hosted. The idea of self hosting the backend on my VPS was very appealing, so I gave it a shot. Overall, it was a pretty painless experience, especially when using the docker image. You simply spin it up with a postgres instance and set [some config vars](https://docs.commento.io/configuration/backend/) for things like email notifications, akismet integration, and google oauth. Then you place the script supplied from this backend on your page and it's good to go.

Here are some links for people who would like to try self hosting Commento:

* [Commento on GitLab](https://gitlab.com/commento/commento)
* [The docs for self hosting](https://docs.commento.io)
* [Freecodecamp article on setting up 3rd party authentication](https://www.freecodecamp.org/news/how-to-setup-worry-free-blog-comments-in-20-simple-steps/) (This is missing from the official docs)
* Note: The Disqus export takes a very long time, in my case 8 hours (!) for < 600 comments. It's almost like they don't want you to back up your data. I'd recommend queuing up a Disqus export first thing if you are planning to migrate off it.

Commento is very nice and I would not hesitate to pay for the hosted version (which I can always migrate to) if it weren't for self hosting being interesting for me. You can check out the hosted service at [commento.io](https://commento.io).
