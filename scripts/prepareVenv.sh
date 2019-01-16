#!/bin/sh

cd ..

if ! [ -f "requirements.txt" ] ; then
   echo Run script in script directory using $0 command.
   exit 1
fi

echo Using the following python:
python --version

if ! [ $? -eq 0 ] ; then
   echo No Python found
   exit 1
fi

if [ -d "venv" ] ; then
   echo venv already exists. Please remove venv directory in order to continue.
   exit 1
fi

echo Creating virtual env.
python -m virtualenv venv

if ! [ $? -eq 0 ] ; then
   echo No virtualenv module found. Installing virtualenv
   pip install virtualenv
   python -m virtualenv venv
fi

echo Installing python requirements:
source venv/bin/activate && pip install -r requirements.txt && deactivate

if ! [ $? -eq 0 ] ; then
   echo Something went wrong. Please check if you need to setup HTTP proxy.
   rm -rf venv
   exit 1
fi

echo Installation completed.