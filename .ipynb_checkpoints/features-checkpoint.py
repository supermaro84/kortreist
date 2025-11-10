import openrouteservice as ors
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

def get_isochrone_time(x,y,time_minutes):
    coordinates=[x,y]
    client = ors.Client(key=api_key)

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

def coordinates_to_geojson_with_labels(coordinates):
    """Convert list of coordinates to GeoJSON with index labels"""
    features = []
    
    for i, coord in enumerate(coordinates):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": coord  # [lon, lat] format for GeoJSON
            },
            "properties": {
                "label": f"{i+1}",
                "index": i,
                "coordinates": f"{coord[1]:.5f}, {coord[0]:.5f}"  # lat, lon for display
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson


def get_route(waypoints):
    client = ors.Client(key=api_key)
    if 'MULTIPOINT' in str(next(iter(waypoints['geometry']))):
        coords = tuple((mp.geoms[0].x, mp.geoms[0].y) for mp in waypoints['geometry'].to_list())
    else:
        coords=tuple((p.x,p.y) for p in waypoints['geometry'].to_list())

    routes = client.directions(coords, profile='driving-car', optimize_waypoints=True)
    geometry = routes['routes'][0]['geometry']
    decoded = ors.convert.decode_polyline(geometry)
    stops=routes['routes'][0]['way_points']
    stops_coordinates=[decoded['coordinates'][s]for s in stops ]
    return decoded,stops_coordinates,routes['routes'][0]['summary']