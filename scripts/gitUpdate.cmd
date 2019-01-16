@echo off

git fetch -p && git stash && git rebase && git stash pop

cd .. && venv\Scripts\activate.bat && pip install -r requirements.txt