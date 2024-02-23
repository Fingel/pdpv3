---
title: "Location Based Search for FastAPI" # Title of the blog post.
date: 2020-12-28T21:57:08-08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: true # Sets whether to render this page. Draft of true will not be rendered.
toc: true # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
featureImage: "/images/locationbasedsearch.jpg" # Sets featured image on blog post.
thumbnail: "/images/locationbasedsearchthumb.jpg" # Sets thumbnail image appearing inside card on homepage.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.
categories:
  - Tutorial 
tags:
  - FastAPI
  - GIS
# comment: false # Disable comment if false.
---
Are you interested in adding geographical capabilities to your app? Perhaps you want to be able to search for nearby items on your site. Or maybe you want to know if your user's location is within a specific region. With a few tools it is easy to add GIS (Geographical Information Systems) to your FastAPI back end.

## Geometric Types and WKT (Well Known Text)

Programmers are used to data types like integers, strings and the like. But if we want to represent a location, shape, or line, how do we do that? Not only do we need to represent these types, we need to do it in a way that is interoperable with other tools.

One way to represent geometric types is by using [Well Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format. Also known as WKT, this format provides an easy to read representation of geometries with widespread support, especially in open source tools. Here is how various geometries are represented in WKT:

![Well Know Text Formats from Wikipedia](/images/2020-12-28-location-based-search-fastapi/wkt.png)

As we can see, a `POINT` is represented simply by an X and Y coordinate. A `LINESTRING` is just a list of `POINT`s, a `POLYGON` is a special `LINESTRING` that starts and end at the same `POINT`. Multiple `POLYGON`s can be combined in a list (sometimes called a `MULTI-POLYGON`) to create complex shapes.

### Geometry vs Geography

A geometry is a point, shape or line that exists on the Cartesian plane. The X and Y coordinates that make up a `POINT` are unit-less. But once we need to represent `POINT`s on earth (like locations) or `LINESTRING`s (like roads) we need to use Geography.

Geographies are represented exactly the same in WKT, but can be treated differently by the software working with them. Typically, a Geography `POINT` uses longitude and latitude for X and Y, and these axis are limited to -90/90 degrees north, and 360 degrees east, respectively. Also calculations using geographies should be done on the surface of a sphere (defined by the [SRID](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) or [UTM](https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system)) instead of a flat plane.

The details here are not important. Just remember that if you are working with data that is meant to represent locations or earth (or space), which you probably are, you'll want to use Geographies. Usually this just means using "Geography" instead of "Geometry" when typing out your queries and definitions.

## PostGIS and Spatialite

Most databases need some kind of extension to work with Geometric data types. For Postgres, there is [PostGIS](https://postgis.net). For Sqlite3, we have [Spatialite](https://www.gaia-gis.it/fossil/libspatialite/index).

## Geoalchemy2

## Models and Queries




