from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, answer
from config import TELEGRAM_TOKEN

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    app.run_polling()

if __name__ == "__main__":
    main()
