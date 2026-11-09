import os
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('Defina SECRET_KEY no ambiente antes de iniciar o sistema.')

    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith(('postgres://', 'postgresql://')):
        database_url = database_url.replace(database_url.split('://')[0], 'postgresql+psycopg2', 1)
    SQLALCHEMY_DATABASE_URI = database_url or URL.create(
        drivername=os.environ.get('DB_DRIVER', 'postgresql+psycopg2'),
        username=os.environ.get('DB_USER', 'stockchef_app'),
        password=os.environ.get('DB_PASSWORD', ''),
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        port=int(os.environ.get('DB_PORT', '5432')),
        database=os.environ.get('DB_NAME', 'postgres'),
        query={'sslmode': os.environ.get('DB_SSLMODE', 'require')},
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'poolclass': NullPool}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('COOKIE_SECURE', 'true').lower() == 'true'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
