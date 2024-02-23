---
categories:
- AstroChallenge
- astronomy
- code
date: 2015-02-19 17:56:31
title: Using Django and PyEphem to Determine the Location of White Fuzzies
---

I've been working on new project recently called AstroChallenge.
While the details of what exactly AstroChallenge is will have to come later,
rest assured, it has to do with Astronomy.

<img class="img-fluid" src="http://s3-us-west-2.amazonaws.com/pedaldp/images/2015-02-using-pyephem-to-determine-the-location-of-white-fuzzies/right_ascention.png" alt="2015-02-19-using-pyephem-to-determine-the-location-of-white-fuzzies.markdown">

One of the bits of information I'm interested in is whether a particular
celestial object is visible in the sky or not. Given an observer's latitude, longitude and elevation and an object's right ascension and declination it becomes a straightforward calculation.

<!--more-->

However, there are libraries written by smarter people than I and it would be a good idea to use them. So instead if spending my time carefully coding maths, I can simply:

`$pip install pyephem`

and

`import ephem`

into my project.

Now the work is done for me. Isn't the modern age great?

[PyEphem](http://rhodesmill.org/pyephem/) is a great python library for performing calculations on all sorts of celestial objects including planets,
moons, comets, asteroids, stars and deep space objects. Once you input
your observation date, time and location some of the interesting functions
you can run include:

* Next transit

* Altitude, Azimuth

* Distance from Earth, Sun, other bodies

* Current Constellation

* Phase, day, month and year

And so on. When you set up an observer, you can even supply dates in the path so you can, for example, find the positions of the moons of Jupiter on  February 15, 1564.

Since AstroChallenge is a webapp written in [Django](https://www.djangoproject.com/) we have data models for things like deep space objects on which we can
place handy methods to get information from pyephem:

(fields truncated for readability)
{{< highlight python >}}
class DeepSpaceObject(models.Model):
    ra_hours = models.IntegerField()
    ra_minutes = models.FloatField()
    dec_sign = models.CharField(max_length=1, choices=(('+', '+'), ('-', '-')), default="+")
    dec_deg = models.IntegerField()
    dec_min = models.FloatField()

    @property
    def fixed_body(self):
        """ Return a FixedBody object which PyEphem uses to perform calculations """
        object = ephem.FixedBody()
        object._ra = "{0}:{1}".format(self.ra_hours, self.ra_minutes)
        object._dec = "{0}{1}:{2}".format(self.dec_sign, self.dec_deg, self.dec_min)
        return object

    def observation_info(self, observer):
        """ Given an observer, perform the calculations we are interested in and return them as a dictionary """
        p_object = self.fixed_body
        p_object.compute(observer)
        up = True if ephem.degrees(p_object.alt) > 0 else False
        return {
            'alt': str(p_object.alt),
            'az': str(p_object.az),
            'up': up,
            'neverup': p_object.neverup,
            'rise': timezone.make_aware(observer.next_rising(p_object).datetime(), pytz.UTC) if p_object.rise_time else None,
            'set': timezone.make_aware(observer.next_setting(p_object).datetime(), pytz.UTC) if p_object.set_time else None
        }
{{< / highlight >}}

Some things to note:

* An object is "visible" if it's Altitude is greater than 0, meaning it is above the horizon. If it still light out, or you live in a light polluted area, you're probably still out of luck, though,

* PyEphem's `Observer.next_rising/setting` methods may return `None`, that means an object either never rises (as can be determined using `Body.neverup`) or never sets.

The `Observer` data can be provided using a simple method on a UserProfile model:

{{< highlight python >}}
class UserProfile(models.Model):
    user = models.OneToOneField(User, editable=False)
    timezone = TimeZoneField(default="UTC")
    lat = models.FloatField("latitude", default=0.0)
    lng = models.FloatField("longitude", default=0.0)
    elevation = models.IntegerField(default=0)

    @property
    def observer(self):
        observer = ephem.Observer()
        observer.lat, observer.lon, observer.elevation = str(self.lat), str(self.lng), self.elevation
        return observer

    @property
    def sunset(self):
        sun = ephem.Sun()
        sun.compute(self.observer)
        return timezone.make_aware(self.observer.next_setting(sun).datetime(), pytz.UTC)

{{< / highlight >}}

Notice the `observer` property just returns an observer, so we can now supply it in our views to a Celestial object and get the information we need. Another
handy property, `sunset` uses the `observer` property to compute the time at
which the sun will be setting for this user. PyEphem rocks.