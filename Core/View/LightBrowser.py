#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Simple navegador web con PyQt 5.
#
#       Copyright 2018 Recursos Python - www.recursospython.com
#
#

import sys
import ctypes
from PyQt5 import QtGui
sys.path.insert(0, '../Model')

from PyQt5.QtCore import QUrl, QEvent
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QStatusBar
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QMenuBar, QMenu
from PyQt5.QtWidgets import QWidget, QAction, QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView

from Model.helpers.adif_helper import get_body
from Model.DataModel import DataModel


class LightBrowser(QMainWindow):

    def __init__(self):
        # Init QT 
        QMainWindow.__init__(self)
        self.setWindowTitle("RAM Tu Map")
        self.setIcon()
        self.widget = QWidget(self)

        # Init Models
        self.models = {}
        
        # Define Actions
        self._create_actions()

        # Connect Actions()
        self._connectActions()

        # Create Menu
        self._create_menu()

        # Status Basr
        self.status_bar = QStatusBar()
        self.statusBar().eventFilter = self.event_filter
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Loading Ram tu Map ...", 2000)
        
        # Browser Widget
        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://radioactivacionmadrid.blogspot.com/"))
        self.webview.urlChanged.connect(self.url_changed)

        # Back Button
        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.webview.back)
        
        # Forward Button
        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.webview.forward)
        
        # Actualizar la página
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.webview.reload)
        
        # Barra de direcciones
        self.url_text = QLineEdit()
        
        # Cargar la página actual
        self.go_button = QPushButton("Go!")
        self.go_button.clicked.connect(self.url_set)
        
        self.toplayout = QHBoxLayout()
        self.toplayout.addWidget(self.back_button)
        self.toplayout.addWidget(self.forward_button)
        self.toplayout.addWidget(self.refresh_button)
        self.toplayout.addWidget(self.url_text)
        self.toplayout.addWidget(self.go_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.toplayout)
        self.layout.addWidget(self.webview)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def setIcon(self):
        
        if sys.platform == 'win32':
            myappid = 'ram.2021.11.04' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        self.setWindowIcon(QtGui.QIcon("ram.png"))

    # Actions
    def openFile(self):
        # Get Filename from Dialog 
        fileDialog = QFileDialog()
        file_name = fileDialog.getOpenFileName(self, 'Open File', 'C:\\temp\\', 'Adif Files (*.adi)')
        self.adif_file_name = file_name[0]
        self.status_bar.showMessage('Loading data model {0} ... '.format(self.adif_file_name))
        self.status_bar.repaint()

        # Load File and Geolocate it
        try:
            self.dataModel = DataModel(get_body(file = self.adif_file_name, as_pandas = True, geolocate = True))
            null_lines = self.dataModel.get_nb_of_empty_cells()
        except Exception as err:
            error_message = 'Unable to retrive data from model. Details: {0}'.format(err)
            msg_box = QMessageBox.critical(self, "Error loading File", error_message)
            self.status_bar.showMessage('Data Model Source: None')
            return

        # Show info dialog for loading data
        msg_box =  QMessageBox.information(self, 'Data Loaded', '{0} loaded into data model. \n {1} lines unable to geolocate'.format(self.adif_file_name, null_lines))
        self.status_bar.showMessage('Data Model Source: {0}'.format(self.adif_file_name))

    def about(self):
        self.webview.load(QUrl("https://radioactivacionmadrid.blogspot.com/"))
        self.webview.urlChanged.connect(self.url_changed)

    def heatMap(self):
        heatMapFnc = self.models.get('heatMap', None)
        if heatMapFnc is None:
            raise Exception ('HeatMapModel is not defined')
        else:
            self.heatMapModel = heatMapFnc (self.dataModel)
            heatModelFileName = self.heatMapModel.saveMap()
            self.status_bar.showMessage("Heat Map Model Generated at {0}".format(heatModelFileName))
           
            self.webview.load(QUrl("file:///{0}".format(heatModelFileName)))

    def addModel (self, model, fnc):
        self.models[model] = fnc
    
    # Connect Actions
    def _connectActions(self):
        # Connect File actions
        self.openAction.triggered.connect(self.openFile)
        self.exitAction.triggered.connect(self.close)

        # Connect Model Actions
        self.heatMapAction.triggered.connect(self.heatMap)

        # Connect Help actions
        self.aboutAction.triggered.connect(self.about)

     # Snip...
    def _create_actions(self):
        # Creating action using the first constructor
        self.openAction = QAction(self)
        self.openAction.setText("&Open")
        # Creating actions using the second constructor
        self.exitAction = QAction("&Exit", self)
        self.aboutAction = QAction("&About", self)
        self.heatMapAction = QAction("&HeatMap", self)

    def _create_menu(self):
        # Create Menu bar
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        
        # File Menu
        fileMenu = QMenu("&File", self)
        self.menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        editMenu = QMenu("&Edit", self)
        self.menuBar.addMenu(editMenu)
        editMenu.addAction(self.heatMapAction)

        helpMenu = QMenu("&Help", self)
        self.menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.aboutAction)

    @staticmethod
    def event_filter(_, event):
        """ Monkey patch status bar: 
            https://stackoverflow.com/questions/42423425/pyqt-how-can-i-prevent-hovering-over-a-qmenu-from-clearing-the-qstatusbar
        """
        if event.type() == QEvent.StatusTip:
            return True
        return False
        
    def url_changed(self, url):
        """Actualizar la barra de direcciones"""
        self.url_text.setText(url.toString())
        self.status_bar.showMessage('Data Model Source: None')
    
    def url_set(self):
        """Acceder a un nuevo URL"""
        self.webview.setUrl(QUrl(self.url_text.text()))
