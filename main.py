import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
import threading

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Flask for uptime check
app_web = Flask(__name__)

@app_web.route("/")
def health():
    return {"status": "alive"}

# Telegram Bot Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ 봇이 정상 작동 중입니다!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - 시작\n/help - 도움말\n/status - 상태 확인")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 봇 상태: 정상 작동 중입니다!")

async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

# Start Flask in background
def run_flask():
    app_web.run(host="0.0.0.0", port=8080)

# Main Telegram bot function
def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, auto_delete))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, auto_delete))

    print("✅ Telegram 봇이 작동 중입니다.")
    app.run_polling()

# Run both Flask + Telegram
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
