# 🚀 How to Deploy Your AI Research Bot for FREE (2026)

To keep your Telegram bot running 24/7 without keeping your computer on, you can deploy it to a cloud provider. Since your agent performs **web scraping**, you need a provider that allows outbound internet requests.

---

## Recommended Provider: [Render](https://render.com/) or [Koyeb](https://www.koyeb.com/)

Both of these have excellent free tiers. Render is slightly more beginner-friendly.

### 1. Prepare Your Project
Make sure your folder has these files (I have already created them for you):
- `telegram_bot.py` (The main entry point)
- `requirements.txt` (List of libraries)
- `run_agent.py` & `execution/` folder (The backend)
- `Dockerfile` (Instructions for the server)

### 2. Push to GitHub
1. Create a private repository on GitHub.
2. Upload all your files into that repository.
   - **IMPORTANT:** Do NOT upload your `.env` file. We will set the token in the dashboard instead.

### 3. Deploy to Render (Free)
1. Go to [Render dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository.
4. Settings:
   - **Name:** `ai-research-bot`
   - **Language:** `Docker` (This is the most reliable way)
   - **Plan:** `Free`
5. Click **Advanced** and then **Add Environment Variable**:
   - **Key:** `TELEGRAM_BOT_TOKEN`
   - **Value:** `PASTE_YOUR_BOT_TOKEN_HERE`
6. Click **Create Web Service**.

---

## 🏗 Docker Configuration
I have created a `Dockerfile` in your root folder. This tells the server exactly how to set up the environment:

```dockerfile
# Use Python 3.9
FROM python:3.9-slim

# Install system dependencies for PDF/Word generation
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create necessary folders
RUN mkdir -p .tmp outputs

# Run the Telegram Bot
CMD ["python", "telegram_bot.py"]
```

---

## ⚠️ Important Notes

### 1. Inactivity (Render Free Tier)
On Render's Free tier, the service "sleeps" after 15 minutes of no one visiting the URL.
- **Problem:** If it sleeps, your Telegram bot won't respond until it's "woken up".
- **Fix:** You can use a free service like [Cron-job.org](https://cron-job.org/) to ping your Render URL every 10 minutes to keep it awake!

### 2. IP Blocking
Some websites block requests from cloud providers like Render or AWS. If you find your bot failing to scrape specific sites while deployed:
- It's not a bug in your code.
- It's the website blocking the "Cloud IP".
- Real-world solution: You would eventually need a "Proxy Service" (this usually costs money).

### 3. Persistent Data
On free tiers, any files in the `outputs/` folder will be **deleted** when the server restarts or sleeps.
- This is fine for a research bot! You simply run the research, get the file in Telegram, and move on. The bot doesn't need to keep the file forever on the server because it sent it to your chat.
