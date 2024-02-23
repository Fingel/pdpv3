---
categories:
- code
date: 2013-09-30 11:46:28
title: Goodbye Wordpress
---

For the past 6 years this blog has been running off
the same Wordpress install on a 1&1 shared hosting account without
interruption. It was a good run, and speaks to how well Wordpress upgrades
work.

But a Wordpress install is just so _uncool_. I decided to hop on the
[Jeykll](http://jekyllrb.com) train. This blog is now 100% static, which
is pretty refreshing after years of dealing a massive PHP application.
It doesn't even require a database and it allows me to tweak to my heart's
content. Wordpress always seemed like a bit of a black box. Sure, the code
was there, but it was daunting to even think about touching it.

<!--more-->

Certain things become more complicated with Jekyll, since by default pretty
much everything is done manaully. The most trivial being just creatig a post.
Manually you will have to create the file, name it correctly, and then
upload images, and link to them. Not a great workflow if you just want to write
a quick post. So I created a rakefile that takes care of some of these tasks
for me. The real timesaver is creating a folder in _images/ for each post,
and then syncing them with s3 with the s3sync task:

{{< highlight ruby >}}

desc 'create new post. args: title, category'
# rake new title="New post title goes here" category="category"
task :new do
  require 'rubygems'
  title = ENV["title"] || "New Title"
  category = ENV["category"] || "other"
  slug = title.gsub(' ','-').downcase

  TARGET_DIR = "_posts"

  filename = "#{Time.new.strftime('%Y-%m-%d')}-#{slug}.markdown"
  image_dir ="_images/#{Time.new.strftime('%Y-%m')}-#{slug}"
  path = File.join(TARGET_DIR, filename)
  post = <<-HTML
  ---
  layout: post
  title: TITLE
  date: DATE
  categories: CATEGORY
  ---
  <!--- {{site.image_url}}/{{page.id | replace: '/','-' | remove_first: '-'}}/image.jpg -->

  HTML
  post.gsub!('TITLE', title).gsub!('DATE', Time.new.to_s).gsub!('CATEGORY', category)
  File.open(path, 'w') do |file|
    file.puts post
  end
  puts "new post generated in #{path}"
  system "mkdir #{image_dir}"
  system "geany #{path}"
end

task :s3sync do
  system "s3cmd sync _images/ s3://pedaldp/images/ -P"
end

{{< / highlight >}}

This post was written in a text editor. It will be published to my vps
with a `git push deploy master`. _Cool_.