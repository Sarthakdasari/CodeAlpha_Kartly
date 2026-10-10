import os, secrets
BASE = os.path.dirname(os.path.abspath(__file__))
PRODUCTION = os.environ.get("FLASK_ENV") == "production"
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    DATABASE = os.path.join(BASE, "instance", "ecommerce.db")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = PRODUCTION
    DEBUG = False
if PRODUCTION and not os.environ.get("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY must be set in production")
