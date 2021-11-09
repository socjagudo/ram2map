import os
import subprocess

from datetime import date

INNO = """
; -- Ram2Map.iss --

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

#define public ramsourcedir "%s"
#define public version "%s" 

[Setup]
AppName=RAM Tu Map
AppVersion={#version}
WizardStyle=modern
DefaultDirName={autopf}\RAM\Ram2Map
DisableProgramGroupPage=yes
Compression=lzma2
SolidCompression=yes
SourceDir={#ramsourcedir}
OutputDir=..\..\Release
OutputBaseFilename=Installer_Ram2Map_{#Version}

[Files]
Source: "*"; DestDir: "{app}" ;Flags: ignoreversion recursesubdirs

[Icons]
Name: "{autoprograms}\RAM\Ram2map"; Filename: "{app}\Ram2map.exe"
Name: "{autodesktop}\RAM\Ram2map"; Filename: "{app}\Ram2map.exe"
"""

if __name__ == '__main__':

  # Build paths
  cwd = os.getcwd()
  dist_path = os.path.join(cwd, '..\\dist\\ram2map\\')
  inno_script_filename = os.path.join(cwd, '..\\inno\\ram2map.iss')
  
  # Build inno params
  d = date.today()
  version = d.strftime('%Y.%m.%d')
  
  # Build inno file
  iscc_script = INNO % (dist_path, version)
  f = open(inno_script_filename, 'w')
  f.write(iscc_script)
  f.close()
  
  # Run inno file
  subprocess.run(['iscc', inno_script_filename]) 
  
  
