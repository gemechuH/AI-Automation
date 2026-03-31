# 🕵️‍♂️ AI Research Telegram Bot (Version 1)

This setup allows you to run your local AI Research Agent through a Telegram interface. Just message your bot a topic, and it will respond with a research summary and the full report files.

---

## 🚀 Getting Started

### 1. Create Your Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Type `/newbot` and follow the instructions to name your bot.
3. BotFather will give you an **API Token**. 
4. Copy that token and paste it into your `.env` file like this:
   `TELEGRAM_BOT_TOKEN=YOUR_NEW_TOKEN_HERE`

### 2. Install Requirements
Make sure you have all the needed Python libraries installed:
```bash
pip install -r requirements.txt
```

### 3. Run the Bot
Inside your project folder, start the bot with this command:
```bash
python telegram_bot.py
```
You should see a message saying: `--- Bot is now online and listening! ---`

---

## 👨‍💻 How to Test It
1. Find your bot on Telegram (use the link BotFather gave you).
2. Type `/start` to see the welcome message.
3. Type a research topic, for example: `Best AI tools for 2026`.
4. The bot will reply with `🚀 Research started...`.
5. Wait about 30-60 seconds while your local machine performs the research.
6. The bot will message you back with the **Key Findings** and then upload:
   - `report.md`
   - `report.docx`
   - `report.pdf` (if available)

---

## 🛠 Troubleshooting

### "Research Failed" or 0 Facts
This usually means the research agent couldn't find good data on the website it scraped. Try a different topic or a more specific search term.

### Bot Not Responding
- Check your terminal/console for error messages.
- Ensure your `.env` file has the correct token.
- Make sure your internet connection is active.

### File Missing in Telegram
The bot only sends the files if they actually exist in your `outputs/` folder after the research is done. Check if `run_agent.py` generated the files correctly on your local machine.
