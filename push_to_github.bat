@echo off
echo Preparing to push SNEAI Assistant to GitHub...

echo Initializing Git repository...
git init

echo Adding files to Git...
git add .

echo Committing changes...
git commit -m "Updated by Abhay: Fixed Render deployment issues with Python 3.9 compatibility"

echo Adding remote repository...
git remote add origin https://github.com/Amangupta210/today_ai_v2.git

echo Pushing to GitHub...
git push -u origin master

echo Done! Your project has been pushed to GitHub.
echo Repository URL: https://github.com/Amangupta210/today_ai_v2
pause