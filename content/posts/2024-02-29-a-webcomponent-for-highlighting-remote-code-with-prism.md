---
categories:
    - code
date: 2024-02-28 19:41:00.160485-08:00
title: A Web Component for Highlighting Remote Code with Prism
---

I was playing around with Web Components and thought it would be neat to be able to
display code snippets, but instead of static text load the content from a remote source.
For example, displaying the source code for a file hosted on Github inline in a blog post.
Thus [prism-remote](https://github.com/Fingel/prism-remote) was born.

<!--more-->
<link href="https://unpkg.com/prismjs@v1.x/themes/prism-twilight.min.css" rel="stylesheet" />
<script src="https://unpkg.com/prismjs@v1.x/components/prism-core.min.js"></script>
<script src="https://unpkg.com/prismjs@v1.x/plugins/autoloader/prism-autoloader.min.js"></script>
<script
    src="https://unpkg.com/prism-remote@latest/prism-remote.js"
    type="module"
></script>

For example: To highlight lines 1 through 20 of
https://github.com/Fingel/prism-remote/blob/main/prism-remote.js using the `<prism-remote>`
custom element:

```html
<prism-remote
    src="https://github.com/Fingel/prism-remote/blob/main/prism-remote.js"
    start="1"
    end="20"
    lang="javascript"
>
</prism-remote>
```

Results in:

<prism-remote
src="https://github.com/Fingel/prism-remote/blob/main/prism-remote.js"
start="1"
end="20"
lang="javascript">
</prism-remote>

While I think the Webcomponent API leaves a little to be desired, there are clearly neat
use cases like this where they can be very useful.
