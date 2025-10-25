import features
from ipyleaflet import Map, basemaps, Marker,AwesomeIcon

def main():
   icon = AwesomeIcon(
    name='flag',
    marker_color='green',
    icon_color='white'
    )
   bakery = [60.141162879935706, 11.172404842272075]
   iso=features.get_isochrone_time(bakery[1],bakery[0],25)
   addresses=features.get_addresses_from_osm_for_isochrone(iso)
   subsampled=features.subsample_addresses(addresses,sample_size=50)
   route=features.get_route(subsampled)
   print(route)
if __name__ == "__main__":
    main()
