import dataclasses
import geopandas as gpd
import pandas as pd
import requests


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

def get_features_by_polygon(geoserver: Geoserver, collection_name: str, polygon_wkt: str) -> gpd.GeoDataFrame:
    response = requests.get(f"{geoserver.url}/{geoserver.collections_endpoint}/{collection_name}/items?filter=INTERSECTS(geometry, {polygon_wkt})")
    response.raise_for_status()
    data = response.json()
    gdf = gpd.GeoDataFrame.from_features(data['features'])
    return gdf

def main():
    geoserver = Geoserver(
        url="https://geoserver-4vzmi.ondigitalocean.app/geoserver",
        collections_endpoint="ogc/features/v1/collections")
    adresses = "kortreist:addresser_leilighet"
    tettsteder_aggr = "kortreist:tettsteder2025_aggr"
    tettsteder = "kortreist:tettsteder2025"
    tettsteder_centroids = "kortreist:tettsteder2025_centroids"
    print("Fetching unique places...")
    tettsteder_list=get_unique_values_from_geoserver_collection(geoserver, tettsteder_centroids, "tettstednavn")
    tettsted_polygon_aggr=get_features_by_attribute_value(geoserver, tettsteder_aggr, "tettstednavn", tettsteder_list[0])
    tettsted_polygon=get_features_by_attribute_value(geoserver, tettsteder, "tettstednavn", tettsteder_list[0])
    tettsted_addresses=get_features_by_attribute_value(geoserver, adresses, "tettstednavn", tettsteder_list[0])
    print(f"Number of addresses in {tettsteder_list[0]}: {len(tettsted_addresses)}")
    print(tettsted_addresses.head())


main()