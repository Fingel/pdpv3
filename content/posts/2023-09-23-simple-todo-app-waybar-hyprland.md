---
title: A minimal todo app for Waybar
date: 2023-09-23T09:03:44-07:00
categories:
    - linux
---

What is the simplest TODO app imaginable? In my opinion, it's just a text file
in your home directory named `todo.txt`. One line per item, edited with Vim. No
need for additional software, websites, or electron apps.

Using standard unix tools, this setup is easy to extend. In my case, I wanted a
persistent, nagging reminder of my constant procrastination. I also use
[waybar](https://github.com/Alexays/Waybar). Naturally then the end goal is a
custom module.

[![Image](https://pedaldp.s3-us-west-2.amazonaws.com/images/2023-09-23-waybar-todo/thumb-waybartodo.png)](https://pedaldp.s3-us-west-2.amazonaws.com/images/2023-09-23-waybar-todo/waybartodo.png)

Obviously, it displays the number of TODOs you have remaining. Additionally, hovering
over the module will print display them in a tooltip. When you click a new Neovim instance will spawn
opening the file.

Simple and effective. Here's the code. I placed this is `~/.config/waybar/scripts/todo.sh`:

```bash
#!/bin/bash
COUNT=$(wc -l < ~/todo.txt)
TODOS=$(cat ~/todo.txt | head -c -1 - | sed -z 's/\n/\\n/g')
printf '{"text": "%s", "tooltip": "%s"}\n' "$COUNT" "$TODOS"
```

And then add a custom module to `~/.config/waybar/config`:

```json
 "custom/todo": {
        "exec": "~/.config/waybar/scripts/todo.sh",
        "return-type": "json",
        "format": "{} todos",
        "on-click": "wezterm -e nvim ~/todo.txt",
        "interval": 5,
    }
```

Replace wezterm with your preferred terminal emulator and you should be good to go!

<!--more-->
