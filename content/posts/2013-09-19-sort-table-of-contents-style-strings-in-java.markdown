---
categories:
- code
date: 2013-09-19 00:00:00
title: Sort Table of Contents Style Strings In Java
type: post
---

This is for when you have String likes "1.1", "1.2"..."1.10" such that
you want "1.10" &gt; "1.1". Just another example of terrible code programmers
have to write when people insist on presenting data in illogical ways.

{{< highlight java >}}
private static class TocComparator implements Comparator&lt;String&gt;{
    public int compare(String s1, String s2){
        Integer s1front = Integer.parseInt(s1.substring(0, s1.indexOf('.')));
        Integer s2front = Integer.parseInt(s2.substring(0, s2.indexOf('.')));
        if(s1front.equals(s2front)){
            Integer f1ass = Integer.parseInt(s1.substring(s1.indexOf('.')+1));
            Integer f2ass = Integer.parseInt(s2.substring(s2.indexOf('.')+1));
            return f1ass.compareTo(f2ass);
        }
        else{
            return s1front.compareTo(s2front);
        }
    }
}
{{< / highlight >}}
This class is a comparator which can be used with `Collections.sort()`