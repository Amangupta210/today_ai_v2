@echo off
echo Preparing SNEAI Assistant for Render deployment...

echo Removing unnecessary files...
if exist today_logic.py del today_logic.py
if exist todayAI.py del todayAI.py
if exist requirements_full.txt del requirements_full.txt
if exist run_desktop.bat del run_desktop.bat
if exist deploy.py del deploy.py
if exist DEPLOYMENT.md del DEPLOYMENT.md
if exist app.json del app.json
if exist runtime.txt del runtime.txt

echo Renaming README_WEB.md to README.md...
copy README_WEB.md README.md /Y

echo Creating render.yaml...
echo services: > render.yaml
echo   - type: web >> render.yaml
echo     name: sneai-assistant >> render.yaml
echo     env: python >> render.yaml
echo     buildCommand: pip install -r requirements.txt >> render.yaml
echo     startCommand: gunicorn app:app >> render.yaml
echo     envVars: [] >> render.yaml

echo Done! Your project is now ready for Render deployment.
echo Please follow the instructions in RENDER_DEPLOYMENT.md to deploy your application.
pause