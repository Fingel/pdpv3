---
title: Be Careful with Object.assign in Javascript
date: 2020-08-23T21:20:36-07:00
categories:
    - code
    - javascript
---

[Immutability is
important](https://reactjs.org/tutorial/tutorial.html#why-immutability-is-important)
say the React docs. And of course this is correct, especially in the context of
React, Vue.js and the like that depend on immutability to work correctly. It's
also a core facet of functional programming which is becoming more and more
popular by the hour. But can you over do it?

<!--more-->

## Object.assign for the win?

One of the most popular tools for writing immutable code in Javascript is
[Object.assign()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign).

Instead of mutating an object:

```javascript
x = { baz: 'boo'}
x.foo = 'bar'
// x is now:
{foo: 'bar', baz: 'boo'}
```

We can use `Object.assign` to create a new object as a copy of an existing
object but with new values(s):

```javascript
x = { baz: 'boo'}
y = Object.assign({}, {foo: 'bar'}, x)
//y is now:
{foo: 'bar', baz: 'boo'}
//x is still:
{ baz: 'boo'}
```

So why not just use `Object.assign` or the [spread
operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)
all the time thus removing mutability, side effects, and all that stuff that
functional programming teaches us is bad? Well, because performance can be
abysmal.

Take the following test suite using [benchmark.js](https://benchmarkjs.com):

```javascript
var Benchmark = require('benchmark')

const suite = new Benchmark.Suite;

const obj = { foo: 1, bar: 2 };
let mutObj = { foo: 1, bar: 2};

suite.
  add('Object spread', function() {
    ({ baz: 3, ...obj});
  }).
  add('Object.assign()', function() {
    Object.assign({}, { baz: 3 }, obj);
  }).
  add('Mutation', function() {
    mutObj.baz = 3
  }).
  on('cycle', function(event) {
    console.log(String(event.target));
  }).
  on('complete', function() {
    console.log('Fastest is ' + this.filter('fastest').map('name'));
  }).
  run();
```

The results are telling:

Object spread x **18,041,542** ops/sec ±0.81% (85 runs sampled)\
Object.assign() x **12,785,551** ops/sec ±0.87% (89 runs sampled)\
Mutation x **780,033,935** ops/sec ±1.86% (84 runs sampled)\
Fastest is Mutation

We can see here that mutating an object is 65x faster than using `Object.assign`.
Which makes sense because `Object.assign` is creating an entire new object.

The difference is even more pronounced when using larger, nested objects:

```javascript
const obj = {
  foo: 1,
  bar: 2,
  lorem: 'ipsum, dolor, amet...',
  nested: {
    bird: 'yes',
    mammal: 'no',
    platypus: 'maybe',
  }
}
```

Object spread x **7,612,732** ops/sec ±1.14% (85 runs sampled)\
Object.assign() x **7,264,250** ops/sec ±1.16% (87 runs sampled)\
Mutation x **769,863,543** ops/sec ±1.50% (82 runs sampled)\
Fastest is Mutation

Again, it makes intuitive sense that using `Object.assign` would be slower.

So is it a big deal? Probably not, as you'll usually be using these slower,
immutable patterns to work with React/Vue data in which the performance impact is
not only negligible but necessary.

## A real world example

I was recently asked to take a look at some very poorly performing pages in a
Vue.js app. When I took a look I found some code that looked like this:

```javascript
trackpoints[i] = new Object()
track.trackpoints.forEach(t => {
    const temp = trackpoints[i]
    const key = someFunction(t)
    trackpoints[i] = Object.assign({}, temp, {
        [key]: [t.foo, t.bar, t.baz]
    })
})
return trackpoints
```

Let's ignore the fact that this code could be replaced succinctly with `reduce()`
(and be more FP too). The problem is that `track.trackpoints` consists of 10s to
100s of thousands of objects. While the above code is technically immutable, it is
also creating a new Object per loop. Once the usage of Object.assign() was
removed, the performance issues went away.

To me this is a good lesson of why it's not a good idea to be too dogmatic in
programming. Programming languages are just tools to do a job and to a certain
extent the way you write your code is as well.
