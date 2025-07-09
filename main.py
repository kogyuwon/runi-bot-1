# main.py

import logging
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from flask import Flask
import threading

# Telegram 토큰 환경변수에서 불러오기
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 로깅 설정
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start 명령어
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 루니봇이 작동을 시작했습니다!")

# 입장/퇴장 메시지 삭제
async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

# Flask 앱으로 웹서버 실행 (Render 유지를 위해)
app = Flask(__name__)

@app.route("/")
def home():
    return "Running!"

@app.route("/health")
def health():
    return {"status": "alive"}

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# 메인 함수
async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, auto_delete))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, auto_delete))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # 여기를 없애야 함!
    logger.info("✅ 봇이 작동 중입니다.")

    await application.idle()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    import asyncio
    asyncio.run(main())
