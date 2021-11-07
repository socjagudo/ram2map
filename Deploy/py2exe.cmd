RMDIR /S /Q build
RMDIR /S /Q dist
del *.spec
pyinstaller ..\Core\ram2map.py --additional-hooks-dir .\hooks --clean -p ..\Core -p ..\Core\View -p ..\Core\Model -p ..\Core\Control