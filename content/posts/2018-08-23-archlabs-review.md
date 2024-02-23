---
title: ArchLabs Linux Review (and tips)
date: 2018-08-23T11:02:12-07:00
categories:
    - linux
---

Today I'm writing a review of the [ArchLabs](https://archlabslinux.com/) linux
distro. Have you ever wanted a badass Arch linux install, complete with
an openbox window manager, conky, and dark gtk themes, worthy of the top
spot on [/r/unixporn](https://www.reddit.com/r/unixporn/top/?t=month)? Of 
course you do, but if you're anything like me, you're a busier person than you
were when you were 15, and you no longer have the time, or the inclination.

Enter ArchLabs, elite Arch Linux for the lazy:

[![Desktop](https://s3-us-west-2.amazonaws.com/pedaldp/images/2018-08-23-archlabs-review/desktop.png)](https://s3-us-west-2.amazonaws.com/pedaldp/images/2018-08-23-archlabs-review/desktop.png)

<!--more-->

## Installation

To start, the ArchLabs ISO is a bootable live environment, so you can test it 
out right away. You'll get a fairly minimal Openbox desktop, with a panel, 
conky, and some other goodies. Once you decide to install, because why wouldn't
you, the curses based installer will launch in a new terminal:

[![Installer](https://s3-us-west-2.amazonaws.com/pedaldp/images/2018-08-23-archlabs-review/installer2.png)](https://s3-us-west-2.amazonaws.com/pedaldp/images/2018-08-23-archlabs-review/installer2.png)

The installer is amazing, and way easier to use than many of the other fully
graphical ones I have used. I am seriously impressed with how simply and easily
it'll bootstrap a system for you, with plenty of options (including LuKS and 
LVM) but perfectly sane defaults. The entire install took about 5 minutes.

## First Boot

Once you boot into your system, you're greeted with a post-install script, 
which is also a delight to use:

[![Installer](https://s3-us-west-2.amazonaws.com/pedaldp/images/2018-08-23-archlabs-review/welcome.png)](https://s3-us-west-2.amazonaws.com/pedaldp/images/2018-08-23-archlabs-review/welcome.png)

This post-install script gives you the option to install additional desktop
environments, a login manager, nvidia drivers, and some other stuff. Super cool.

Once you're done with that, you're asked to reboot one more time (probably only
necessary if you've chosen to install a login manager or video drivers) and then
you're done, and using your new install.

## Fixes

While my first impressions of ArchLabs are that it's a very well put together
distro, there were still some things I needed to fix/tweak once I started
actually using it. Theses might come in handy for others, but hopefully they
quickly become irrelevant.

### Firefox text inputs are unreadable.

The dreaded dark gtk theme/Firefox combo. You'd thing we'd be past this by now,
but alas, not so. Luckily I found 
[this bug and comment](https://bugzilla.mozilla.org/show_bug.cgi?id=70315#c46)
which suggested adding `widget.content.gtk-theme-override` to `Adwaita:light`
in about:config (right click, new, add that key and value).

### Audacious can't play audio streams.

What am I to do without my [Defcon radio](https://somafm.com/defcon/)? 
This is just due to a missing package:

    $ aurman -S neon

### No shortcut for locking the screen!

ArchLabs provides a bunch of keyboard shortcuts for all sorts of stuff, but 
not activating the screen lock. How does that make any sense?

Edit `~./config/openbox/rc.xml` and add the following contents to the 
`<keyboard>` section (just place it next to another keybind):

    {{< highlight xml >}}
    <keybind key="W-l">
      <action name="Execute">
        <command>i3lock-fancy</command>
      </action>
    </keybind>
    {{< / highlight >}}

There is already a keybind for W-l, one of the many unmaximize ones, delete 
that one too. Now you can use super (windows key) + l to the lock the screen.

P.S. i3lock-fancy is really cool.

### No image viewer

There just isn't one included at all, oddly enough. Try feh:

    aurman -S feh

