# vuln_app_hack.py (lab-hacking mode)
from flask import Flask, request, g
import sqlite3
import os

DB = "lab_users.db"
app = Flask(__name__)

# --- Delete existing DB to start fresh (lab-only) ---
if os.path.exists(DB):
    os.remove(DB)

# --- Initialize database ---
def init_db():
    db = sqlite3.connect(DB)
    db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    db.execute("INSERT INTO users (username, password) VALUES ('admin', 's3cret')")
    db.execute("INSERT INTO users (username, password) VALUES ('alice', 'password123')")
    db.commit()
    db.close()

init_db() # force creation at startup

# --- DB helper ---
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

# --- Routes ---
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

@app.route('/login')
def login():
    username = request.args.get('username','')
    password = request.args.get('password','')
    db = get_db()
    # === LAB-VULNERABLE: SQL injection allowed on purpose ===
    query = f"SELECT id, username FROM users WHERE username = '{username}' AND password = '{password}'"
    cur = db.execute(query)
    row = cur.fetchone()
    if row:
        return f"Authenticated as {row['username']}. (id={row['id']})"
    return "Login failed."

# --- Teardown DB ---
@app.teardown_appcontext
def teardown(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

# --- Run app ---
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
