---
title: Speeding Up API Endpoints using Python AsyncIO
date: 2021-09-25T12:19:01-07:00
categories:
    - code
    - python
draft: true
---

As a developer, you want the APIs you write to be as fast as possible. So what if I told you that with *this one simple
trick*, you might be able to increase the speed of your API by 2x, 3x, or maybe even 4x? You'd probably tell me to get lost with the clickbait, but hear me out. In this article you will learn how to utilize Python **asyncio**, the **httpx** library, and the **Flask** micro framework to optimize certain parts of your API.

<!--more-->

In this tutorial you will:

1. Write a small HTTP API using everyone's favorite Python framework: [Flask](https://flask.palletsprojects.com/en/2.0.x/).
2. Use [httpx](https://www.python-httpx.org/), an awesome modern Python HTTP client that supports async.
3. Familiarize yourself with a small subset of Python's [asyncio](https://docs.python.org/3/library/asyncio.html) Library.

## One app, two endpoints.

To begin this feat of strength, you will write a simple Flask app with two endpoints. One will be asynchronous and the other will not.

__For maximum compatibility, please make sure you are using Python **3.8** or newer.__

Begin by creating a directory to hold your code and create a virtual environment in it:

```bash
mkdir asyncapi
cd asyncapi
python3 -m venv env/
```

Activate the virtual environment and install Flask with async support.

```bash
source venv/bin/activate
pip install Flask[async]
```

Next, place the following code in a file named **app.py**.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/get_data')
def get_data():
    return 'ok'

@app.route('/async_get_data')
async def async_get_data():
    return 'ok'
```

You now have a fully working Flask API with two endpoints. If you are new to Flask and are curious what is going on here, check out the [Flask quickstart documentation](https://flask.palletsprojects.com/en/2.0.x/quickstart/).

Notice that the second endpoint, `/async_get_data` uses the `async def` syntax for defining it's method. Still, this endpoint does exactly the same thing as the normal `/get_data` endpoint, except that we can run asynchronous code in it. As it is written now, however, it is not any faster. We can prove this by running our API and making a few calls with **cURL**.

Start the Flask development server:

```bash
flask run
```
Now **time** some cURL requests to show that both endpoints return in about the same time:

```bash
time curl "http://localhost:5000/get_data"
ok
________________________________________________________
Executed in    7.28 millis    fish           external
   usr time    5.86 millis  248.00 micros    5.61 millis
   sys time    0.03 millis   32.00 micros    0.00 millis
```

Notice the line that says "Executed in 7.28 millis". That's pretty quick. Try again using the other endpoint:

```bash
time curl "http://localhost:5000/async_get_data"
ok
________________________________________________________
Executed in   21.77 millis    fish           external
   usr time    2.48 millis    0.00 micros    2.48 millis
   sys time    2.77 millis  293.00 micros    2.48 millis
```

Not only was the async version not faster, it was about 3x slower. The difference between 7 miliseconds and 21 miliseconds is not noticeable to our human eyes, But this is a good demonstration that there can be overhead to using asyncio, so it is not faster in *all* situations.

## Two endpoints, one fast, one slow.

In order to see the `async_get_data` endpoint become faster than it's sync counterpart, you'll have to make the endpoints actually do some work. One common case for APIs is that they need to make calls to other APIs, for example, to fetch the weather for a specific location from a third party service.

You can add HTTP requests to your API using a combination of `httpx` and [Flash](https://flash.siwalik.in/), a service that intentionally returns slow HTTP responses. Why slow? Because you want to be able to simulate large and or slow external APIs, as well as exaggerate the effect of using asyncio.

First, install the `httpx` library:

```bash
pip install httpx
```

Modify `app.py` to look like this:

```python
from flask import Flask
import asyncio
import httpx

app = Flask(__name__)

@app.route('/get_data')
def get_data():
    r1 = httpx.get('https://flash.siwalik.in/delay/1000/')
    r2 = httpx.get('https://flash.siwalik.in/delay/1000/')

    return {
        'r1': r1.status_code,
        'r2': r2.status_code
    }

@app.route('/async_get_data')
async def async_get_data():
    async with httpx.AsyncClient() as client:
        c1 = client.get('https://flash.siwalik.in/delay/1000/')
        c2 = client.get('https://flash.siwalik.in/delay/1000/')
        results = await asyncio.gather(c1, c2)

        return {
            'r1': results[0].status_code,
            'r2': results[1].status_code
        }
```

Both endpoints now make two GET requests to https://flash.siwalik.in/delay/1000/, which returns a simple response after one second. The first method `get_data` should look familiar to anyone who has used the Python `requests` library. `r1` contains the result of the first API call, and r2 contains the result of the second API call. The method then returns the status code of each response.

The second method, `async_get_data`, looks a bit different, although the end result is the same. Going step by step, this is what is happening:

```python
async with httpx.AsyncClient() as client:
```

The code creates an asynchronous context manager which makes the `client` object available. This is the same thing as a normal context manager, except that it allows the execution of asynchronous code. `client` is what makes the actual http calls.

```python
c1 = client.get('https://flash.siwalik.in/delay/1000/')
c2 = client.get('https://flash.siwalik.in/delay/1000/')
```

Next, two variables are assigned the results of calling `client.get()` on the two API calls to the Flash API. At first you might assume that the results of the API calls will be stored in these variables, but actually, c1 and c2 are `co-routines`, not HTTP responses.


```python
results = await asyncio.gather(c1, c2)
```

Now the magic of async happens. Here the return value of `asyncio.gather()`is assigned to the `result` variable, and it is `await`ed. When you see the `await` keyword, it means that the code will block execution there until the call to a co-routine is complete. The `gather` method itself is a co-routine, and will execute a sequence of other co-routines (like [c1, c2]) *concurrently*, and then return a list of results.

```python
return {
    'r1': results[0].status_code,
    'r2': results[1].status_code
}
```

Finally, the method returns the status code for each HTTP response by accessing it within the array of results.


Calling `get_data` and `async_get_data` should result in the exact same result, but `async_get_data` will complete much faster. How much faster do you think it will finish?

## Timing the Results

Now that you have an API with two endpoints that do the same thing, except one is async and one is not, you should return to using cURL to time them.

Start with `get_data`:

```bash
time curl "http://localhost:5000/get_data"
{"r1":200,"r2":200}

________________________________________________________
Executed in    3.56 secs      fish           external
   usr time    0.29 millis  295.00 micros    0.00 millis
   sys time    5.00 millis   48.00 micros    4.96 millis
```

You can see that both responses return an HTTP 200, and in total your endpoint took about 3.5 seconds to return. That makes sense: the external endpoints (Flash) paused for one second each and the extra 1.5 seconds of other overhead can be accounted for in DNS lookups, tcp connections, slow Comcast internet, and other internet related spaghetti.

Next, try timing the `async_get_data` endpoint:

```bash
time curl "http://localhost:5000/async_get_data"
{"r1":200,"r2":200}

________________________________________________________
Executed in    1.81 secs      fish           external
   usr time    6.21 millis  342.00 micros    5.87 millis
   sys time    0.06 millis   59.00 micros    0.00 millis
````

If in the previous section you guessed that the async version would be about twice as fast, you are correct! Why? Because the calls to the external API were run concurrently. That means that in this case, the entire act of retrieving the results from the Flash API was only as slow as the slowest call.

In fact, you can try adding a third call to each method. The first endpoint will take roughly 1.5 seconds longer, while the async version will still execute in roughly 1.8 seconds. You can keep adding HTTP calls to the aysnc version and it should *continue* to return in roughly the same amount of time until you start hitting various hardware, network and operating system level constraints.

## A Real World Use Case.

You may think this is a contrived example. How often do you write endpoints that make multiple external HTTP calls? However, HTTP calls aren't the only place where asyncio can make a difference. In fact, it's right there in the name: Asynchronous Input/Output.

We often use databases to back our APIs and getting the results of a SQL query from a database server is often bound by I/O. We could replace one of the calls to the Flash API in our app with a call to a database. Let's say this DB call returns a lot of data and takes 500 milliseconds to return. Imagine now that you replaced one of the HTTP calls in the endpoints written earlier with a call to a database. This seems like a more realistic example.

The first endpoint, `get_data`, would take roughly 1.5 seconds to return the result: 1 second for the HTTP call, and 0.5 seconds for the DB call.

The second endpoint, `async_get_data`, would take roughly 1 second to return the result: 1 second for the HTTP call, 0.5 seconds for the DB call, but both execute *concurrently*. This means it only takes as long as the slowest operation to return the result. That's still 0.5 seconds we saved by using asyncio!

Keep in mind that if you need the results of one async call for the next async call, this won't be much help.

## Conclusion

In this article you learned how Python's asyncio can speed up your application considerably in situations where your code is waiting on multiple instances of Input/Output. You also learned how asyncio can be used effectively and easily with the Flask web framework and the HTTPX library.

Asyncio won't always make your API faster, but in certain situations like demonstrated in this tutorial, it can make a huge difference. Keep what you learned here in mind when writing APIs or other code in the future and you might gain some easy performance wins!
