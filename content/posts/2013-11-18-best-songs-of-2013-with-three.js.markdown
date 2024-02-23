---
categories:
- code
- featured
date: 2013-11-18 23:34:41
featured_image: bestof2013.png
title: Best Songs of 2013 With Three.js
---

<!-- {{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/image.jpg -->
[![Best of 2013 with Three.js]({{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/screenshot.png "Best of 2013 With Three.js")]({{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/screenshot.png)


I have to admit my favorite thing about the new year has to be all the
awesome "Best Of" remixes and lists that come out just in time for the NYE parties.

I decided this year I was going to make my own. But instead of a boring list,
why not make it interactive? So, I present to you:

**[Best Songs of 2013 with Three.js](http://toxiccode.com/bestof2013/)**

<!--more-->

You can fly around and listen to each of the 6 songs that I chose while
fighting both the controls and epilepsy! Be warned, you should have a
modern browser and a decent tolerance for cheesy indie music or you will
not enjoy this site.

Obviously, I used [Three.js](http://threejs.org/) to set the scene
(pun intended) but I also used [Buzz.js](http://buzz.jaysalvat.com/)
for handling the music because the native `<audio>` element was not holding
up well with so much music playing at once. It was my first time with both
libraries. Three.js has a steep learning curve, but nothing impossible.

One of the coolest things about 3D programming is how much math you have
to use. I can't even remember that last time I got to write code that used
Math.sin and Math.cos, and it made me happy:

{{< highlight javascript >}}
frequency = .3
h = ( 360 * ( 1.0 + time ) % 360 ) / 360;
i = time % 1080
red   = Math.sin(frequency*i + 0) * 127 + 128;
green = Math.sin(frequency*i + 2) * 127 + 128;
blue  = Math.sin(frequency*i + 4) * 127 + 128;

partical_material.color.setRGB(red,green, blue );
ball1.position.y =+ time;
ball_material.color.setHSL( 0.1, 0.3 + 0.7 * ( 1 + Math.cos( time ) ) / 2, 0.5 );
{{< / highlight >}}

Just for completeness sake, here is the track list in no particular order:

1. Alabama Shakes - Always Alright
2. London Grammar - Wasting my Young Years
3. Trails and Ways - Border Crosser
4. Cage the Elephant - Come a Little Closer
5. MØ - Waste of Time
6. Lady Lamb the Bee Keeper - Bird Balloons

Source code (minus the songs, sorry) is [available on github](https://github.com/WD-42/bestof2013).

Happy New Year!