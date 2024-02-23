---
title: Password-store (pass) extremely slow on OSX
date: 2019-05-01T00:54:26-07:00
categories:
    - code
---

[password-store](https://www.passwordstore.org) (installed via
homebrew) on OSX is very slow.

    Austins-MacBook% time pass testpass
    thisisatestpass
    pass testpass  0.55s user 0.25s system 83% cpu 0.969 total

Over half a second to print out a password. Pass is just a bash script. This would not do.

<!--more-->

After doing some sleuthing, it turns out it is [this line](https://git.zx2c4.com/password-store/tree/src/platform/darwin.sh#n46) in the platform specific code for OSX that is causing the problem:

{{< highlight shell >}}
GETOPT="$(brew --prefix gnu-getopt 2>/dev/null || { which port &>/dev/null && echo /opt/local; } || echo /usr/local)/bin/getopt"
{{< / highlight >}}

Every time pass is run on OSX, it first has to run homebrew to find out where gnu-getopt is installed.

It seems silly to default to such a heavy handed approach. It would make sense to first test a well known location (perhaps, the default location where homebrew installs gnu-getopt?) first, and then resort to the other methods after:

{{< highlight shell >}}
GETOPT="$({ [ -x /usr/local/opt/gnu-getopt ] && echo /usr/local/opt/gnu-getopt; } || brew --prefix gnu-getopt 2>/dev/null || { which port &>/dev/null && echo /opt/local; } || echo /usr/local)/bin/getopt"
{{< / highlight >}}

Using that method, things are improved considerably:

    Austins-MacBook% time pass testpass
    thisisatestpass
    pass testpass  0.02s user 0.01s system 19% cpu 0.177 total

There [have been patches](https://lists.zx2c4.com/pipermail/password-store/2018-October/003447.html) submitted upstream in the past for this issue, but none have been merged. So I [forked](https://github.com/Fingel/password-store) the upstream repo and applied the fix. You can install this version of pass using homebrew:

Uninstall pass if you already have it installed via brew:

    brew uninstall pass

Then "tap" the repo:

    brew tap Fingel/pass-osx

Finally, install the formula:

    brew install fingel/pass-osx/pass


Enjoy a properly fast pass. This should be helpful for anyone using pass on OSX, who doesn't mind installing their password manager via some random guy's fork on Github... 🤔



