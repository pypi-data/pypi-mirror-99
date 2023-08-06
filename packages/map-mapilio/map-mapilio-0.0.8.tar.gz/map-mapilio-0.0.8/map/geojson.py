from addict import Dict
import os
import json
import collections

class Geojson:
    """
     Get geo json format
    """
    common_json = Dict({
        "type": "FeatureCollection",
        "features": []
    })

    @staticmethod
    def get_geo_json(**kwargs) -> Dict:
        """
        Geo json Features format
        value: Dict,
        area: float,
        height: float, width: float,
        type: str
        """
        params = Dict(kwargs)

        if params.type == "Point":
            geom_type = {
                "type": params.type,
                "coordinates": [
                    params.lon,
                    params.lat
                ]
            }
        if params.type == "Polygon":
            geom_type = {
                "type"          : params.type,
                "coordinates"   : params.segmentation
            }
        if params.format == "paired":
            return Dict(
                {
                    "type": "Feature",
                    "properties": {
                        "score_1"           : params.score_1,
                        "score_2"           : params.score_2,
                        "objId_1"           : params.objId_1,
                        "objId_2"           : params.objId_2,
                        "bbox_1"            : params.bbox_1,
                        "bbox_2"            : params.bbox_2,
                        "segmentation_1"    : params.segmentation_1,
                        "segmentation_2"    : params.segmentation_2,
                        "panoId_1"          : params.panoId_1,
                        "panoId_2"          : params.panoId_2,
                    },
                    "geometry": geom_type
                })

        if params.format == "alone":
            return Dict(
                {
                    "type": "Feature",
                    "properties": {
                        "average_score"     : params.avg_score,
                        "classname"         : params.classname,
                        "area"              : params.area,
                        "height"            : params.height,
                        "width"             : params.width,
                        "confidence"        : params.confidence,
                        "match_id"          : params.match_id,
                        "matchedPoints"     : params.matchedPoints
                    },
                    "geometry": geom_type
                })

    @staticmethod
    def convert_dict_to_geojson(params: Dict, type: str) -> json:
        for key, value in params.items():
            value = Dict(value)
            ff = Geojson.get_geo_json(lat=value.lat, lon=value.lon,
                                      classname=value.classname,
                                      area=value.area,
                                      score=value.average_score,
                                      key=key,
                                      type=type)
            Geojson.common_json.features.append(ff)

        return Geojson.common_json


    @staticmethod
    def create_geojson_format(input):
        geoform = []
        for key, params in input.items():
            params = Dict(params)

            geoform.append(Geojson.get_geo_json(**params))

        return geoform

    @staticmethod
    def export_geojson(points: Dict):
        """
        Export geo json format
        """
        Geojson.common_json.features = points
        with open(os.path.join('Exports', 'detected_points.json'), 'w') as f:
            json.dump(Geojson.common_json, f)
