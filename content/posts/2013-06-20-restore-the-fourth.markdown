---
categories:
- code
- featured
date: 2013-06-20 00:00:00
featured_image: rt4.png
title: Coding Restore The Fourth
type: post
---

Recently we have learned that a certain branch of the government
may be overstepping the consitutional right to privacy.
While this may be <a href="http://www.cispaisback.org/">old
news for many</a> the recent leaks by Edward Snowden have brought the issue
to national attention and have caused quite a stir.

And rightly so, the argument can be made that the NSA is violating the forth amendment.
Restore the Fourth, a grassroots organization that sprung up nearly overnight,
is making that argument and taking it to the public.

From the <a href="http://www.restorethefourth.net">website</a>:
>Restore the Fourth is a grassroots, non-partisan movement; we believe
>the government of the United States must respect the right to privacy of
>all its citizens as the Fourth Amendment clearly states. We seek to bring
>awareness to the abuses against our civil liberties and the erosion of
>this cornerstone of our democracy.

I'm sympathetic with this cause. And despite most likely being placed on a
government watch list for the rest of my life, I decided to take a crack
at building these folks a website. The decision was
made to use <a href="https://www.djangoproject.com/">Django</a>, a neat
framework written in Python.

One of the most interesting features of the website is the map on the front page.
The locations are set by pulling objects from the database that represent
protests. These objects are editable in the back end by regular admins
using Django's awesome gui admin interface so developers do not need to
be involved.

When creating a protest via the admin interface you don't need
to supply a latitude/longitude pair (which are needed for google maps)
but instead the backend utilizes the <a href="https://developers.google.com/maps/documentation/business/geolocation/">Google Maps Geolocation Api</a>
so all that's needed is a city and/or state. To make that process easy,
we're using <a href="https://code.google.com/p/geopy/">geopy</a>, a
geolocation library for Python. In the Protest model, we can simply call this:

{{< highlight python >}}
def generateLatLong(self):
    g = geocoders.GoogleV3()
    place, (lat, lng) = g.geocode("{0} {1}".format(self.state, self.city),exactly_one=True)
    self.latitude = lat
    self.longitude = lng
{{< / highlight >}}
to generate a proper latitude/longitude pair for the object, using it's city and state.

Then in our views, we make a method to serialize these objects as json:
{{< highlight python >}}
def protestsjson(request):
    protest_list = Protest.objects.all()
    data = serializers.serialize('json', protest_list)
    return HttpResponse(data, mimetype="application/json")
{{< / highlight >}}

From there, its just a matter of telling the google map to use those objects to create markers:

{{< highlight javascript >}}
var map = new EventsMap();
    $.getJSON('/protests.json', function(data){
    map.plotStaticMarkers(data);
});

// plot new markers on the map, make them interactive
this.plotStaticMarkers = function(data){
    $.each(data, function (i, location) {
        var latlng = new google.maps.LatLng(location.fields.latitude, location.fields.longitude);
        var marker = new google.maps.Marker({
             map: map,
             position: latlng,
             title: location.fields.city
        });

         google.maps.event.addListener(marker, 'click', function () {
         var content = infoWindowTemplate
              .replace('{location}', location.fields.city)
              .replace('{info}', location.pk);

         infoWindow.setContent(content);
         infoWindow.open(map, marker);
         });
    })
}
{{< / highlight >}}

And there we have it, a neat interactive map that doesn’t require a developer's involvement to edit.

Check it out in action: [restorethefourth.net](http://www.restorethefourth.net)

As usual, the source is available on [Github](https://github.com/AustinRiba/rtf)

<iframe width="100" height="20" src="http://ghbtns.com/github-btn.html?user=AustinRiba&amp;repo=rtf&amp;type=fork&amp;count=true" frameborder="0" scrolling="0"></iframe>