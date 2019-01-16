#!/bin/sh

git fetch -p && git stash && git rebase && git stash pop

cd .. && source venv/bin/activate && cd System && python main.py