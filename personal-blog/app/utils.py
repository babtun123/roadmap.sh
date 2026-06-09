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
