import re
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from config.config import (
    MONGO_URI,
    DB_NAME,
    DB_CONNECTION_TIMEOUT,
    PASSWORD_MIN_LENGTH,
    EMAIL_PATTERN,
    MOBILE_PATTERN,
)

_client = None
_db = None


def get_db():
    """Return the database instance, creating the connection if needed."""
    global _client, _db
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=DB_CONNECTION_TIMEOUT)
        _db = _client[DB_NAME]
        # Ensure unique index on username
        _db.users.create_index("username", unique=True)
    return _db


def is_valid_email(value: str) -> bool:
    return bool(re.match(EMAIL_PATTERN, value))


def is_valid_mobile(value: str) -> bool:
    # Accept 10-15 digit numbers, optionally starting with +
    return bool(re.match(MOBILE_PATTERN, value))


def is_valid_username(value: str) -> bool:
    return is_valid_email(value) or is_valid_mobile(value)


def hash_password(plain: str) -> str:
    return pbkdf2_sha256.hash(plain)


def check_password(plain: str, hashed: str) -> bool:
    try:
        return pbkdf2_sha256.verify(plain, hashed)
    except Exception:
        return False


def register_user(username: str, password: str) -> dict:
    """
    Register a new user.
    Returns {'success': True} or {'success': False, 'error': '<message>'}.
    """
    username = username.strip()
    if not is_valid_username(username):
        return {"success": False, "error": "Enter a valid email address or mobile number."}
    if len(password) < PASSWORD_MIN_LENGTH:
        return {"success": False, "error": f"Password must be at least {PASSWORD_MIN_LENGTH} characters."}

    try:
        db = get_db()
        db.users.insert_one({
            "username": username,
            "password": hash_password(password),
            "created_at": datetime.utcnow(),
        })
        return {"success": True}
    except DuplicateKeyError:
        return {"success": False, "error": "This email / mobile number is already registered."}
    except ConnectionFailure:
        return {"success": False, "error": "Cannot connect to database. Please try again."}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def login_user(username: str, password: str) -> dict:
    """
    Authenticate a user.
    Returns {'success': True, 'user': {...}} or {'success': False, 'error': '<message>'}.
    """
    username = username.strip()
    try:
        db = get_db()
        user = db.users.find_one({"username": username})
        if user is None:
            return {"success": False, "error": "Account not found. Please sign up."}
        if not check_password(password, user["password"]):
            return {"success": False, "error": "Incorrect password. Please try again."}
        return {"success": True, "user": {"username": user["username"]}}
    except ConnectionFailure:
        return {"success": False, "error": "Cannot connect to database. Please try again."}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def request_password_reset(username: str) -> dict:
    """
    Check if the user exists (stub for real reset logic).
    Returns {'success': True} or {'success': False, 'error': '<message>'}.
    """
    username = username.strip()
    if not is_valid_username(username):
        return {"success": False, "error": "Enter a valid email address or mobile number."}
    try:
        db = get_db()
        user = db.users.find_one({"username": username})
        if user is None:
            return {"success": False, "error": "No account found with that email / mobile number."}
        # In a real app, send reset link/OTP here.
        return {"success": True}
    except ConnectionFailure:
        return {"success": False, "error": "Cannot connect to database. Please try again."}
    except Exception as exc:
        return {"success": False, "error": str(exc)}
