---
title: Line by Line Simple but Usable VIM Config
date: 2018-03-23T13:08:09-07:00
categories:
    - code
---

VIM is a great editor, but it's defaults are a little lacking. Fortunately
it's also extremely configurable. This leads many people (myself included),
to scour the internet for lines of internet wisdom to copy in paste into
their `.vimrc` files until they get something that works for them. Before
you know it you have 300 lines of unintelligible gobblegook. In this post,
(which I've started writing in vanilla vim) I'm going to go line by line
through individual config items to construct a simple but usable `.vimrc`
without too much magic or frills.

<!--more-->

You can download the `.vimrc` in full [as a github gist](https://gist.github.com/Fingel/9fdbe9b2d271421f894d06c8418264e6)

### Tabs vs. Spaces
I'm a spaces guy, so let's make vim use spaces instead of tabs. While we're at it
we should make tabs use 4 spaces by default (since I'm also a python guy)

{{< highlight vimrc >}}
set expandtab 		" tabs are spaces
set shiftwidth=4	" size of indents in spaces
set softtabstop=4	" simulate tabs with this many spaces
{{< / highlight >}}

It's possible to change the indent level for different filetypes:

{{< highlight vimrc >}}
" FileType specific tab overrides
filetype plugin indent on " Enable filetype detection and <filetype>.vim loading
autocmd FileType html setlocal shiftwidth=2 tabstop=2
autocmd FileType javascript setlocal shiftwidth=2 tabstop=2
autocmd FileType vue setlocal shiftwidth=2 tabstop=2
autocmd FileType htmldjango setlocal shiftwidth=2 tabstop=2
{{< / highlight >}}

### Line numbers
It's nice to have line numbers, so let's turn those on. Once you do this it get's
annoying to select text with the mouse, though. So let's also enable mouse in auto
mode so that vim doesn't select line numbers (and goes into visual mode).

{{< highlight vimrc >}}
" Line numbers and mouse
set number      " enable line numbers
set mouse=a     " enable mouse in auto mode
{{< / highlight >}}

### Searching
Searching in vim by default is pretty good but there are a few options to make it
even better.

{{< highlight vimrc >}}
" Searching
set incsearch   " don't wait for the enter key to start searching
set hlsearch    " highlight search results
{{< / highlight >}}

### Syntax highlighting and themes
It'd be nice to have some pretty syntax highlighting, so we'll enable it and
also set a nicer theme than default.

{{< highlight vimrc >}}
" Syntax and colors
syntax enable       " turn on syntax highlighting
colorscheme slate   " use the slate theme
{{< / highlight >}}


### Tabs
You can navigate tabs in vim using gT and gt to move backwards and forwards,
respectively. But what about navigating to the previously used tab? I'll
admit, what follows is still magic to me.

{{< highlight vimrc >}}
" Map gl to the previously used tab
let g:lasttab = 1
nmap gl :exe "tabn ".g:lasttab<CR>
au TabLeave * let g:lasttab = tabpagenr()
{{< / highlight >}}

### Trimming trailing whitespace
If you're editor doesn't trim trailing whitespace and you work with other
people using version control, shame on you. The following command will
trim trailing whitespace from all lines in a file. Additionally, we will
call it every time we save the file.

{{< highlight vimrc >}}
" Strip trailing whitespace
fun! TrimWhitespace()
    let l:save = winsaveview()
    %s/\s\+$//e
    call winrestview(l:save)
endfun

autocmd BufWritePre * :call TrimWhitespace() " Call TrimWhitespace on save
{{< / highlight >}}

### Miscellaneous
Theses are settings I find useful, but don't fit in any other category

{{< highlight vimrc >}}
" Misc
set wildmenu    " show tab completions for commands inline

" Files to ignore for various auto completion commands
set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*.pyc,__pycache__,node_modules

" Remap the dd shortcut to not nuke whatever was in the yank buffer
nnoremap d "_d
vnoremap d "_d
{{< / highlight >}}

### Going further
That concludes all the settings I feel make vim a useful _text editor_. If you want to use
vim as a full fledged IDE, there are hundreds of extra settings and plugins to choose from.
In my old age, I much prefer simplicity. If I need a fully fledged IDE, I'll reach for
something like sublime text instead.
