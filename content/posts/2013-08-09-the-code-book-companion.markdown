---
categories:
- code
- featured
date: 2013-08-09 00:00:00
featured_image: codebook.png
title: The Code Book Companion
---

<img class="alignleft" src="https://s3-us-west-2.amazonaws.com/pedaldp/uploads/2013/08/codebook-195x300.jpg" width="195" height="300" />I've been on a cryptology kick recently, which is really no surprise. With all the recent news about <a href="http://www.theguardian.com/world/2013/aug/09/nsa-loophole-warrantless-searches-email-calls">domestic surveillance</a> and services providing private communication being <a href="http://rt.com/usa/lavabit-email-snowden-statement-247/">forcefully shut down</a>, I have to admit my sympathy for the foil hats has increased considerably.

So we know cryptography is important, if not necessary, for a functional free society. But it's also really 'effin cool.  The world of cryptography is an even mix of mathematics, information science, and civil disobedience. What's not to love?

Nothing I have read has done a better job of covering this subject that Simon Singh's <a href="http://simonsingh.net/books/the-code-book/">The Code Book</a>. Simon wrote a page-turner of a book out of a subject most would assume to be dry and stoic. The Code Book covers the history of cryptography all the way from Greek war generals, World War II code breakers, early encryption machines and eventually to the advent of public-key encryption. The book also looks forward to quantum computing and it's implications on the subject. Although published in 1999, the book remains extremely relevant. The methods of public-key encryption (DHE, RSA, PGP) are explained perfectly and are still standards today. The only time the book shows it's age is the lack of a mention of <a href="https://en.wikipedia.org/wiki/Elliptic_curve_cryptography">Elliptic Curve Cryptography </a>which was proposed in 1985 but is just now gaining popularity as an alternative approach to public-key cryptography.

As with most technical leaning books, I felt that sometimes the Code Book was too easy to read without <em>really </em>understanding the subjects described. Indeed, Simon does such a good job of portraying the human aspect of cryptography that often I just wanted to know what would happen next to whichever mathematician/social dissident/treasure hunter was currently the subject. So I decided to slow myself down.

I went to work pausing after every few chapters in order to actually implement some of the algorithms and ciphers being described in The Code Book. The result is <a href="http://toxiccode.com/codebook/">this small website </a>where I placed them for anyone who is interested. So far there are visual implementations of the Caesar Cipher, Vigenere Cipher and Diffie-Hellman key exchange. There is also a tool to perform frequency analysis on two texts and compare the results.

Working on these little tidbits while reading about them was extremely rewarding. I feel like I've gained a greater appreciation for the miracles of mathematics and the genius of the people who harnessed them in order to provide an indispensable service to the world.

I've finished the book now, but I plan on writing more implementations. Possibly RSA? A version of Diffie-Hellman using elliptic curve cryptography? We'll see.

<a href="http://toxiccode.com/codebook/">www.toxiccode.com/codebook</a>

The code for the page is <a href="https://github.com/AustinRiba/thecodebookcompanion">available on Github.</a>