from config import Config
from logger import setup_logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id=thread_id,
                                   text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    configs = Config()
    setup_logger(configs.LOG_LEVEL)

    application = ApplicationBuilder().token(configs.TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)

    application.run_polling()
