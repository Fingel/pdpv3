---
title: "FastAPI Fundamentals: Data Serialization and Pydantic" # Title of the blog post.
date: 2020-12-16T21:53:46-08:00 # Date of post creation.
description: "An introduction to Pydantic for FastAPI developers." # Description used for search engine.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
categories:
  - code
  - python
  - tutorial
# comment: false # Disable comment if false.
---
[Pydantic](https://pydantic-docs.helpmanual.io) is one of the "secret sauces" that makes FastAPI such a powerful framework. The library is used everywhere in our projects: from validation, serialization and even configuration. Understanding better what Pydantic does and how to take advantage of it can help us write better APIs.

<!--more-->

## The problem of working with JSON

Before we delve into Pydantic, let's quickly acknowledge the language modern APIs use: JSON. JSON is the lingua franca of modern APIs, and chances are any new app you start will speak it.

Let's imagine an API that's purpose is to provide a worldwide database of every pie imaginable: apple, pumpkin, even blackbird. This API allows us to search for pies based on name or ingredient and it also allows us to add pies. CRUD pies? Yes please.

OK, now imagine we want to add a pie to the database. We would send some JSON that looks something like this:

  POST https://allpies.io/pies/

```json
{
  "name": "API Pie",
  "calories": 9000,
  "description": "A tasty pie, clean presentation but a messy filling.",
  "ingredients": [
    "python",
    "pydantic",
    "FastAPI",
  ]
}
```

Simple enough. Now let's go over all the steps that our fictional Python backend would have to through in order to persist this delicious API Pie into the database.

The simplest implementation of an endpoint might look like this:

```python
@app.post('/pies')
def create_pie(request):
    data = request.json()
    save_pie_to_database(data)
```
This obviously will not work. What if the JSON payload is missing fields, or is malformed? `save_pie_to_database` will definitely throw an error, and we want to avoid that. So let's add a check to make sure all the required fields are supplied:

```python
@app.post('/pies')
def create_pie(request):
    data = request.json()
    required_fields = ['name', 'calories', 'description', 'ingredients']
    if not set(required_fields).issubset(data.keys()):
      return HTTPError('Missing fields!')
    save_pie_to_database(data)
```
This is a little better, but still really bad. We don't even tell the client which field they are missing if they fail to send one.

Even worse, we need to check to make sure the _type_ of the data is correct. What if the client sends a string for `calories`? Saving to the database will fail. So we add another check:

```python
@app.post('/pies')
def create_pie(request):
    data = request.json()
    required_fields = ['name', 'calories', 'description', 'ingredients']
    if not set(required_fields).issubset(data.keys()):
      return HTTPError('Missing fields!')
    if not type(data['calories']) == int:
      return HTTPError('Calories must be an integer!')
    save_pie_to_database(data)
```

This is just too ugly, and too much work to simply create a silly pie. This problem of taking arbitrary data and converting into Python and/or database objects is known as **serialization**. Making sure our data is good, is called **validation**. Pydantic helps us with both.

## Serializers to the rescue

Most web frameworks provide some method of serializing/deserializing data from HTTP requests and responses. For example, [Django Rest Framework](https://www.django-rest-framework.org/api-guide/serializers/) dedicates an entire three chapters just to it's serializers. They look like this:

```python
class PieSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    calories = serializers.IntegerField()
    description = serializers.CharField()
    ingredients = serializers.ListField(serializers.CharField())
```

We want to use FastAPI though, not Django. Luckily this is where Pydantic comes in.

## Playing with Pydantic

If you haven't already, install Pydantic into a virtualenv:

    $ pip install pydantic

The following code snippets will run as valid Python, so fire up your editor and prepare to copy and paste!

Using Pydantic, let's define a "model" (kinda like a serializer) for a pie. Then we will give it some data and see what happens!

```python
from pydantic import BaseModel, constr
from typing import List

new_pie = {
    "name": "API Pie",
    "calories": 9000,
    "description": "A tasty pie, clean presentation but a messy filling.",
    "ingredients": [
        "python",
        "pydantic",
        "FastAPI",
    ]
}


class Pie(BaseModel):
    name: constr(max_length=200)
    description: str
    calories: int
    ingredients: List[str]


pie = Pie(**new_pie)
print(pie.name)
print(pie.calories)
print(pie.dict())
```

The output should look like this:

```
API Pie
9000
{'name': 'API Pie', 'description': 'A tasty pie, clean presentation but a messy filling.', 'calories': 9000, 'ingredients': ['python', 'pydantic', 'FastAPI']}
```

Neat! With just a few lines and some sweet Python3 type annotations we've created a way to take arbitrary data (in this case a dictionary, but we trust you can figure out how to use `json.loads()`) and turn it into a python object.

But what happens when the data is invalid? Add this to the bottom of the script:

```python
from pydantic import ValidationError
new_pie['calories'] = 'Many, many calories. But not a number.'
try:
    pie = Pie(**new_pie)
except ValidationError as e:
    print(e.json())
```

The script will now output:

```json
[
  {
    "loc": [
      "calories"
    ],
    "msg": "value is not a valid integer",
    "type": "type_error.integer"
  }
]
```

Not only does Pydantic produce an error, but it gives us a nice error in JSON format that we can use how we see fit.

We can even add our own validators. Let's ensure that the description of our pies always contains the word "delicious", we don't want the pie in our database otherwise:

```python
from pydantic import BaseModel, constr, validator
from typing import List


class Pie(BaseModel):
    name: constr(max_length=200)
    description: str
    calories: int
    ingredients: List[str]

    @validator('description')
    def ensure_delicious(cls, v):
        if 'delicious' not in v:
            raise ValueError('We only accept delicious pies')
        return v
```

Now if we try to add our non-delicious pie, we get the following error:

```json
[
  {
    "loc": [
      "description"
    ],
    "msg": "We only accept delicious pies",
    "type": "value_error"
  },
]
```

## Pydantic + FastAPI

Now that we have a basic understand of what Pydantic can do, we should be able to understand the functionality it brings to our FastAPI apps!

The following working FastAPI app has an endpoint that takes POST data and creates an entry into a fake pie database - if the data is a valid `Pie` Pydantic model, of course. Save the following code as `app.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel, constr, validator
from typing import List
import uvicorn


class Pie(BaseModel):
    name: constr(max_length=200)
    description: str
    calories: int
    ingredients: List[str]

    @validator('description')
    def ensure_delicious(cls, v):
        if 'delicious' not in v:
            raise ValueError('We only accept delicious pies')
        return v


app = FastAPI()


def add_pie_to_database(pie: Pie) -> Pie:
    print(f'Adding {pie.name} to database!')
    return pie


@app.post('/pies/')
async def create_pie(pie: Pie):
    return add_pie_to_database(pie)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="info")
```

Our `Pie` model is used here unchanged. Now check out line 29 in `app.py`. The route function `create_pie` takes a single parameter: pie, of type `Pie`. This tells FastAPI that this route should receive data that looks like a `Pie`.


Make sure you have FastAPI, Uvicorn, and our favorite command-line HTTP client, [HTTPie](https://httpie.io/) installed:

    pip install fastapi uvicorn httpie

Now you should be able to run the server with:

    python app.py

Let's try adding a pie (and having it sent right back to us) using HTTPie:

```shell
$ http POST http://127.0.0.1:5000/pies/ \
  name=APIPie \
  description="A delicious pie, clean presentation but a messy filling." \
  calories=900 \
  ingredients:='["python", "pydantic", "FastAPI"]'
```
We should see the following response in our terminal:

```shell
HTTP/1.1 200 OK
content-length: 151
content-type: application/json
date: Thu, 24 Dec 2020 05:40:38 GMT
server: uvicorn

{
    "calories": 900,
    "description": "A delicious pie, clean presentation but a messy filling.",
    "ingredients": [
        "python",
        "pydantic",
        "FastAPI"
    ],
    "name": "APIPie"
}
```

And if we try to add a not delicious pie?

```shell
$ http POST http://127.0.0.1:5000/pies/ \
  name=MudPie \
  description="This is actually just made of mud." \
  calories=unknown \
  ingredients:='["dirt", "water", "bark"]'

HTTP/1.1 422 Unprocessable Entity
content-length: 195
content-type: application/json
date: Thu, 24 Dec 2020 05:49:42 GMT
server: uvicorn

{
    "detail": [
        {
            "loc": [
                "body",
                "description"
            ],
            "msg": "We only accept delicious pies",
            "type": "value_error"
        },
        {
            "loc": [
                "body",
                "calories"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```
As expected, we get an HTTP error with a nice description of exactly what was wrong with our request.

Pydantic also helps us when we want to send JSON representations of pies to our users. Let's add a method to get a fake Pie from our database and send it to the user:

```python {hl_lines=["33-48"]}
from fastapi import FastAPI
from pydantic import BaseModel, constr, validator
from typing import List
import uvicorn


class Pie(BaseModel):
    name: constr(max_length=200)
    description: str
    calories: int
    ingredients: List[str]

    @validator('description')
    def ensure_delicious(cls, v):
        if 'delicious' not in v:
            raise ValueError('We only accept delicious pies')
        return v


app = FastAPI()


def add_pie_to_database(pie: Pie) -> Pie:
    print(f'Adding {pie.name} to database!')
    return pie


@app.post('/pies/')
async def create_pie(pie: Pie):
    return add_pie_to_database(pie)


def get_pie_from_database() -> Pie:
    return Pie(
        name="ApiPie",
        description="A delicious pie, clean presentation but a messy filling.",
        calories=9000,
        ingredients=[
            "python",
            "pydantic",
            "FastAPI"
        ],
    )


@app.get('/pie/')
async def get_pie():
    return get_pie_from_database()

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="info")
```

Let's test the endpoint with a simple GET request:

    http http://127.0.0.1:5000/pie/


And the response should be what you expect, a JSON representation of the pie we created in `get_pie_from_database`.

## Conclusion

This was a simple introduction to Pydantic, but it should give you an idea of the functionality that Pydantic brings to FastAPI applications.

For additional information, check out the docs for [Pydantic](https://pydantic-docs.helpmanual.io) and some of the relevant sections of the [FastAPI docs](https://fastapi.tiangolo.com/tutorial/body/).
