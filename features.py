import openrouteservice as ors
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon

def get_isochrone_time(x,y,time_minutes):
    coordinates=[x,y]
    client = ors.Client(key='')

    iso = client.isochrones(
        locations=[coordinates],
        profile='driving-car',
        range=[time_minutes*60],
        validate=False,
        attributes=['total_pop']
    )
    return iso

def get_addresses_from_osm_for_isochrone(isochrone):
    coords=isochrone['features'][0]['geometry']['coordinates']
    list_of_tuples = [tuple(x) for x in coords[0]]
    polygon = Polygon(list_of_tuples)

    # Define OSM tags for addresses
    tags = {"addr:housenumber": True}
    gdf = ox.features_from_polygon(polygon, tags)
    gdf_points = gdf[gdf.geom_type == "Point"]
    return gdf_points
def gdf_to_geojson(gdf):
    return gdf.__geo_interface__

def subsample_addresses(address_gdf,sample_size):
    return address_gdf.sample(sample_size)

def get_route(waypoints):
    client = ors.Client(key='5b3ce3597851110001cf62482290956be2f54a82b10ada04533d7344') # Specify your personal API key
    coords=tuple((p.x,p.y) for p in waypoints['geometry'].to_list())
    routes = client.directions(coords, profile='driving-car', optimize_waypoints=True)
    geometry = routes['routes'][0]['geometry']
    decoded = ors.convert.decode_polyline(geometry)
    return decoded