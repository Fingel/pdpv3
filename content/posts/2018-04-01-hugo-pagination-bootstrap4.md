---
title: Hugo Pagination Partial for Bootstrap4
date: 2018-04-01T11:02:12-07:00
categories:
    - code
---

Hugo's [internal template for pagination](https://github.com/gohugoio/hugo/blob/master/tpl/tplimpl/template_embedded.go#L125) claims it works with Bootstrap styles. That
may have been the case for Bootstrap3, but now that 4 is out, it requires a few
more classes.

<!--more-->

Below is a template that can be used as a partial in your theme based on Hugo's
internal template with additional Bootstrap4 classes. You can see it in action
on this blog's [front page](http://www.pedaldrivenprogramming.com).

{{< highlight go-html-template >}}
{{ $pag := $.Paginator }}
{{ if gt $pag.TotalPages 1 }}
<ul class="pagination">
    {{ with $pag.First }}
    <li class="page-item">
        <span class="page-link">
            <a href="{{ .URL }}" aria-label="First"><span aria-hidden="true">&laquo;&laquo;</span></a>
        </span>
    </li>
    {{ end }}
    <li class="page-item {{ if not $pag.HasPrev }}disabled{{ end }}">
        <span class="page-link">
            <a href="{{ if $pag.HasPrev }}{{ $pag.Prev.URL }}{{ end }}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a>
        </span>
    </li>
    {{ $.Scratch.Set "__paginator.ellipsed" false }}
    {{ range $pag.Pagers }}
    {{ $right := sub .TotalPages .PageNumber }}
    {{ $showNumber := or (le .PageNumber 3) (eq $right 0) }}
    {{ $showNumber := or $showNumber (and (gt .PageNumber (sub $pag.PageNumber 2)) (lt .PageNumber (add $pag.PageNumber 2)))  }}
    {{ if $showNumber }}
        {{ $.Scratch.Set "__paginator.ellipsed" false }}
        {{ $.Scratch.Set "__paginator.shouldEllipse" false }}
    {{ else }}
        {{ $.Scratch.Set "__paginator.shouldEllipse" (not ($.Scratch.Get "__paginator.ellipsed") ) }}
        {{ $.Scratch.Set "__paginator.ellipsed" true }}
    {{ end }}
    {{ if $showNumber }}
    <li class="page-item {{ if eq . $pag }}active{{ end }}">
        <span class="page-link">
            <a href="{{ .URL }}">{{ .PageNumber }}</a></li>
        </span>
    {{ else if ($.Scratch.Get "__paginator.shouldEllipse") }}
    <li class="page-item disabled"><span class="page-link" aria-hidden="true">&hellip;</span></li>
    {{ end }}
    {{ end }}
    <li class="page-item {{ if not $pag.HasNext }}disabled{{ end }}">
        <span class="page-link">
            <a href="{{ if $pag.HasNext }}{{ $pag.Next.URL }}{{ end }}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a>
        </span>
    </li>
    {{ with $pag.Last }}
    <li class="page-item">
        <span class="page-link">
        <a href="{{ .URL }}" aria-label="Last"><span aria-hidden="true">&raquo;&raquo;</span></a>
    </span>
    </li>
    {{ end }}
</ul>
{{ end }}
{{< / highlight >}}
