import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'sksis-shop-secret-key-change-in-production'
    JWT_SECRET_KEY = 'sksis-jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 7  # 7 дней

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sksis.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True