import features
from ipyleaflet import Map, basemaps, Marker,AwesomeIcon
import endpoints

def main():
   icon = AwesomeIcon(
    name='flag',
    marker_color='green',
    icon_color='white'
    )
   geoserver = endpoints.Geoserver(
        url="https://geoserver-4vzmi.ondigitalocean.app/geoserver",
        collections_endpoint="ogc/features/v1/collections")
   addresses = "kortreist:addresser_leilighet"
   bakery = [60.141162879935706, 11.172404842272075]
   iso=features.get_isochrone_time(bakery[1],bakery[0],25)
   addresses_tettsteder=features.get_addresses_from_osm_for_isochrone(iso)
   addresses=endpoints.get_features_by_attribute_value(geoserver, addresses, "tettstednavn", 'Nordkjosbotn')

   subsampled=features.subsample_addresses(addresses,sample_size=50)

   route,stops_coordinates,summary=features.get_route(subsampled)
   print(route)
   print(stops_coordinates)
   print(summary)
if __name__ == "__main__":
    main()
