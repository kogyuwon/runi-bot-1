import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask

# 환경 변수 로드
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Flask 앱 생성 (헬스 체크용)
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return {'status': 'alive'}

# 메시지 자동 삭제
async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

# /start 명령어 처리
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ 봇이 정상 작동 중입니다!")

# /help 명령어 처리
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - 봇 시작\n/help - 도움말")

# /status 명령어 처리
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 봇 상태: 정상 작동 중입니다!")

# 메인 실행 함수
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, auto_delete))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, auto_delete))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("✅ Telegram 봇이 작동 중입니다.")

    import asyncio
    await asyncio.Event().wait()

# 실행부
if __name__ == "__main__":
    import threading
    import asyncio

    # Flask 서버 백그라운드 실행
    threading.Thread(target=lambda: app_web.run(host="0.0.0.0", port=8080)).start()

    # 텔레그램 봇 실행
    asyncio.run(main())
