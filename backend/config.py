import os
from sqlalchemy.engine import URL


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('Defina SECRET_KEY no ambiente antes de iniciar o sistema.')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or URL.create(
        drivername='mysql+pymysql',
        username=os.environ.get('DB_USER', 'stockchef_app'),
        password=os.environ.get('DB_PASSWORD', ''),
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        port=int(os.environ.get('DB_PORT', '3306')),
        database=os.environ.get('DB_NAME', 'stockchef'),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True, 'pool_recycle': 280}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('COOKIE_SECURE', 'true').lower() == 'true'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
