---
categories:
- cartography
- code
- granitemaps
date: 2015-01-11 17:35:08
title: Creating nice looking topo maps for use in GraniteMaps
---

The goal of [GraniteMaps](http://granitemaps.com "GraniteMaps") is to provide accurate and educational maps for
people participating in outdoor activities, so a large part of the project is creating maps that are pleasing to the eye.

The map displayed in granitemaps is actually two layers: the "base map" and the trail layer. The base map is
is responsible for displaying the details of the map's area such as land boundaries, rivers/lakes, major roads
and elevation. The trail layer is an overlay of the actual trails and points of interest.

<!--more-->

Currently GraniteMaps uses [The National Map](http://viewer.nationalmap.gov/viewer/) provided by the USGS for the base layer. It's a good
public domain map that includes major roads, hillshading, contour lines and place names. It does have it's issues, however:

1. The map is rendered without anti-aliasing which means fonts look jagged. The rest of the render just
looks dated, like 90's jpeg compression was used.
2. Many of the minor roads are rendered it too low a resolution. This means that many of the "lesser used"
roads, i.e the roads we care about in GraniteMaps, are rendered without enough data points. This causes roads
to cut across contour lines, have harsh angles, and in general just not appear where they are supposed to.
3. Not customizable. The map is provided in JPG format which you can use in slippy maps, but what you see is
what you get.

For these reasons (especially #2) I concluded that The National Map would not be satisfactory for use in GraniteMaps' next map.

The solution is to create a custom base layer for use in GraniteMaps. After a few days of getting familiarized with the GIS landscape,
I set to work on creating a nice looking map using MapBox's [TileMill](https://github.com/mapbox/tilemill). A good starting point was
the [osm-bright](https://github.com/mapbox/osm-bright) project which pulls openstreetmap data from your local PostGIS database to
create a fully featured street map. Elevation data is a must have, so after following [this great article](http://stevebennett.me/tag/contours/)
by Steve Bennett I loaded some data from the [Shuttle Radar Topography Mission](http://srtm.csi.cgiar.org/index.asp) into the map to provide
contours and hillshading. After that is was a matter of tweaking the [CartoCSS](https://www.mapbox.com/tilemill/docs/manual/carto/) rules to
get the desired look right. The preliminary result:

<img class="import-img" src="http://s3-us-west-2.amazonaws.com/pedaldp/images/2015-01-creating-nice-looking-topo-maps-for-use-in--granitemaps/topopreview.png" alt="2015-01-11-creating-nice-looking-topo-maps-for-use-in--granitemaps.markdown">

The rendering isn't perfect, but it's a good start and already superior to The National Map. In case anyone else is interested in creating their own
topo map in a similar fashion, the style files are [available on github!](https://github.com/Fingel/granitemaps-basemap/)

Keep enjoying these beautiful winter months out on the trail!