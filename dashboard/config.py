import os

class DBLogin:
    """Database login credentials for dashboard"""
    USER = "root"
    PSWD = "root"

class Config:
    """Configuration settings for dashboard"""
    SQLALCHEMY_DATABASE_URI = os.getenv(f"mysql+pymysql://{DBLogin.USER}:{DBLogin.PSWD}@localhost/labels", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
