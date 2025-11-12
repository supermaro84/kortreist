from dataclasses import dataclass
from geopandas import GeoDataFrame

@dataclass
class RouteSimulationResult:
    max_driving_time_minutes: int
    max_driving_distance_meters: int
    sample_size_addresses: int
    place_name: str
    place_centroid: GeoDataFrame
    polygon_place: GeoDataFrame
    isochrone_time: dict
    isochrone_distance: dict
    addresses_in_isochrone_time: int
    addresses_in_isochrone_distance: int
    addresses_in_place_polygon: int
    subsampled_addresses_iso_time: GeoDataFrame
    subsampled_addresses_iso_distance: GeoDataFrame
    subsampled_addresses_place: GeoDataFrame
    route_iso_time: dict
    route_iso_distance: dict
    route_place: dict
    summary_iso_time: dict
    summary_iso_distance: dict
    summary_place: dict
    stops_iso_time: list
    stops_iso_distance: list
    stops_place: list