import os

class DBLogin:
    USER = "root"
    PSWD = "root"

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DBLogin.USER}:{DBLogin.PSWD}@localhost/labels"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

