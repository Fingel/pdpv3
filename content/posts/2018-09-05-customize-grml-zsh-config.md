---
title: Customizing grml-zsh-config
date: 2018-09-05T14:07:12-07:00
categories:
    - linux
---

Ever heard of [grml-zsh-config](https://grml.org/zsh/)? Maybe not, but it's
possible you may have used it. It's the zsh config for the Arch linux installer,
as well as some Debian systems.

Grml is a nice alternative to heavy and bloated config frameworks like oh-my-zsh
and pretzo (even on a modern machine I've seen zsh take over a second to load
using oh-my-zsh with just a few plugins enabled).

Unfortunately, grml is not that easy to configure, and the available documentation
is a little lacking. With a few tweaks though, I managed to get a proper shell out
of grml.

<!--more-->

Grml provides *almost* everything I'd like out of zsh by default. Here's the
out of the box prompt:

    {{< highlight shell >}}
    austin@nightmare ~/Documents/pdpv2 (git)-[master] %
    {{< / highlight >}}

Not bad, but room for improvement. Let's make some changes. All code below belongs
in your `.zshrc`

### Change the prompt layout.

There are a few items in the prompt that make it unnecessarily long and redundant.
I don't often forget who I am or where I'm at, so let's remove the `user@host`
nonsense. I also like my prompt to contain a newline, so input is consistently
placed on the far left.

    {{< highlight shell >}}
    zstyle ':prompt:grml:left:setup' items rc change-root path vcs newline percent
    {{< / highlight >}}

Now you'll end up with something like this:

    {{< highlight shell >}}
    ~/Documents/pdpv2 (git)-[master]
    %
    {{< / highlight >}}

### Better git information.

It'd be nice to see if there are any unstaged/staged changes in the current
working directory. While we're at it, let's get rid of the lame `(git)-` part of
the prompt. Nobody uses svn anymore, right?

Place this above the `zstyle ':prompt:grml:left:setup'` line in your .zshrc:

    {{< highlight shell >}}
    autoload -U colors && colors
    zstyle ':vcs_info:*' enable git
    zstyle ':vcs_info:*' check-for-changes true
    zstyle ':vcs_info:*' unstagedstr '!'
    zstyle ':vcs_info:*' stagedstr '+'
    zstyle ':vcs_info:git*' formats "%{${fg[cyan]}%}[%{${fg[blue]}%}%b%{${fg[yellow]}%}%m%u%c%{${fg[cyan]}%}]%{$reset_color%}"
    {{< / highlight >}}

This will load only git support, check for changes in the working directory and
add some icons to the prompt if there are changes. It also gets rid of the vcs
type display and adds some pretty colors. Your prompt should look something like
this now:

    {{< highlight shell >}}
    ~/Documents/pdpv2 [master!]
    %
    {{< / highlight >}}

### Add the current virtualenv.

Every self respecting python developer wants the currently activated virtualenv
to appear in their prompt. Due to the way grml configures itself virtualenv's normal
mechanism does not work. Here's how with grml. In your .zshrc:

    {{< highlight shell >}}
    source /usr/bin/virtualenvwrapper.sh
    function virtual_env_prompt () {
        REPLY=${VIRTUAL_ENV+(${VIRTUAL_ENV:t}) }
    }
    grml_theme_add_token virtual-env -f virtual_env_prompt '%F{magenta}' '%f'
    {{< / highlight >}}

Lastly, add the new virtual-env token to the layout:

    {{< highlight shell >}}
    zstyle ':prompt:grml:left:setup' items rc change-root path virtual-env vcs newline percent
    {{< / highlight >}}

You should end up with something like this if in the "testenv" virtualenv:

    {{< highlight shell >}}
    ~/Documents/pdpv2 (testenv) [master]
    %
    {{< / highlight >}}

### Check out the cheat sheet

Grml is a lot more than just a prompt. It adds a bunch of aliases and functions as
well. Check out the exhaustive [cheat
sheet](https://grml.org/zsh/grml-zsh-refcard.pdf) if you'd like to learn more.
Enjoy!

