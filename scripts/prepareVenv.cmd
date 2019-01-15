@echo off

IF NOT EXIST ".git" (
    echo Run script in main directory using script\%0 command.
    EXIT /B 1
)

echo Using the following python:
python --version || echo No Python found && EXIT /B 1

IF EXIST "venv" (
    echo venv already exists. Please remove venv directory in order to continue.
    EXIT /B 1
)

echo Creating virtual env.
python -m virtualenv venv || echo No virtualenv module found. Installing virtualenv && pip install virtualenv

echo Installing python requirements:
venv\Scripts\activate.bat && pip install -r requirements.txt && deactivate || echo Something went wrong. Please check if you need to setup HTTP proxy.

echo Installation completed.