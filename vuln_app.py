# vuln_app.py (lab only)
from flask import Flask, request, g, redirect
import sqlite3
import os

DB = "lab_users.db"
app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    if not os.path.exists(DB):
        db = sqlite3.connect(DB)
        db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        db.execute("INSERT INTO users (username, password) VALUES ('admin', 's3cret')")
        db.execute("INSERT INTO users (username, password) VALUES ('alice', 'password123')")
        db.commit()
        db.close()

@app.before_first_request
def setup():
    init_db()

@app.route('/')
def index():
    return '''
      <h2>Lab Login (vulnerable)</h2>
      <form method="GET" action="/login">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <input type="submit" value="Login">
      </form>
    '''

# === VULNERABLE login endpoint ===
@app.route('/login')
def login():
    username = request.args.get('username','')
    password = request.args.get('password','')
    db = get_db()
    # vulnerable: direct string interpolation into SQL (DO NOT DO THIS in real apps)
    query = "SELECT id, username FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    cur = db.execute(query)
    row = cur.fetchone()
    if row:
        return f"Authenticated as {row['username']}. (id={row['id']})"
    return "Login failed."

@app.teardown_appcontext
def teardown(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)