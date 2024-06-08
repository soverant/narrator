import traceback
import html
import json
import logging
from collections import deque
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackContext,
    CommandHandler,
    ContextTypes
)
import google.generativeai as genai
import config
from logger import setup_logger

# A global dictionary to store messages, using deque to keep only the last 100 messages
from summerizer import gai_summarizer, openai_summarizer

message_storage = {}

configs = config.get_config()
setup_logger(configs.LOG_LEVEL)
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
    summary = openai_summarizer(messages)
    logger.debug("summary response: %s", summary)
    await update.message.reply_text(f"Summary of the last 100 messages:\n{summary}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""

    # Log the error before we do anything else, so we can see it even if something breaks.

    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a

    # list of strings rather than a single string, so we have to join them together.

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)

    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.

    # You might need to add some logic to deal with messages longer than the 4096 character limit.

    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    message = (

        "An exception was raised while handling an update\n"

        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"

        "</pre>\n\n"

        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"

        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"

        f"<pre>{html.escape(tb_string)}</pre>"

    )

    # Finally, send the message
    await update.message.reply_text(message,parse_mode=ParseMode.HTML)


def main() -> None:
    setup_logger(configs.LOG_LEVEL)
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = ApplicationBuilder().token(configs.TELEGRAM_TOKEN).build()
    # Add handlers
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), store_message))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("summarize", summarize_messages))
    # ...and the error handler
    application.add_error_handler(error_handler)
    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
