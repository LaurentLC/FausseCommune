from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import shapely.geometry
    import pandas as pd

COMMUNES_URL = "https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"
REGIONS_URL = "https://france-geojson.gregoiredavid.fr/repo/regions.geojson"


class PublicData:
    _france_shape = None
    _communes_data = None

    @classmethod
    def get_france_shape(cls) -> "shapely.geometry.shape":
        if cls._france_shape is None:
            import requests
            from shapely.ops import unary_union
            from shapely.geometry import shape
            regions_data = requests.get(REGIONS_URL).json()
            france_shape = unary_union([shape(feature['geometry'])
                                        for feature in regions_data['features']
                                        if feature["properties"]["code"][0] != "0"])
            cls._france_shape = france_shape
        return cls._france_shape

    @classmethod
    def fetch_communes_data(cls) -> "pd.DataFrame":
        if cls._communes_data is None:
            import pandas as pd
            df = pd.read_csv(COMMUNES_URL)
            df = df[["nom_commune_complet", "latitude", "longitude"]]
            cls._communes_data = df.dropna()
        return cls._communes_data
