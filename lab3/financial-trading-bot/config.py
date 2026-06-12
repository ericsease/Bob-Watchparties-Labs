"""Application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trading.db")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Exchange credentials
    EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "")
    EXCHANGE_API_SECRET = os.getenv("EXCHANGE_API_SECRET", "")
    EXCHANGE_PASSPHRASE = os.getenv("EXCHANGE_PASSPHRASE", "")

    # Market data
    MARKET_DATA_API_KEY = os.getenv("MARKET_DATA_API_KEY", "")

    # Notifications
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT", "")

    # Application
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_TRADE_AMOUNT_USD = float(os.getenv("MAX_TRADE_AMOUNT_USD", 10000))
    RISK_LIMIT_PERCENT = float(os.getenv("RISK_LIMIT_PERCENT", 2.0))
