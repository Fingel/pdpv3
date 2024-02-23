---
categories:
- code
- books
date: 2013-11-22 00:10:09
title: Scanning with the Digital Anarchists
---

<!-- {{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/image.jpg -->
[![Scanning with the Digital Archivists]({{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/header.jpeg "Scanning with the Digital Archivists")]({{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/header.jpeg)

[Noisebridge](https://noisebridge.net/). I've only been there twice now and it's
already become one of my favorite places to hang out in San Francisco. Noisebridge
is a unique place where the anarchistic ideals of my youth and my current love of technology
exist in tandem. Not only is there amazing hacking going down but I've also found
myself once again doing things like trash talking Crimethinc and comparing
dumpster diving stories. Ah, it feels good (and smells bad!).

<!--more-->

Depending on the kind of "hacker" you are you will either love or hate this place.
Are you (A) the kind of hacker that loves technology and learning as an end in of itself?
Or (B) the kind of hacker that would do questionable things in the back room of
a VC's office to secure funding for your snapchat for cats app? In this case B
stands for don't Bother.

One of the cooler projects to emerge from the chaos is the work being done on a DIY
book scanner. The [Digital Archivists](https://noisebridge.net/wiki/Digital_Archivists)
meet every Thursday in the space and hack away at it. I got to join them this week
and had a stab at getting some OCR (Optical Character Recognition) software working
so that we can <strike>break some copyright law</strike> convert images of pages
into actual text.

[Tesseract](https://code.google.com/p/tesseract-ocr/) is some amazing software that
takes images as input and spits out text files. In fact the software is so simple
(at least by default) and effective that converting an actual .tiff of a page to
a text file is as simple as:

`$tesseract page0001.tiff page0001.txt`

Considering Tesseract is doing all the hard work, all I had to do was write a
[simple shell script](https://gist.github.com/WD-42/7595388) to wrap it and convert
entire directories of images to text.

As dorky as it may seem I find it something very satisfying about seeing  a
physical book go from ink on paper to bytes in memory. Pretty dorky actually.
Goodnight.