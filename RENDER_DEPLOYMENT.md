# Deploying SNEAI Assistant to Render

This guide explains how to deploy SNEAI Assistant to Render for free.

## Step 1: Prepare Your Project

Ensure your project has the following essential files:
- `app.py` - Main Flask application
- `local_ai_engine.py` - Local AI engine
- `templates/index.html` - Web interface template
- `static/style.css` - CSS styling
- `requirements.txt` - Dependencies
- `Procfile` - For web service configuration

## Step 2: Create a Render Account

1. Go to [render.com](https://render.com/)
2. Sign up for a free account
3. Verify your email address

## Step 3: Create a New Web Service

1. Log in to your Render dashboard
2. Click the "New +" button in the top right
3. Select "Web Service"

## Step 4: Connect Your Repository

Option 1: Connect to GitHub
1. Click "Connect account" under GitHub
2. Authorize Render to access your repositories
3. Select your SNEAI Assistant repository

Option 2: Deploy Manually
1. Select "Deploy from existing repository"
2. Click "Public Git repository"
3. Enter your repository URL or use the "Upload Files" option

## Step 5: Configure Your Web Service

Fill in the following details:
- **Name**: `sneai-assistant` (or any name you prefer)
- **Environment**: `Python 3`
- **Region**: Choose the closest to your users
- **Branch**: `main` (or your default branch)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Select "Free"

## Step 6: Deploy Your Application

1. Click "Create Web Service"
2. Wait for the deployment to complete (this may take a few minutes)
3. Once deployed, Render will provide a URL for your application (e.g., `https://sneai-assistant.onrender.com`)

## Step 7: Test Your Deployment

1. Visit the provided URL in your browser
2. Test the SNEAI Assistant functionality
3. Verify that all features are working correctly

## Troubleshooting

If you encounter issues:
1. Check the Render logs for error messages
2. Ensure all required files are included in your repository
3. Verify that your `requirements.txt` includes all necessary dependencies
4. Make sure your `Procfile` contains `web: gunicorn app:app`

## Maintaining Your Deployment

- Render's free tier has some limitations, including:
  - Limited compute hours per month
  - The service will spin down after periods of inactivity
  - The first request after inactivity may be slow

- To update your application:
  1. Push changes to your repository
  2. Render will automatically redeploy your application

## Additional Resources

- [Render Python Documentation](https://render.com/docs/deploy-python)
- [Render Free Tier Information](https://render.com/pricing)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)