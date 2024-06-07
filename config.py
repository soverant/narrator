import logging
import os
from dotenv import load_dotenv


class Config:
    def __init__(self, telegram_token="", gemini_token="", log_level=logging.INFO):
        load_dotenv()
        self.TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", telegram_token)
        self.GEMINI_TOKEN = os.environ.get("GEMINI_TOKEN", gemini_token)
        self.LOG_LEVEL = os.environ.get("GEMINI_TOKEN", log_level)
