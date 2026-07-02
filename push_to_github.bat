@echo off
cd /d %~dp0

git init

git remote remove origin 2>nul
git remote add origin https://github.com/apiusage/IdeaFinder.git

git add .

git commit -m "auto update %date% %time%"

git checkout -B main

git push --force origin main

pause