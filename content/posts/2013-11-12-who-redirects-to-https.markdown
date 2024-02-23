---
categories:
- code
date: 2013-11-12 17:49:21
title: Who Redirects to HTTPS?
---

<!-- {{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/image.jpg -->

I was browsing Twitter yesterday, following some people I met at the
[Aaron Swartz memorial hackathon](https://www.noisebridge.net/wiki/Worldwide_Aaron_Swartz_Memorial_Hackathons)
over the weekend when I came across this tweet:

<blockquote class="twitter-tweet"><p>At <a href="https://twitter.com/internetarchive">@internetarchive</a> on Friday, I think <a href="https://twitter.com/brewster_kahle">@brewster_kahle</a> said only 54 of top 1000 sites run HTTPS by default. Can anybody verify that stat?</p>&mdash; Parker Higgins (@xor) <a href="https://twitter.com/xor/statuses/399959103209873409">November 11, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

Nobody seemed to be able to verify that number, so I fired out Geany and
wrote some python to attempt at a verification myself.

<!--more-->

I downloaded the [Alexa top 1,000,000](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip)
.csv and with a combination of cURL and Regex, was able to hack together
a [working albeit ugly script](http://toxiccode.com/misc/httpscheck/httpscheck.py).

To my surprise, the number I came up with was even lower than the estimate.
When the script finally stopped running (it took about 2 hours to cover 1000
urls) the result was that only **44 of the top 1000** sites that I tested
redirected http requests to their domain to https. You can view
a table with the specifics [here](http://toxiccode.com/misc/httpscheck/).

To be fair, this script only tested the initial landing page. Many of the
sites tested will switch to https once the user starts doing something
that involves user input, or dealing with data that may be considered sensitive.

Still, the SSL turnout is less than stellar. Let's hope for an increase to the
0.44 percent figure soon.