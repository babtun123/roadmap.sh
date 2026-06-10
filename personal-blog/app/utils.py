"""Utils"""
from config import Config
import json

ARTICLE_PATH = Config.ARTICLES_DIR

def get_all_articles():
    """Returns all articles."""
    list_of_articles = []

    for file in ARTICLE_PATH.glob("*.json"):
        loaded = load_json(file)
        loaded["slug"] = file.stem
        list_of_articles.append(loaded)
    return list_of_articles

def get_article(slug):
    """return a specific article"""
    path = slug + ".json"
    loaded = load_json(ARTICLE_PATH / path)
    return loaded

def load_json(file_path):
    """Load json file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            return loaded
    except FileNotFoundError:
        return {}

def save_json(file_path, data):
    """Save json file"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def validate_login_cred(user, passw):
    """Validate login credentials"""
    return user == Config.ADMIN_USERNAME and passw == Config.ADMIN_PASSWORD

def save_article(data):
    """Save article"""
    title = data['title']
    slug = title.lower().replace(' ', '-')
    path = slug + ".json"
    save_json(ARTICLE_PATH / path, data)

def update_article(slug, data):
    """update article"""
    path = slug + ".json"
    save_json(ARTICLE_PATH / path, data)

def delete_article(slug):
    """delete an article"""
    file = slug + ".json"
    path = ARTICLE_PATH / file
    path.unlink()
