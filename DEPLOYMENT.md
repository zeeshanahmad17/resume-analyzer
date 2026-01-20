# 🚀 Render Deployment Guide (Absolute Free Tier)

Follow these exact steps to host your AI Resume Analyzer for free on Render.

## 1. Push Code to GitHub
Ensure all your project files (including the `Procfile` and updated `requirements.txt` I just created) are pushed to a repository on **GitHub** or **GitLab**.

## 2. Create a Render Account
Go to [render.com](https://render.com) and sign up (linking your GitHub account is easiest).

## 3. Create a New Web Service
1.  Click the **"New +"** button and select **"Web Service"**.
2.  Connect your Resume Analyzer repository.

## 4. Configure the Service
Set the following options in the Render dashboard:
-   **Name**: `resume-analyzer-ai` (or any name you like)
-   **Region**: Pick the one closest to you (e.g., Singapore or US East).
-   **Branch**: `main`
-   **Root Directory**: (Leave blank)
-   **Runtime**: `Python 3`
-   **Build Command**: `pip install -r requirements.txt`
-   **Start Command**: `gunicorn app:app`
-   **Instance Type**: Select **Free** ($0/month).

## 5. Add Environment Variables
This is the **most important step**. Render needs your secret keys:
1.  Go to the **"Environment"** tab on your Render dashboard.
2.  Add the following keys (copy them from your local `.env` file):
    -   `GEMINI_API_KEY` = `your_actual_key`
    -   `MONGODB_URI` = `your_actual_mongodb_uri`
    -   `FLASK_ENV` = `production`
    -   `FLASK_DEBUG` = `0`

## 6. Deploy!
Click **"Create Web Service"**. Render will start building the project.
-   It will take about 2-3 minutes to install dependencies.
-   Once you see **"Your service is live!"**, click the URL provided at the top (e.g., `https://resume-analyzer-ai.onrender.com`).

---

### ⚠️ Important Notes for Free Tier:
1.  **Cold Starts**: If you don't visit the site for 15 minutes, Render puts the server to sleep. The next time you open the URL, it will take ~40 seconds to "wake up."
2.  **Indexing Time**: Since we are on a free tier, keep that **30-second wait** in the UI to ensure MongoDB Atlas has plenty of time to process the vectors on the cloud.
3.  **Uploads Folder**: On Render's free tier, files uploaded to the `uploads/` folder are temporary and will disappear when the server restarts. This is fine for our app because we store everything in MongoDB!
