# Imports for main
import sys
from PyQt5.QtWidgets import QApplication

# App Modules
from View.LightBrowser import  LightBrowser
from Model.HeatMapModel import HeatMapModel 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = LightBrowser()

    view.addModel('heatMap', HeatMapModel)
    view.show()

    sys.exit(app.exec_())