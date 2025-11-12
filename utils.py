from shapely.geometry import shape,Polygon
from shapely import wkt


def isochrone_polygon_wkt(isochrone):
    """First polygon of isochrone to WKT."""
    ring = isochrone['features'][0]['geometry']['coordinates'][0]
    return Polygon(ring).wkt

def polygon_bbox_from_wkt(wkt_geom):
    """Return (minx, miny, maxx, maxy)."""
    geom = wkt.loads(wkt_geom)
    return list(geom.bounds)

def gdf_to_geojson(gdf):
    return gdf.__geo_interface__