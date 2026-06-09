"""config"""

import os
from pathlib import Path

class Config:
    """config class"""
    # csrf token
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE_DIR = Path(__file__).parent
    ARTICLES_DIR = BASE_DIR / "articles"
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'wembydagoat'
