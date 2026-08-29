"""
Configuration module for MySchool application.
Loads all application settings from .env file using python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_bool(key: str, default: bool) -> bool:
    """Convert environment variable to boolean."""
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ('true', '1', 'yes', 'on')


def get_env_int(key: str, default: int) -> int:
    """Convert environment variable to integer."""
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def get_env_list(key: str, default: list) -> list:
    """Convert environment variable to list (comma-separated)."""
    value = os.getenv(key)
    if value is None:
        return default
    return [item.strip() for item in value.split(',')]


# ─────────────────────────────────────────────────────────────────────
# DATABASE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "myschool")
DB_CONNECTION_TIMEOUT = get_env_int("DB_CONNECTION_TIMEOUT", 5000)


# ─────────────────────────────────────────────────────────────────────
# APPLICATION SETTINGS
# ─────────────────────────────────────────────────────────────────────

APP_TITLE = os.getenv("APP_TITLE", "MySchool")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
THEME_COLOR = os.getenv("THEME_COLOR", "#3949AB")
SECONDARY_COLOR = os.getenv("SECONDARY_COLOR", "#5C6BC0")


# ─────────────────────────────────────────────────────────────────────
# WINDOW CONFIGURATION
# ─────────────────────────────────────────────────────────────────────

WINDOW_WIDTH = get_env_int("WINDOW_WIDTH", 400)
WINDOW_HEIGHT = get_env_int("WINDOW_HEIGHT", 780)
WINDOW_RESIZABLE = get_env_bool("WINDOW_RESIZABLE", True)
BACKGROUND_COLOR = os.getenv("BACKGROUND_COLOR", "#F5F5F5")


# ─────────────────────────────────────────────────────────────────────
# SECURITY SETTINGS
# ─────────────────────────────────────────────────────────────────────

PASSWORD_MIN_LENGTH = get_env_int("PASSWORD_MIN_LENGTH", 8)
SESSION_TIMEOUT = get_env_int("SESSION_TIMEOUT", 0)
MAX_LOGIN_ATTEMPTS = get_env_int("MAX_LOGIN_ATTEMPTS", 5)
LOCKOUT_DURATION = get_env_int("LOCKOUT_DURATION", 15)


# ─────────────────────────────────────────────────────────────────────
# VALIDATION SETTINGS
# ─────────────────────────────────────────────────────────────────────

EMAIL_PATTERN = os.getenv(
    "EMAIL_PATTERN",
    r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
)
MOBILE_PATTERN = os.getenv(
    "MOBILE_PATTERN",
    r"^\+?[0-9]{10,15}$"
)
MOBILE_MIN_LENGTH = get_env_int("MOBILE_MIN_LENGTH", 10)
MOBILE_MAX_LENGTH = get_env_int("MOBILE_MAX_LENGTH", 15)


# ─────────────────────────────────────────────────────────────────────
# API ENDPOINTS (for future use)
# ─────────────────────────────────────────────────────────────────────

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
PASSWORD_RESET_SERVICE = os.getenv(
    "PASSWORD_RESET_SERVICE",
    "http://localhost:8000/api/reset-password"
)
EMAIL_SERVICE_ENABLED = get_env_bool("EMAIL_SERVICE_ENABLED", False)
EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL", "http://localhost:3000/api/send-email")
SMS_SERVICE_ENABLED = get_env_bool("SMS_SERVICE_ENABLED", False)
SMS_SERVICE_URL = os.getenv("SMS_SERVICE_URL", "http://localhost:3000/api/send-sms")


# ─────────────────────────────────────────────────────────────────────
# FEATURE FLAGS
# ─────────────────────────────────────────────────────────────────────

ENABLE_PASSWORD_RESET_EMAIL = get_env_bool("ENABLE_PASSWORD_RESET_EMAIL", False)
ENABLE_SMS_NOTIFICATIONS = get_env_bool("ENABLE_SMS_NOTIFICATIONS", False)
ENABLE_USER_REGISTRATION = get_env_bool("ENABLE_USER_REGISTRATION", True)
ENABLE_GUEST_ACCESS = get_env_bool("ENABLE_GUEST_ACCESS", False)
ENABLE_SOCIAL_LOGIN = get_env_bool("ENABLE_SOCIAL_LOGIN", False)


# ─────────────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_TO_FILE = get_env_bool("LOG_TO_FILE", False)
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/myschool.log")
LOG_TO_CONSOLE = get_env_bool("LOG_TO_CONSOLE", True)


# ─────────────────────────────────────────────────────────────────────
# ENVIRONMENT SPECIFIC SETTINGS
# ─────────────────────────────────────────────────────────────────────

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = get_env_bool("DEBUG", True)
ALLOW_CORS = get_env_bool("ALLOW_CORS", True)
CORS_ORIGINS = get_env_list("CORS_ORIGINS", ["http://localhost:*", "http://127.0.0.1:*"])
