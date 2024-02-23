---
categories:
- code
date: 2014-04-30 11:13:04
title: Getting the Time Right in Python
---

I hate time. I especially hate dates. There is not a single data type I hate working with more.

I think the problem boils down to the fact that they seem so arbitrary. The [Gregorian calendar](http://en.wikipedia.org/wiki/Gregorian_calendar) just doesn't translate over well to binary systems. Ideally, there would be 100
seconds in every minute, 100 minutes in every hour, 100 hours in every day, etc. But no. We must deal with weird numbers like 60, 24 and 31 (but sometimes 28, or maybe 30) and all the inconsistencies they cause.

&lt;/rant&gt;

I'm going to lay out some of the modules and function in Python relevant to working with time.

<!--more-->

The time module
===============
Documentation: [https://docs.python.org/2/library/time.html](https://docs.python.org/2/library/time.html)


The time module is the most basic module when working with time in python.
`time.time()` returns the time in seconds since the [unix epoch](http://en.wikipedia.org/wiki/Unix_time):

{{< highlight python >}}
time.time()
Out[1]: 1398882554.878436
{{< / highlight >}}

I've found that most operations dealing with time usually boil down to converting something into
a unix timestamp and then perform operations on them. For example:

{{< highlight python >}}
In [1]: a = time.time()
In [2]: b = time.time()
# The first command was executed before the second, so a's second value is less than b's.
In [3]: print a < b
True
{{< / highlight >}}

`time.time()` itself is pretty limited. We can't easily deduce from a unix timestamp the human measurements of time, like minutes hours and days. The timestamp also doesn't contain any timezone
information.

Oh god, timezones.

Timezones are a bitch. When doing anything with time, they must always be accounted for.
A computer in New York that runs `time.time()` at the same one as one in California will return
different values. No, it has nothing to do with a New York minute being any faster than a minute in California, it has everything to do with localtime.

Let's take a look at two more methods, `time.localtime()` and the terribly named `time.gmtime()`:
{{< highlight python >}}
In [1]: time.gmtime()
Out[1]: time.struct_time(tm_year=2014, tm_mon=4, tm_mday=30, tm_hour=18, tm_min=39, tm_sec=33, tm_wday=2, tm_yday=120, tm_isdst=0)

In [2]: time.localtime()
Out[2]: time.struct_time(tm_year=2014, tm_mon=4, tm_mday=30, tm_hour=11, tm_min=39, tm_sec=45, tm_wday=2, tm_yday=120, tm_isdst=1)
{{< / highlight >}}

`time.localtime()` returns a named struct for the localtime, whereas `time.gmtime()` returns the time in Coordinated Universal Time. Why the method is named gmtime and not utctime I have no idea,
but I can only assume 'gm' stands for Greenwich Mean time which should be avoided.

Take a look at `tm_hour` element.

{{< highlight python >}}
In [1]: gmtime = time.gmtime()

In [2]: localtime = time.localtime()

In [3]: print gmtime.tm_hour - localtime.tm_hour
7
{{< / highlight >}}

You can see that the times differ by 7 hours. That's because my computer in located in Santa Cruz, CA. Which as well as being the best place on earth, is located in the Pacific Time Zone, which is
UTC - 8. But wait, why did we get 7 as the time difference?

Because daylight savings time, that's why. Add another point to time's suckiness score.

At least we can figure out if we are in daylight savings or not:

{{< highlight python >}}
In [1]: time.daylight
Out[1]: 1
# Looks like we are in daylight saving time! I'm just having the best time ever!
{{< / highlight >}}

We'll talk about timezones in python more a little later.

Additional Methods
------------------

`time.mktime(t)`

Takes a named struct like the ones returned by `time.localtime()` and `time.gmtime()` and converts it to a unix timestamp:

{{< highlight python >}}
In [1]: time.mktime(time.gmtime())
Out[1]: 1398921105.0
{{< / highlight >}}

Not terribly useful in that context, but you'll want to use it in conjunction with:

`time.strptime(string[, format])`

Takes a string and parses out a time in the format of a named struct, the same format that `time.localtime()` and `time.gmtime()` use. Format is built using directives which
can be found [here](https://docs.python.org/2/library/time.html#time.strftime):

{{< highlight python >}}
In [1]: today = time.strptime('4/30/2014', "%m/%d/%Y")
In [2]: time.mktime(today)
Out[2]: 1398841200.0

{{< / highlight >}}

`time.strftime(format[, t])`

This method takes the time and prints it in a human readable format. Well, sort of. It formats a String From the Time. (StrFTime) so its up to the programmer if he wants to make it readable or not:

{{< highlight python >}}
In [1]: time.strftime('%m/%d/%Y')
Out[1]: '04/30/2014'

In [2]: time.strftime("'Tis the %dth of %B which is the %wrd day of the %Wth week of the year %Y")
Out[2]: "'Tis the 30th of April which is the 3rd day of the 17th week of the year 2014"

In [3]: time.strftime("The time is %H:%M")
Out[3]: 'The time is 13:55'

{{< / highlight >}}

The datetime module
===================

You could do everything you wanted to do with the time module alone. But in most cases, you would
be insane to do so. the `datetime` module provides some high level functionality for working with dates. From the [documentation](https://docs.python.org/2.7/library/datetime.html):

> While date and time arithmetic is supported, the focus of the implementation is on efficient
> attribute extraction for output formatting and manipulation.

Basically, we want to be able to do thing things like "add one week to this date and print the result" without going [batshit insane](http://english.stackexchange.com/questions/38354/where-did-the-phrase-batsht-crazy-come-from).

One of the main gotchya's with the datetime module is the concept of *naive* vs *aware* time objects.

Aware objects are "aware" of timezone and daylight savings time. So a datetime of 4:00am, 1st of April 2014 that is aware and set to PST, would represent 7:00am, 1st of April 2014 in EST.

"Naive" dates represent absolute values. The same object representing 4:00am, 1st of April, 2014 would still read 4:00am, 1st of April, 2014 in PST and EST.

Let's check out an example using the `pytz` module to help with timezones:

{{< highlight python >}}
import datetime
import pytz

# Set the timezones
In [1]: eastern = pytz.timezone('US/Eastern')
In [2]: pacific = pytz.timezone('US/Pacific')

# Make 2 dates using the same naive datetime, and localize them to the timezone.
In [3]: eastern_dt = eastern.localize(datetime.datetime(2013, 10, 1, 12, 0, 0))
In [4]: pacific_dt = pacific.localize(datetime.datetime(2013, 10, 1, 12, 0, 0))

#subtact the time
In [5]: diff = pacific_dt - eastern_dt

In [6]: diff.seconds
Out[6]: 10800 # 3 hours
{{< / highlight >}}

Basically, working with timezones is a pain. It's best just not to do it and **always store time in UTC**, converting to localtime for display purposes only using a method like `datetime.datetime.fromtimestamp()`


The datetime.date object
------------------------

the `datetime.date` object is about as close as you can get to representing a "date" as most people understand them in code:

{{< highlight python >}}
In [1]: today = datetime.date.today()
In [2]: print today
2014-04-30

In [3]: print today.month
4

In [4]: tomorrow = datetime.date(2014, 5, 1)
In [5]: print tomorrow.month
5

{{< / highlight >}}

You can convert the date into the format heavily used by the `time` module:

{{< highlight python >}}
In [1]: first_of_this_month = datetime.date.today().replace(day=1)

In [2]: first_of_this_month
Out[3]: datetime.date(2014, 4, 1)

In [4]: first_of_this_month.timetuple()
Out[4]: time.struct_time(tm_year=2014, tm_mon=4, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=91, tm_isdst=-1)

In [5]: time.mktime(first_of_this_month.timetuple())
Out[5]: 1396335600.0

In [6]: datetime.date.fromtimestamp(1396335600.0)
Out[6]: datetime.date(2014, 4, 1)

{{< / highlight >}}


The `datetime.date` object has other useful methods such as `date.isoformat()` which prints the date in ISO 8601 format (YYYY-MM-DD) and `date.strftime()` which functions the same as `time.strftime()` allowing you to print dates in whatever format you'd like.

The datetime.datetime object
----------------------------

`datetime.datetime` is the same as `datetime.date` except it includes time data as well.

{{< highlight python >}}
In [1]: datetime.datetime.today()
Out[2]: datetime.datetime(2014, 4, 30, 15, 20, 15, 86516)
{{< / highlight >}}

Remember to watch out for TZ gotchyas.

The timedelta object
--------------------

A `timedelta` object represents a duration - meaning the difference between two times. Thus it helps us set times in the future or past.


Lets try a simple use case. Print the time one week from today:

{{< highlight python >}}
In [1]: today = datetime.datetime.today()
In [2]: print today
2014-04-30 16:58:02.663769

In [3]: print today + datetime.timedelta(weeks=1)
2014-05-07 16:58:02.663769
{{< / highlight >}}

We can also obtain `timedelta` objects from performing arithmetic operations on `datetime` objects:

{{< highlight python >}}
In [1]: today = datetime.datetime.today()

In [2]: print today
2014-04-30 17:02:00.378875

In [3]: future = datetime.datetime(2014, 11, 1)

In [4]: print future
2014-11-01 00:00:00

In [5]: print future - today
184 days, 6:57:59.621125

{{< / highlight >}}

Stuff to remember
----------------

1. It's a good idea to always store time in UTC. Convert to localtime as late as possible.
2. Use the high level libraries as much as possible. You may think you can pull off using
`time.time()` when in reality, you're forgetting in your calculations that this month has 31 days instead of 28. The higher level libraries are good at taking these inconsistencies into account.
3. Stay sane, go outside, hug your mother.