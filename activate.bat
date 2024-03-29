@echo off
set PROJECTS_ROOT=C:\Users\Larry\__prjs
set PROJECT_NAME=ourfield
set PYTHON_ROOT=C:\Python27
set PYTHONHOME=%PYTHON_ROOT%
set PROJECT_ROOT=%PROJECTS_ROOT%\%PROJECT_NAME%
set DJANGO_SETTINGS_MODULE=%PROJECT_NAME%.settings

set OSGEO4W_ROOT=C:\OSGeo4W
set GEOS_LIBRARY_PATH=%OSGEO4W_ROOT%\bin
set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
set GEOS_LIBRARY_PATH=%OSGEO4W_ROOT%\bin
set PATH=%PATH%;%PROJECT_ROOT%\scripts\windows;%OSGEO4W_ROOT%\bin

set PYTHONPATH=%PROJECTS_ROOT%;%PROJECT_ROOT%;%PROJECT_ROOT%\parts;%PROJECT_ROOT%\apps;%PROJECT_ROOT%\ve\Lib;%PROJECT_ROOT%\ve\Lib\site-packages;%PYTHON_ROOT%;%PYTHON_ROOT%\Lib;%PYTHON_ROOT%\Lib\site-packages;%GEOS_LIBRARY_PATH%

for %%f in (%OSGEO4W_ROOT%\etc\ini\*.bat) do call %%f

%PROJECT_ROOT%\ve\Scripts\activate.bat

@echo on

@cmd.exe

