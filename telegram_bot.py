import os
import logging
import subprocess
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# --- SETUP ---
# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup project paths
BASE_DIR = Path(__file__).resolve().parent
TMP_DIR = BASE_DIR / ".tmp"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORT_MD = OUTPUTS_DIR / "report.md"
REPORT_DOCX = OUTPUTS_DIR / "report.docx"
REPORT_PDF = OUTPUTS_DIR / "report.pdf"
CONFIG_FILE = TMP_DIR / "config.json"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- HELPERS ---

def extract_summary_data(md_path: Path):
    """
    Reads report.md and extracts topic, source, and key findings.
    """
    data = {
        "topic": "Unknown",
        "source": None,
        "findings": []
    }
    
    if not md_path.exists():
        return data
    
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    found_findings = False
    for line in lines:
        line = line.strip()
        # Extract Topic
        if "**Research Topic:**" in line:
            data["topic"] = line.replace("**Research Topic:**", "").strip()
        # Extract Source
        if "**Source Used:**" in line:
            data["source"] = line.replace("**Source Used:**", "").strip()
        
        # Extract Findings
        if "## 2. Key Findings" in line:
            found_findings = True
            continue
        
        if found_findings:
            if line.startswith("##"): # Next section started
                break
            if line.startswith("-"):
                data["findings"].append(line.replace("-", "💡").strip())
    
    return data

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    user = update.effective_user
    await update.message.reply_html(
        rf"👋 Hi {user.mention_html()}! I am your **AI Research Agent**."
        "\n\n🚀 Just send me a topic and I will find the best facts for you!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /help command."""
    await update.message.reply_text(
        "📝 How to use:\n\n"
        "1. Send any topic (e.g., 'Future of AI in 2026')\n"
        "2. Wait for the agent to search and analyze.\n"
        "3. Get a summary and professional PDF/Word reports!"
    )

async def handle_research(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main handler that takes a topic and runs the research agent."""
    topic = update.message.text
    if not topic:
        return

    # 1. Force PDF and DOCX generation via config
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"gen_docx": True, "gen_pdf": True}, f)

    # Send initial status
    await update.message.reply_text(f"🔍 **Researching:** _{topic}_\n\n⚙️ I am searching the web and generating your reports. Please wait...")

    try:
        # Run the research agent via subprocess
        process = await asyncio.create_subprocess_exec(
            "python", "run_agent.py", topic,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(BASE_DIR)
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            # 2. Extract Data for Premium Formatting
            report_data = extract_summary_data(REPORT_MD)
            
            # 3. Create Premium Message
            response_text = (
                f"✅ **Research Complete!**\n\n"
                f"🎯 **Topic:** {report_data['topic']}\n\n"
                f"📊 **Executive Summary:**\n"
            )
            
            if report_data["findings"]:
                for finding in report_data["findings"][:8]: # Show top 8
                    response_text += f"{finding}\n"
            else:
                response_text += "_No specific facts found for this topic._\n"

            # 4. Create Interactive Buttons
            keyboard = []
            
            # Row 1: Source & New Research
            row1 = []
            if report_data["source"] and report_data["source"].startswith("http"):
                row1.append(InlineKeyboardButton("🌐 View Source Website", url=report_data["source"]))
            row1.append(InlineKeyboardButton("🔍 New Research", callback_data="new_search"))
            keyboard.append(row1)
            
            # Row 2: Download Buttons (User requested these)
            row2 = [
                InlineKeyboardButton("📄 Download PDF", callback_data="dl_pdf"),
                InlineKeyboardButton("💼 Download Word", callback_data="dl_doc")
            ]
            keyboard.append(row2)

            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send Summary with Buttons
            await update.message.reply_text(response_text, parse_mode="Markdown", reply_markup=reply_markup)

        else:
            error_details = stderr.decode().strip()
            await update.message.reply_text(f"❌ **Research Failed**\n\nError: {error_details[:300]}")

    except Exception as e:
        logger.exception("Error during research execution:")
        await update.message.reply_text(f"🆘 **System Error:** {str(e)}")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for button clicks (callbacks)."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "new_search":
        await query.message.reply_text("Please type your next research topic below!")
        return

    if query.data == "dl_pdf":
        if REPORT_PDF.exists():
            await query.message.reply_document(
                document=open(REPORT_PDF, "rb"),
                filename="Research_Report.pdf"
            )
        else:
            await query.message.reply_text("⚠️ PDF file not found. It may not have been generated yet.")
            
    elif query.data == "dl_doc":
        if REPORT_DOCX.exists():
            await query.message.reply_document(
                document=open(REPORT_DOCX, "rb"),
                filename="Research_Report.docx"
            )
        else:
            await query.message.reply_text("⚠️ Word file not found. It may not have been generated yet.")

# --- MAIN ---

if __name__ == "__main__":
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        exit(1)

    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_research))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print("--- AI Research Bot is online with Button Downloads! ---")
    application.run_polling()
