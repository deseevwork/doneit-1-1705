import os
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_db_name.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
