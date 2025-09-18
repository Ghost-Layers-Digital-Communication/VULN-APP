# vuln_app.py (lab-only, fixed for Python 3.11 + Flask 3.1.2)
from flask import Flask, request, g
import sqlite3
import os

DB = "lab_users.db"
app = Flask(__name__)

# --- Database helper functions ---
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    """Initialize database if it does not exist."""
    if not os.path.exists(DB):
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

# --- Run init_db only once before the first request ---
def setup_once():
    if not getattr(app, "_got_first_request", False):
        init_db()
        app._got_first_request = True

@app.before_request
def before_request_hook():
    setup_once()

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
    # === VULNERABLE SQL query for lab purposes ONLY ===
    query = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    cur = db.execute(query, (username, password))
    row = cur.fetchone()
    if row:
        return f"Authenticated as {row['username']}. (id={row['id']})"
    return "Login failed."

# --- Close database at teardown ---
@app.teardown_appcontext
def teardown(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

# --- Run the app ---
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
