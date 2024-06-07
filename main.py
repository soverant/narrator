from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackContext,
    CommandHandler
)
from collections import deque
import google.generativeai as genai
from config import Config
from logger import setup_logger
import logging

# A global dictionary to store messages, using deque to keep only the last 100 messages
message_storage = {}

summarize_system_prompt = f"""
You are a Narrator who summarize a chat history for fast boarding
"""

logger = logging.getLogger(__name__)


# Define the function to handle messages
async def store_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    message = update.message

    if chat_id not in message_storage:
        message_storage[chat_id] = deque(maxlen=100)

    message_storage[chat_id].append((message.message_id, message.text))


# Function to handle commands or any other types of messages
async def start(update: Update, context: CallbackContext) -> None:
    logger.debug("start called")
    await update.message.reply_text("Hello! I'm tracking the last 100 messages in this group/channel.")


# Function to summarize messages
async def summarize_messages(update: Update, context: CallbackContext) -> None:
    logger.debug("summarize_messages called")
    chat_id = update.effective_chat.id

    if chat_id not in message_storage or len(message_storage[chat_id]) == 0:
        await update.message.reply_text("No messages to summarize.")
        return

    messages = list(message_storage[chat_id])
    text_to_summarize = "\n".join([msg[1] for msg in messages])

    chat_summarize_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest',
                                                 system_instruction=summarize_system_prompt)
    logger.debug("summary request: %s", text_to_summarize)
    summary = chat_summarize_model.generate_content(text_to_summarize)
    logger.debug("summary response: %s", summary.text)
    await update.message.reply_text(f"Summary of the last 100 messages:\n{summary.text}")


def main() -> None:
    configs = Config()
    setup_logger(configs.LOG_LEVEL)
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = ApplicationBuilder().token(configs.TELEGRAM_TOKEN).build()
    genai.configure(api_key=configs.GEMINI_TOKEN)
    # Add handlers
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), store_message))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("summarize", summarize_messages))
    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
