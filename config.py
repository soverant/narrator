import logging
import os
from dotenv import load_dotenv


class Config:
    _instance = None

    def __new__(cls, telegram_token="", gemini_token="", log_level=logging.INFO):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, telegram_token="", gemini_token="", openai_token="", log_level=logging.INFO):
        load_dotenv()
        self.LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "").upper(), log_level)
        self.TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", telegram_token)
        self.GEMINI_TOKEN = os.environ.get("GEMINI_TOKEN", gemini_token)
        self.OPENAI_TOKEN = os.environ.get("OPEN_AI_TOKEN", openai_token)


def get_config():
    return Config()
