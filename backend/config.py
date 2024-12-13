import os

class Config:
    SECRET_KEY = os.urandom(24)  # Secret key for sessions
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Example database URL (SQLite)
    SQLALCHEMY_TRACK_MODIFICATIONS = False