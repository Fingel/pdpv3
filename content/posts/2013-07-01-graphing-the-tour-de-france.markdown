---
categories:
- Cycling
- Code
date: 2013-07-01 00:00:00
title: Graphing the Tour De France
type: post
---

Two things are going on right now:

1. The Tour De France.

2. I need to learn a new charting library.

I started looking around and <a title="Highcharts" href="http://www.highcharts.com/">Highcharts</a> seemed like a nice JS solution with a complete API. It does require a license for commercial use, though.

At the same time, I found a bunch of cool historical data on the Tour De France. I set up a MySQL database, made a few PHP pages, and here we have the results.

The most interesting metric is the average speed of the winner over the years. It is amazing to see the acceleration, though there appears to be an plateau or possible even a decline in the last few years. Doping possibly?

<iframe width="608" height="400" style="border: 0px none transparent;" src="http://toxiccode.com/misc/tdf-stats/speedbyyear.php" frameborder="0" scrolling="no"></iframe>

What ages are winning the tour?

<iframe width="608" height="400" style="border: 0px none transparent;" src="http://toxiccode.com/misc/tdf-stats/agebyyear.php" frameborder="0" scrolling="no"></iframe>

And the obligatory wins by country:

<iframe width="608" height="420" style="border: 0px none transparent;" src="http://toxiccode.com/misc/tdf-stats/winsbycountry.php" frameborder="0" scrolling="no"></iframe>

Now, back to watching the races.