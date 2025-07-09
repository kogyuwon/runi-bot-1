import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from keep_alive import keep_alive  # 웹 서버 유지용

# 로깅 설정
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 봇 토큰 (환경 변수에서 가져옴)
TOKEN = os.getenv("TOKEN")

# 새로운 멤버 입장 시 메시지 삭제
async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except Exception as e:
        logger.warning(f"메시지 삭제 실패: {e}")

# /start 명령어 처리
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ 봇이 정상적으로 작동 중입니다.")

# /status 명령어 처리
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 서버 상태: 정상")

# /help 명령어 처리
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - 봇 상태 확인\n/status - 서버 상태\n/help - 명령어 목록")

# 메인 함수
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, auto_delete))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, auto_delete))

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("✅ Telegram 봇 작동 시작")
    await app.run_polling()

if __name__ == "__main__":
    keep_alive()
    import asyncio
    asyncio.run(main())
