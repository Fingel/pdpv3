---
categories:
- astronomy
- code
- astrochallenge
date: 2015-02-25 14:08:56
title: Reviving fchart to Create Beautiful Astronomical Finder Charts
---

I've spent a good deal of time in the last few days searching for a good library to draw star charts (finder charts) that I could use to integrate with AstroChallenge. While there are plenty of utilities to create star maps, they mostly consist of desktop software or websites that are not open source.

<img class="img-fluid" src="http://s3-us-west-2.amazonaws.com/pedaldp/images/2015-02-creating-finder-charts-for-astronomy-using-fchart/m31.jpg" alt="2015-02-25-creating-finder-charts-for-astronomy-using-fchart.markdown">

Eventually I found [fchart](https://www.astro.rug.nl/~brentjen/fchart.html) which resembled was I was looking for. A set of python scripts with minimal dependencies that would output star maps! This I could use.

<!--more-->

I extracted the package downloaded from Michiel Brentjens' website and hit go... nothing. Then I realized the file's last modified date: 2005. Uh-oh. It depended on numarray, a package long ago replaced by [numpy](http://www.numpy.org/).

But the source was clean, so I decided to see if I couldn't upgrade it to work in numpy and python2.7. Indeed, after a few find/replaces and some method renaming, the code ran! However, there was another problem. The tyc2.bin file from fchart website seemed to be corrupt - I couldn't get any stars to draw. So I headed over to [http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/259](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/259) and grabbed a fresh copy of the tyco2 star database, concatenated the archives and created a new tyc2.bin file using the [tyc2\_to\_binary](https://github.com/Fingel/fchart/blob/master/scripts/tyc2_to_binary) script.

Now everything appears to be working. The image above is an example of a chart generated for the Andromeda Galaxy. I emailed Michiel to let him know about my modifications and that I've hosted the code on [github](https://github.com/Fingel/fchart). The repo also contains the new tyc2.bin file that contains the star catalog - so the installation should run out of the box without issues.

This is a great example of why open source software works. Not only can the software be useful to a wider audience now, but I plan on adding my own improvements and functionality.


[Get fchart](https://github.com/Fingel/fchart)

[Michiel Brentjens' website](https://www.astro.rug.nl/~brentjen/fchart.html)