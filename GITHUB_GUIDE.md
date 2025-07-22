# Pushing SNEAI Assistant to GitHub

This guide explains how to push the SNEAI Assistant project to GitHub.

## Prerequisites

1. [Git](https://git-scm.com/downloads) installed on your computer
2. A [GitHub](https://github.com/) account
3. Access to the repository: https://github.com/Amangupta210/today_ai_v2

## Option 1: Using the Batch Script

1. Run the `push_to_github.bat` script included in the project
2. Enter your GitHub credentials when prompted
3. Wait for the process to complete

## Option 2: Manual Push

1. Open a terminal or command prompt in the project directory
2. Initialize a Git repository:
   ```
   git init
   ```
3. Add all files to the repository:
   ```
   git add .
   ```
4. Commit the changes:
   ```
   git commit -m "Initial commit of SNEAI Assistant with web scraping capabilities"
   ```
5. Add the remote repository:
   ```
   git remote add origin https://github.com/Amangupta210/today_ai_v2.git
   ```
6. Push to GitHub:
   ```
   git push -u origin master
   ```
7. Enter your GitHub credentials when prompted

## Troubleshooting

If you encounter a "Permission denied" error:
1. Make sure you have write access to the repository
2. Try using a personal access token instead of your password
3. Contact the repository owner for access

If you encounter a "Repository already exists" error:
1. Clone the repository first:
   ```
   git clone https://github.com/Amangupta210/today_ai_v2.git
   ```
2. Copy your files into the cloned repository
3. Commit and push the changes

## After Pushing

Once you've pushed the code to GitHub, you can:
1. Deploy to Render using the instructions in RENDER_DEPLOYMENT.md
2. Share the GitHub repository URL with others
3. Continue developing and push updates as needed