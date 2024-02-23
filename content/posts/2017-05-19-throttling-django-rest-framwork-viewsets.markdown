---
categories:
- code
date: 2017-05-19 13:25:02
slug: throttling-django-rest-framwork-viewsets
title: Throttling Specific Actions in Django Rest Framework Viewsets
---

If you are using rate limiting with [Django Rest Framework](http://www.django-rest-framework.org/) you probably already know that
it provides some pretty simple methods for setting global rate limits
using [DEFAULT\_THROTTLE\_RATES](http://www.django-rest-framework.org/api-guide/throttling/#setting-the-throttling-policy).
You can also set rate limits for specific views using the `throttle_classes` property on class-based views
or the `@throttle_classes` decorator for function based views.

What if you are using `ViewSets` but want different throttling rules to apply to different actions? Unfortunately
DRF provides no official method of doing this. Luckily we can accomplish this functionality without too much fuss using `get_throttles()`.

<!--more-->

The solution comes from combining the [ScopedRateThrottle](http://www.django-rest-framework.org/api-guide/throttling/#scopedratethrottle)
throttle class with the `get_throttles()` method of `APIView`.


In our `ViewSet` let's override the `get_throttles()` method:

{{< highlight python >}}
    class FooViewSet(viewsets.ModelViewSet):
        queryset = Foo.objects.all()
        serializer_class = FooSerializer

        def get_throttles(self):
            if self.action in ['delete', 'validate']:
                self.throttle_scope = 'foo.' + self.action
            return super().get_throttles()

        @list_route()
        def validate(self, request):
            return Response('Validation!')
{{< / highlight >}}

What we are doing here is pretty simple: checking to see if the action being performed is one we want to throttle , and if so,
setting the `throttle_scope` property on the `ViewSet`.

This alone won't do anything (in fact it will error) so let's add the necessary config to `settings.py` to make it work:

{{< highlight python >}}

    REST_FRAMEWORK = {
        'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.UserRateThrottle',
            'rest_framework.throttling.ScopedRateThrottle',
        ),
        'DEFAULT_THROTTLE_RATES': {
            'user': '5000/day',
            'foo.delete': '100/day',
            'foo.validate': '10000/day'
        }
    }
{{< / highlight >}}

The magic is contained within the [ScopedRateThrottle](http://www.django-rest-framework.org/api-guide/throttling/#scopedratethrottle).
This class will look for the `throttle_scope` property on the view, and if found, look up a corresponding key in the
`DEFAULT_THROTTLE_RATES` dictionary.

Notice that the keys are namespaced with `.foo`. This isn't necessary, but if you're using more than one `ViewSet` and you don't
want the rules to apply to all of them, you should namespace them.

There you have it, throttling for `ViewSets`.
