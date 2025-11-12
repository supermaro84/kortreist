import dataclasses
import geopandas as gpd
import pandas as pd
import requests
import features 
import utils
from shapely import wkt



def get_collections_geoserver(url, collections_endpoint) -> pd.DataFrame:
    response = requests.get(f"{url}/{collections_endpoint}")
    response.raise_for_status()

    data = response.json()
    return pd.DataFrame(data['collections'])
@dataclasses.dataclass
class Geoserver:
    url: str
    collections_endpoint: str

def get_unique_values_from_geoserver_collection(geoserver: Geoserver, collection_name: str, property_name: str) -> list:
    response = requests.get(f"{geoserver.url}/{geoserver.collections_endpoint}/{collection_name}/items?properties=tettstednavn")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data['features'])
    if 'properties' in df.columns:
        properties_df = pd.json_normalize(df['properties'])
        unique_values = properties_df[property_name].unique().tolist()
        return unique_values
    else:
        raise ValueError("No properties found in the features.")
def get_features_by_attribute_value(geoserver: Geoserver, collection_name: str, attribute_name: str, attribute_value: str) -> gpd.GeoDataFrame:
    response = requests.get(f"{geoserver.url}/{geoserver.collections_endpoint}/{collection_name}/items?filter={attribute_name}='{attribute_value}'")
    response.raise_for_status()
    data = response.json()
    gdf = gpd.GeoDataFrame.from_features(data['features'])
    return gdf

def get_features_by_polygon(geoserver: Geoserver, collection_name: str, wkt_geom) -> gpd.GeoDataFrame:
    bbox=utils.polygon_bbox_from_wkt(wkt_geom)
    response = requests.get(f"{geoserver.url}/{geoserver.collections_endpoint}/{collection_name}/items?bbox={bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}")
    response.raise_for_status()
    data = response.json()
    gdf = gpd.GeoDataFrame.from_features(data['features'])
    wkt_geom_obj = wkt.loads(wkt_geom)
    gdf = gdf[gdf.geometry.within(wkt_geom_obj)]
    return gdf

