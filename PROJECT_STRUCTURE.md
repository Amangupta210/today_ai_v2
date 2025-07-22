# SNEAI Assistant Project Structure

This document explains the structure of the SNEAI Assistant project and which files are essential for different deployment scenarios.

## Core Files (Required for All Deployments)

- `app.py` - Main Flask application
- `local_ai_engine.py` - Local AI engine implementation
- `templates/index.html` - Web interface HTML template
- `static/style.css` - CSS styling for the web interface
- `requirements.txt` - Dependencies for the application
- `Procfile` - For web service configuration (contains: `web: gunicorn app:app`)

## Web Deployment Files

- `RENDER_DEPLOYMENT.md` - Guide for deploying to Render
- `prepare_for_render.bat` - Script to prepare the project for Render deployment
- `README_WEB.md` - Simplified README for the web version
- `.gitignore` - Specifies files to exclude from version control

## Desktop Application Files (Not Required for Web Deployment)

- `sneai_desktop.py` - Desktop application using CustomTkinter
- `run_desktop.bat` - Script to run the desktop application

## Documentation Files

- `README.md` - Main project documentation
- `PROJECT_STRUCTURE.md` - This file, explaining the project structure

## Deployment Configuration Files

- `render.yaml` - Configuration for Render deployment

## Temporary Files (Can Be Removed)

- `today_logic.py` - Original API-based logic (not used in the local version)
- `todayAI.py` - Original desktop application (replaced by sneai_desktop.py)
- `requirements_full.txt` - Full requirements including desktop dependencies

## Data Files

- `custom_responses.json` - Stores custom responses taught to the AI (created automatically)

## How to Prepare for Deployment

1. Run `prepare_for_render.bat` to clean up the project
2. Follow the instructions in `RENDER_DEPLOYMENT.md`
3. Deploy to Render using the web interface or CLI