# Setting Up Dev On Windows

## Python

- Install [Python ActiveState Version for windows](http://www.activestate.com/activepython/downloads) (use 32bit version)
- Execute: ActivePython-2.7.2.5-win32-x86.msi
- Should default install to C:\Python27

## Windows Environment

**Console2**

Settings/edit/shell:

    C:\Users\Larry\set_alias.bat


**Create System Variables:**

    set PYTHONHOME=C:\Python27
    set PYTHONPATH=%PYTHONHOME%;C:\Python27\Lib
    set PYTHONSTARTUP=%HOME%\.pythonrc

**To associate .py to lauch automatically, launch cmd as administrator and run:**

    assoc .py=Python.File
    ftype Python.File=%PYTHONHOME%\python.exe "%1" %*
    

Had to hack a file to enable virtualenv to run!

    ed C:\Python27\Lib\socket.py

Insert above: import _socket

    import sys
    sys.path.append('C:\\Python27\\DLLs')
    
Install libraries for GeoDjango. **OSGeo4W**

Download the **OSGeo4W Installer**

    http://download.osgeo.org/osgeo4w/osgeo4w-setup.exe

Execute installed and select Express install: **OSGeo4W**
**Select defaults. Do not include Apache**

## Clone [ourfield](https://github.com/LarryEitel/ourfield) GIT Project
    
**NOTE:** activate.bat, a convenience batch file assumes project name is ourfield

    mkdir /__prjs
    cd __prjs
    git clone git@github.com:LarryEitel/ourfield.git ourfield
    

## Create virtualenv Environment in Windows

**NOTE: **If you have installed ActiveState Python, you DO NOT need to install pip

    pip install -U virtualenv

**Do not use --no-site-packages per** [Stack Overflow](http://stackoverflow.com/questions/9046125/fab-hello-returns-no-module-named-win32api-only-in-virtualenv) comment

Create virtual environment called **ve**.

    virtualenv ve

Activate new environment using convenience batch file. It does a little more than activate enviroment. For example, it sets some environment variables for **GEOS** and **OSGEO4W**.

    activate.bat

## MySQL

- Download MySQL-python and install
- [Downloads codegood](http://www.codegood.com/downloads) [MySQL-python-1.2.3.win32-py2.7.exe](http://www.codegood.com/download/10/)
- Create Database

    mysql --user=<user> --password=<password> --execute="CREATE DATABASE _of CHARACTER SET utf8 COLLATE utf8_general_ci;"

## coffee

**Download and Install** [nodejs](http://nodejs.org/#download). **See also**: [CoffeeScript-Compiler-for-Windows](https://github.com/alisey/CoffeeScript-Compiler-for-Windows)

**Download** [CoffeeScript](http://github.com/jashkenas/coffee-script/tarball/master)

Extract into **ourfield/utils**
**Create a symlink** of the DIR named something like **jashkenas-coffee-script-cb0003d** in the same folder and name it **coffee-script**.

In ourfield project folder, run:


    python utils\ryppi.py install coffee-script


























