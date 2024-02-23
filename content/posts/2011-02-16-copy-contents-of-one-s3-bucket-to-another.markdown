---
categories:
- code
date: 2011-02-16 00:00:00
title: Copy Contents of one S3 Bucket to Another.
type: post
---

Need to automate copying files from one Amazon S3 bucket to another? So did I. Everything I found on google, <a href="http://snippets.dzone.com/posts/show/4935">like this,</a> was useless. Most of the scripts I found required downloading the objects first to the local machine and then reuploading them to the destination bucket. Unacceptable, especially if you are dealing with a large and or many files.

I've never written a line of Ruby before, but it seems like there are some great AWS libraries for it, so I decided to give it a shot. There is a cool library out there called<a href="http://rubyforge.org/projects/rightscale"> right_aws</a>. You can install it using `#gem install right_aws`. Then simply copy this script:
{{< highlight ruby >}}
#!/usr/bin/env ruby
require 'right_aws'

        S3ID = "Your AWS ID Here"
        S3KEY = "Your AWS secret key"
        SRCBUCKET = "Source Bucket"
        DESTBUCKET = "Destination Bucket"

        s3 = RightAws::S3Interface.new(S3ID, S3KEY)
        objects = s3.list_bucket(SRCBUCKET)
        objects.each do |o|
        puts("Copying " +  o[:key])
        s3.copy(SRCBUCKET, o[:key], DESTBUCKET, o[:key])
        end
        puts("Done.")
{{< / highlight >}}
Make sure the file is executable and you should be able to run it via command line on any unix system. To make a generic ruby script get rid of the first line.

I know its pretty brutish, probably sucks in more ways than one, but for now it works. And I think I like Ruby :D