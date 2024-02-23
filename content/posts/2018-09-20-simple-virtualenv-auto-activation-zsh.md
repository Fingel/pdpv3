---
title: Simple Virtualenv Auto Activation With ZSH.
date: 2018-09-20T20:46:24-07:00
categories:
    - linux
---

Since I moved from fish to zsh, one of the main things I missed was
[virtualfish](https://virtualfish.readthedocs.io/en/latest/). I'm not sure how any
serious python developer lives without auto activation, as in automatically
activating the virtualenv for your project when you open a terminal or cd to it.

Here is a script you can use to achieve auto activation. It doesn't require
virtualenvwrapper, pyenv, or anything like that. Just use python3's built in
`python -m venv` to create a virtualenv in `~/.virtualenvs/`, use the provived
`venvconnect` function to connect the activated env with the current directory,
and you're done.

```zsh
#!/bin/zsh
#
# Auto activate a python virtualenv when entering the project directory.
# Installation:
#   source virtualenv-auto-activate.sh
#
# Usage:
#   Function `venvconnect`:
#       Connect the currently activated virtualenv to the current directory.
#
VENV_HOME=$HOME/.virtualenvs

function _virtualenv_auto_activate() {
    if [[ -f ".venv" ]]; then
        _VENV_PATH=$VENV_HOME/$(cat .venv)

        # Check to see if already activated to avoid redundant activating
        if [[ "$VIRTUAL_ENV" != $_VENV_PATH ]]; then
            source $_VENV_PATH/bin/activate
        fi
    fi
}

function venvconnect (){
    if [[ -n $VIRTUAL_ENV ]]; then
        echo $(basename $VIRTUAL_ENV) > .venv
    else
        echo "Activate a virtualenv first"
    fi
}

chpwd_functions+=(_virtualenv_auto_activate)
precmd_functions=(_virtualenv_auto_activate $precmd_functions)
```

Source the above script in your `~/.zshrc` and you should get auto activation of
python virtualenvs.
<!--more-->
