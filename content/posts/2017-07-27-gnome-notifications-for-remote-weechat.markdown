---
categories:
- code
date: 2017-07-27 06:02:09
title: GNOME Notifications for Remote Weechat
---

I ❤ [Weechat](https://weechat.org). It's my IRC client of choice. But I also
use it for gtalk and Slack. All my conversations in one convenient interface.
Even better, I run it in a remote tmux session so I can pick up wherever
I left off from anywhere.

The only annoying thing about this setup was the lack of real notifications
for private messages or mentions. So I wrote [Weelisten](https://github.com/Fingel/weelisten).

<img class="img-fluid" src="http://s3-us-west-2.amazonaws.com/pedaldp/images/2017-07-gnome-notifications-for-remote-weechat/weelisten.png" alt="2017-07-27-gnome-notifications-for-remote-weechat.markdown">


Weelisten is a small python script that leverages
Weechat's relay protocol, python 3 asyncio and libnotify so I can get awesome
native notifications on my desktop.

Sounds useful? [Get it on Github](https://github.com/Fingel/weelisten)

<!--more-->
