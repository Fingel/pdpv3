---
categories:
- code
- cartography
- granitemaps
- featured
date: 2014-11-18 14:50:23
featured_image: granitemaps.png
title: Building a trail map for Android using Ionic and Leaflet
---

<img class="import-img" src="http://s3-us-west-2.amazonaws.com/pedaldp/images/2014-11-building-a-trail-map-for-android-using-ionic/phone.png" alt="2014-11-18-building-a-trail-map-for-android-using-ionic.markdown">

__Edit 11/27/2014: GraniteMaps Santa Cruz is now available on the iOS store! [link](https://itunes.apple.com/us/app/granitemaps-santa-cruz/id944142392?mt=8&uo=4)__

It took me a while, but over the weekend I officially submitted my [first app into the Google Play Store](https://play.google.com/store/apps/details?id=com.ionicframework.gmsantacruz735722):

>GraniteMaps: Santa Cruz is a digital trail map for those looking to hike, ride or trot the trails in and around Santa Cruz, CA. GraniteMaps: Santa Cruz provides an easy to read topographical map, current location, trail list, and extra information on local wildlife.

So technically, how did all this come together? Using a bunch of awesome libraries held together by dirty hacks, of course!

<!--more-->

Ionic Framework
---------------

When starting a new project the first decision you make is which framework you want to use, if any. The decision usually depends on many factors:
familiarity with the technology, maturity of the library, userbase, and of course the name. I'm a bigger fan of Doric architecture but I went with the [Ionic Framework](http://ionicframework.com/) anyway because I am already familiar with web technologies. As a bonus your project gets to be "platform agnostic" - whether or not this is true I have yet to see.

Once you get past the unease of installing yet *another* node application globally getting started with the tooling is very easy. Ionic's main executable can generate a basic skeleton app with a few tabs and some example code. Then it's up to you to fill in the rest. Building and deploying to an Android device is a trivial, once you have the Android SDK installed. After bootstrapping the project the only commands I ever found myself running regularly during development were `ionic serve` to start the built-in development server, and `ionic run android` to deploy to my phone for testing.

Besides wrapping [Cordova](http://cordova.apache.org/) to get your webapp running in a web container on smartphones, Ionic is a collection Javascript and CSS libraries nefariously designed to deceive your users into thinking they are running a real app. It works well: your app will have native looking controls and transitions and respond to touch *almost* as well as native. [Angular-JS](http://angularjs.org) is the weapon of choice to do the actual work, this should be great news to all those javascript kiddies already familiar with client side JS frameworks.

Ionic is opinionated in some areas and I'm fine with most of them but I must to complain about the choice of using ui-router instead of ng-route. ui-router is overly complex, impossible to understand and horrendously documented. Now that I think about it, so is  ng-route. And pretty much the entire Angular library. So really I have nothing to complain about except everything. Moving on...

Leaflet
-------

When it is convenient for me I like to tell Google to suck it. Luckily there exists this great library called [Leaflet](http://leafletjs.com) that is awesome for working with maps, so no Google Maps for me. Leaflet has all the features I need: custom tiles, GeoJSON support, and custom markers.

To generate awesome custom tiles, I used [Mobile Atlas Creator](http://mobac.sourceforge.net/). This lets you export a folder structure containing tiles that Leaflet can read instead of using an online source. In my case, I created tiles from USGS topographical maps.

To work with the actual GPS tracks, I used [GPS Logger for Android](https://play.google.com/store/apps/details?id=com.mendhak.gpslogger&hl=en) to collect the data, and [Viking](http://sourceforge.net/projects/viking/) to massage it into it's final GeoJSON form.

Then it's simply a matter of feeding the files to Leaflet. Simple, sort of. I decided to use an [angular directive for leaflet](http://tombatossals.github.io/angular-leaflet-directive/#!/) instead of using the library directly so I could get some fancy two way binding and stuff. This directive turned out to be horribly buggy and I found myself using `leafletData.getMap()` constantly anyway to get direct access to leaflet. In hindsight I should have just saved myself the frustration and used leaflet.js directly, which was nothing but awesome.

I did start to see a performance hit as I got to adding the maximum number of trails in the app. On some older phones, it is visibly laggy. This is one of the trade offs you must make when decided to use something like Ionic instead of native. All in all though, performance was good.

Conclusion
----------

_Ionic: Good. Leaflet: Great. Actually riding: Better than both._

Building this app was an enjoyable and educational experience. With a few tweaks, I wouldn't hesitate to use the same stack again, especially as Ionic is continually improving.

As for the app itself I admit it is rewarding to have an app in a smart phone store that you can tell your friends to install. If anyone will actually use it remains to be seen. I even managed to squeeze an easter egg in. There are trails in that map that are hidden, and only nofreds can access them with special knowledge. Good luck and thanks for reading.