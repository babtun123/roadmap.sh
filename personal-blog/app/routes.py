"""routes"""
from app import app
from flask import render_template, url_for, abort, request, session, redirect
from app.utils import get_all_articles, get_article, delete_article
from app.utils import validate_login_cred, save_article, update_article

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_login_cred(username, password):
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return render_template("login.html", title='Sign in')

@app.before_request
def check_login():
    """Check if user is logged in as admin"""
    print("before request running", request.path)
    if request.path.startswith('/admin'):
        if not session.get('logged_in'):
            return redirect(url_for('login'))

@app.route('/admin')
def admin():
    """admin route"""
    articles = get_all_articles()
    return render_template('admin.html', title="Admin page", articles=articles)

@app.route('/admin/new', methods=['GET', 'POST'])
def new():
    """To add new article as an admin"""
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        content = request.form['content']
        data = {
            "title": title,
            "content": content,
            "date": date
        }
        save_article(data)
        return redirect(url_for('admin'))
    return render_template('new.html', title='New Article')

@app.route('/admin/edit/<slug>', methods=['GET', 'POST'])
def edit(slug):
    """edit an article"""
    if request.method == "GET":
        selected_article = get_article(slug)
        if not selected_article:
            abort(404)
        return render_template('edit.html', title=selected_article['title'],
                           selected_article = selected_article)

    title = request.form['title']
    date = request.form['date']
    content = request.form['content']
    data = {
        "title": title,
        "content": content,
        "date": date
    }
    update_article(slug, data)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<slug>', methods=['POST'])
def delete(slug):
    """delete route"""
    delete_article(slug)
    return redirect(url_for('admin'))
