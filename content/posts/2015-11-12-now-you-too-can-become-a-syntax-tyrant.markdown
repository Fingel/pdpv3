---
categories:
- code
date: 2015-11-12 18:40:39
title: Now You Too Can Become A Syntax Tyrant
---

So I really like code linters. My coworkers know this. Actually, I got called a
syntax Nazi today by a fellow developer. I'm OK with that. I believe in
readability and consistency.

In my projects I make it impossible to make a git commit before
the source code passes a [flake8](https://flake8.readthedocs.org/en/latest/)
check. How to perform this minor miracle you ask?
With a simple git pre-commit hook:

**myproject/.git/hooks/pre-commit**

    #!/bin/sh
    flake8 .

When I commit, the hook executes. Since git knows a return
of anything besides 0 means abort, it stops the commit
from happening. Awesome.

Here is a terminal recording of it in action:

<iframe src="http://showterm.io/61042144ecbe05b860067" width="600" height="380"></iframe>

Don't forget to make your pre-commit hook file executable!

<!--more-->
