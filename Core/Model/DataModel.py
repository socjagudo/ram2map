import pandas as pd

class DataModel:
    
    def __init__(self, data):
        self.non_geolocated = pd.DataFrame(data[data.COORD.isnull() == True])
        self.data = pd.DataFrame(data[(data.COORD.isnull() == False) & (data.RST_SENT.isnull() == False)])
        self.data.RST_SENT = self.data.RST_SENT.apply(pd.to_numeric)

    def get_nb_of_empty_cells(self):
        return len (self.non_geolocated.index)

    def get_latitudes (self):
        return [latitude for longitude, latitude in self.data.COORD]
    
    def get_longitudes (self):
        return [longitude for longitude, latitude in self.data.COORD]
    
    def get_RST (self):
        return self.data.RST_SENT