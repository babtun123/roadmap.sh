"""routes"""
from app import app
from flask import render_template, url_for, abort
from app.utils import get_all_articles, get_article

@app.route('/')
@app.route('/home')
def home():
    """Home page"""
    articles = get_all_articles()
    return render_template('home.html', title="Home page", articles=articles)

@app.route('/article/<slug>')
def article(slug):
    """article"""
    selected_article = get_article(slug)
    if not selected_article:
        abort(404)
    return render_template('article.html', title=selected_article['title'],
                           selected_article = selected_article)
