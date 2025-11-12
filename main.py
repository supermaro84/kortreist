import features
from ipyleaflet import Map, basemaps, Marker,AwesomeIcon
import endpoints
from constants import MAX_DRIVING_TIME_MINUTES, MAX_DRIVING_DISTANCE_METERS,TETTSTEDER_AGGREGATED, TETTSTEDER, TETTSTEDER_CENTROIDS, ADDRESSES,SAMPLE_SIZE
import utils
from models import RouteSimulationResult 
import pickle
def main():
   geoserver = endpoints.Geoserver(
      url="https://geoserver-4vzmi.ondigitalocean.app/geoserver",
      collections_endpoint="ogc/features/v1/collections")
   addresses = ADDRESSES
   tettsteder_aggr = TETTSTEDER_AGGREGATED
   tettsteder = TETTSTEDER
   tettsteder_centroids = TETTSTEDER_CENTROIDS
   tettsteder_list=endpoints.get_unique_values_from_geoserver_collection(geoserver, tettsteder, "tettstednavn")
   list_results=[]
   for i,t in enumerate(tettsteder_list):      
      max_driving_time_minutes=MAX_DRIVING_TIME_MINUTES
      max_driving_distance_meters=MAX_DRIVING_DISTANCE_METERS
      sample_size_addresses=SAMPLE_SIZE
      place_name=t
      place_centroid=t_centroid=endpoints.get_features_by_attribute_value(geoserver,tettsteder_centroids, "tettstednavn", t)
      polygon_place=tettsted_polygon_aggr=endpoints.get_features_by_attribute_value(geoserver, tettsteder_aggr, "tettstednavn", t)
      isochrone_time=features.get_isochrone_time(t_centroid.geometry.iloc[0].x, t_centroid.geometry.iloc[0].y, MAX_DRIVING_TIME_MINUTES)
      isochrone_distance = features.get_isochrone_distance(t_centroid.geometry.iloc[0].x, t_centroid.geometry.iloc[0].y, MAX_DRIVING_DISTANCE_METERS)
      addresses_in_isochrone_time = endpoints.get_features_by_polygon(geoserver, addresses, utils.isochrone_polygon_wkt(isochrone_time))
      addresses_in_isochrone_distance = endpoints.get_features_by_polygon(geoserver, addresses, utils.isochrone_polygon_wkt(isochrone_distance))
      addresses_in_place_polygon = endpoints.get_features_by_polygon(geoserver, addresses,tettsted_polygon_aggr['geometry'][0].wkt)
      subsampled_addresses_iso_time=features.subsample_addresses(addresses_in_isochrone_time,SAMPLE_SIZE)
      subsampled_addresses_iso_distance=features.subsample_addresses(addresses_in_isochrone_distance,SAMPLE_SIZE)
      subsampled_addresses_place=features.subsample_addresses(addresses_in_place_polygon,SAMPLE_SIZE)
      print(f"Simulating routes for place: {place_name}")
      route_iso_time,stops_iso_time,summary_iso_time=features.get_route(subsampled_addresses_iso_time)
      print(f"Simulating routes for isochrone distance for place: {place_name}")
      route_iso_distance,stops_iso_distance,summary_iso_distance=features.get_route(subsampled_addresses_iso_distance) 
      print(f"Simulating routes for place polygon for place: {place_name}")
      route_place,stops_place,summary_place=features.get_route(subsampled_addresses_place) 
      result=RouteSimulationResult(
         max_driving_time_minutes=max_driving_time_minutes,
         max_driving_distance_meters=max_driving_distance_meters,
         sample_size_addresses=sample_size_addresses,
         place_name=place_name,
         place_centroid=place_centroid,
         polygon_place=polygon_place,
         isochrone_time=isochrone_time,
         isochrone_distance=isochrone_distance,
         addresses_in_isochrone_time=len(addresses_in_isochrone_time),
         addresses_in_isochrone_distance=len(addresses_in_isochrone_distance),
         addresses_in_place_polygon=len(addresses_in_place_polygon),
         subsampled_addresses_iso_time=subsampled_addresses_iso_time,
         subsampled_addresses_iso_distance=subsampled_addresses_iso_distance,
         subsampled_addresses_place=subsampled_addresses_place,
         route_iso_time=route_iso_time,
         route_iso_distance=route_iso_distance,
         route_place=route_place,
         summary_iso_time=summary_iso_time,
         summary_iso_distance=summary_iso_distance,
         summary_place=summary_place,
         stops_iso_time=stops_iso_time,
         stops_iso_distance=stops_iso_distance,
         stops_place=stops_place
      )      
      list_results.append(result)
      if i ==5:
         break
   with open('route_simulation_results.pkl', 'wb') as f:
      pickle.dump(list_results, f)
   
if __name__ == "__main__":
    main()
