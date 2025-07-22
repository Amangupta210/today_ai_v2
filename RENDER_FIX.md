# Fixing Render Deployment Issues

This guide addresses common deployment issues with Render.

## Python Version Compatibility

The application is now configured to use Python 3.9.16, which is more compatible with the dependencies.

Files that specify the Python version:
- `runtime.txt` - Contains `python-3.9.16`
- `.python-version` - Contains `3.9.16`
- `render.yaml` - Specifies `runtime: python3.9`

## Dependency Changes

The following changes were made to fix dependency issues:

1. Replaced `lxml` with `html5lib` as the parser for BeautifulSoup
2. Updated `web_tools.py` to use the `html5lib` parser
3. Removed some heavy dependencies like `wolframalpha`

## Deployment Steps

1. Push the latest changes to GitHub:
   ```
   git add .
   git commit -m "Fixed Render deployment issues with Python 3.9 compatibility"
   git push origin main
   ```

2. In Render dashboard:
   - Create a new Web Service
   - Connect to your GitHub repository
   - Select the Python environment
   - Use the following settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Deploy the service

3. If you still encounter issues:
   - Check the build logs for specific errors
   - Try manually setting the Python version in the Render dashboard
   - Consider using a Docker-based deployment instead

## Testing the Deployment

After deployment, test the following features:
- Basic chat functionality
- Weather information
- Web search capabilities
- News updates

If any feature doesn't work, check the server logs for specific errors.