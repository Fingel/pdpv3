---
categories:
- code
date: 2015-04-28 21:23:45
title: 'Upgrading Wheezy to Jessie: Nginx and PHP5-fpm'
---

I just upgraded this VPS from Debian Wheezy to Jessie. The upgrade went pretty flawless, excpet some minor issues with postgres and the new bad systemd smell.

However, if you are running NGINX + PHP5-fpm, you may want to read the news that gets
displayed during the upgrade:

	nginx shipped a modified `fastcgi_params`, which declared `SCRIPT_FILENAME`
	fastcgi_param. This line has now been removed. From now on we are also
	shipping fastcgi.conf from the upstream repository, which includes a sane
	`SCRIPT_FILENAME` parameter value.

	So, if you are using fastcgi_params, you can try switching to fastcgi.conf
	or manually set the relevant params.


After the upgrade, I was getting blank responses from nginx for all php scripts. No errors in nginx or fpm logs. After re-reading the news above, the following fix worked for me:

In /etc/nginx/sites-available/* change

`include fastcgi_params`

to

`include fastcgi.conf`

Hope this helps anyone in need.