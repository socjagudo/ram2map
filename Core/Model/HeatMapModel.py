import statistics
import tempfile
from folium import Map
from folium.plugins import HeatMap



class HeatMapModel:
    def __init__(self, datamodel):
        self.datamodel = datamodel
        self.meanLongitudes = statistics.mean(self.datamodel.get_longitudes())
        self.meanLatitudes  = statistics.mean(self.datamodel.get_latitudes())

        # Create object Map
        km0 = [40.4167, -3.70325]
        self.mapObj = Map(location=km0, zoom_start = 11.5)

        # Create Heat Map
        self.heatmap = HeatMap( list(zip(self.datamodel.get_longitudes(), self.datamodel.get_latitudes(), self.datamodel.get_RST())),
                                min_opacity=0.2,
                                radius=50, blur=50, 
                                max_zoom=1)

        # Add layer to base map
        self.heatmap.add_to(self.mapObj)

    def saveMap (self, full_path_file_name = None):
        if full_path_file_name is None:
            fo, full_path_file_name = tempfile.mkstemp(suffix = '.html')
            full_path_file_name = full_path_file_name.replace('\\', '/')
            
        self.mapObj.save(full_path_file_name)
        return full_path_file_name
