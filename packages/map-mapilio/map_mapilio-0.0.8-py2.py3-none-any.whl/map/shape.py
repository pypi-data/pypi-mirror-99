import os
from addict import Dict
from folium import folium, features
import folium


class ShapeOperations:
    """
    Shape Operatings
    Draw Line
    Add Point
    """

    def __init__(self, map):
        self.map = map

    def addPoint(self, kwargs: Dict,
                 area: float = None,
                 color: str = 'darkgreen'):
        """
        Add point
        """

        params = Dict(kwargs)
        objectImage_1 = os.path.join("../", params.detectedPath_1)  #
        objectImage_2 = os.path.join("../", params.detectedPath_2)

        area = '{:.3f}'.format(area)
        html = "<section class="'container'" style="'width:450px'"> \
        	        <div class="'value'"> \
                        <b>MatchId = </b> {id1}  <br>  <b>Area = </b> {area} square meter </br>\
        		        <img src={detectedObjectPath_1} style="'width:auto;height:80px;'"> \
                        <img src={detectedObjectPath_2} style="'width:auto;height:80px;'"> \
                        <a href="'{imgUrl_1}'">Panorma Url - 1 </a> \
                        <a href="'{imgUrl_2}'">Panorma Url - 2 </a> \
        		    </div> \
        	    </section>".format(id1=str(params.match_id), area=area,
                                   detectedObjectPath_1=objectImage_1,
                                   detectedObjectPath_2=objectImage_2,
                                   imgUrl_1=params.imgUrl_1,
                                   imgUrl_2=params.imgUrl_2)

        mk = features.Marker([params.Lat_center, params.Lon_center],
                             popup=html, icon=folium.Icon(color=color, icon_color='#FFFF00'))

        self.map.add_child(mk)

    def addPolyline(self, des, classname, obj):
        """
        Poly line drawing
        """
        folium.PolyLine(
            locations=des,
            color='red',
            opacity=4,
            tooltip=classname + "-" + str(obj),
            weight=4
        ).add_to(self.map)

    def triggerPolyLine(self, mapDrawPolyLine):
        """
        processing coming polyline data
        """

        for key, params in mapDrawPolyLine.items():
            params = Dict(params)
            self.addPolyline(des=params.desPoint, classname=params.classname, obj=key)

    def triggerPoint(self, mapDrawPoint):
        """
        processing coming point data
        """

        for key, params in mapDrawPoint.items():
            params = Dict(params)
            # randomColor = random.choice(self.config.selectionColorMap)
            self.addPoint(kwargs=params.point, area=params.area, color="red")
