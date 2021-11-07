*** WATCH OUT WHEN BUILDING 

Package needs some extra hooks in the code of your current environment.
See https://stackoverflow.com/questions/54836440/branca-python-module-is-unable-to-find-2-essential-json-files-when-running-an-ex

Basically:

Firstly you have to edit these 3 files:

    \folium\folium.py
    \folium\raster_layers.py
    \branca\element.py

Makes the following changes, commenting out the existing ENV line and replacing with the code below:

#ENV = Environment(loader=PackageLoader('folium', 'templates'))
import os, sys
from jinja2 import FileSystemLoader
if getattr(sys, 'frozen', False):
        # we are running in a bundle
    templatedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    templatedir = os.path.dirname(os.path.abspath(__file__))
ENV = Environment(loader=FileSystemLoader(templatedir + '\\templates'))

Create this spec file in your root folder, obviously your pathex and project name will be different:

# -*- mode: python -*-

block_cipher = None


a = Analysis(['time_punch_map.py'],
         pathex=['C:\\Users\\XXXX\\PycharmProjects\\TimePunchMap'],
         binaries=[],
         datas=[
         (".\\venv\\Lib\\site-packages\\branca\\*.json","branca"),
         (".\\venv\\Lib\\site-packages\\branca\\templates","templates"),
         (".\\venv\\Lib\\site-packages\\folium\\templates","templates"),
         ],
         hiddenimports=[],
         hookspath=[],
         runtime_hooks=[],
         excludes=[],
         win_no_prefer_redirects=False,
         win_private_assemblies=False,
         cipher=block_cipher,
         noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)
exe = EXE(pyz,
      a.scripts,
      a.binaries,
      a.zipfiles,
      a.datas,
      [],
      name='time_punch_map',
      debug=False,
      bootloader_ignore_signals=False,
      strip=False,
      upx=True,
      runtime_tmpdir=None,
      console=True )

Finally generate the single exe with this command from the terminal:

pyinstaller time_punch_map.spec
