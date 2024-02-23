---
categories:
- code
date: 2014-10-06 11:46:59
title: Making ng-grid scroll and select naturally with arrow keys
---

The default behaviour of angular's [ng-grid](http://angular-ui.github.io/ng-grid/) library while using multiselect is a little strange.
By default using the arrow keys will select multiple rows. I was looking for behaviour that would only select rows if ctrl or shift were being held.
ng-grid also seems to have [an issue](https://github.com/angular-ui/ng-grid/issues/1275) with not showing the currently selected row in the viewport, causing the table not to scroll properly. The following code placed in your `gridOptions` object addresses both issues:

<!--more-->

{{< highlight javascript >}}
beforeSelectionChange: function(rowItem, event){
    if(!event.ctrlKey && !event.shiftKey && event.type != 'click'){
      var grid = $scope.gridOptions.ngGrid;
      grid.$viewport.scrollTop(rowItem.offsetTop - (grid.config.rowHeight * 2));
      angular.forEach($scope.myData, function(data, index){
        $scope.gridOptions.selectRow(index, false);
      });
    }
    return true;
},
{{< / highlight >}}

Here is a plunker demonstrating how the table behaves:

<iframe width="500" height="420" frameborder="0" src="http://embed.plnkr.co/xsY6W9u7meZsTJn4p1to/preview"></iframe>

Happy coding.