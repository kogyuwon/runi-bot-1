import os
import time
import logging
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 로그 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask 서버 설정
app = Flask(__name__)

@app.route('/')
def index():
    return {"status": "alive"}

@app.route('/health')
def health():
    return {"status": "healthy", "timestamp": time.time()}

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    Thread(target=run_flask, daemon=True).start()

# 입장/퇴장 메시지 자동 삭제
async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message and (update.message.new_chat_members or update.message.left_chat_member):
            await update.message.delete()
    except Exception as e:
        logger.error(f"메시지 삭제 오류: {e}")

# /start 명령어
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ 봇이 정상 작동 중입니다!")

# /status 명령어
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 상태: 온라인\n🧹 입장/퇴장 메시지 자동 삭제 중!")

# 메인 실행 함수
async def main():
    if not TOKEN:
        logger.error("환경변수에 TELEGRAM_BOT_TOKEN이 설정되지 않았습니다.")
        return

    application = Application.builder().token(TOKEN).build()

    # 핸들러 등록
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, auto_delete))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, auto_delete))
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))

    await application.initialize()
    await application.start()
    logger.info("🤖 봇이 시작되었습니다.")
    await application.updater.start_polling()

    # 종료 방지
    import asyncio
    await asyncio.Event().wait()

if __name__ == '__main__':
    keep_alive()

    import asyncio
    asyncio.run(main())
