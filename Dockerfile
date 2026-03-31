# PRO TIP: Standard Python 3.9 image
FROM python:3.9-slim

# Install system dependencies for report generation
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory where the bot will live
WORKDIR /app

# Step 1: Copy only requirements first (this makes building MUCH faster)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Copy the rest of the project
COPY . .

# Step 3: Create temporary folders so the agent can save files
RUN mkdir -p .tmp outputs

# Step 4: Tell the server to start the Telegram bot
CMD ["python", "telegram_bot.py"]
