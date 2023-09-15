import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import shapely.lib


def load_france_shape() -> "shapely.lib.Geometry":
    import urllib.request
    from shapely.ops import unary_union
    from shapely.geometry import shape
    regions_url = "https://france-geojson.gregoiredavid.fr/repo/regions.geojson"
    regions_fp = "regions.json"
    urllib.request.urlretrieve(regions_url, regions_fp)
    with open(regions_fp) as f:
        regions_data = json.load(f)
    france_shape = unary_union([shape(feature['geometry'])
                                for feature in regions_data['features']
                                if feature["properties"]["code"][0] != "0"])
    return france_shape
