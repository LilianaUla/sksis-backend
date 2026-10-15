import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sksis-shop-secret-key-change-in-production')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'sksis-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 7

    # Берём DATABASE_URL из окружения (Vercel/Neon), иначе SQLite локально
    db_url = os.environ.get('DATABASE_URL')

    if db_url:
        # Vercel/Neon иногда отдаёт 'postgres://', SQLAlchemy требует 'postgresql://'
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sksis.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'