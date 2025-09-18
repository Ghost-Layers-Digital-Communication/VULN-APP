run vuln app on rasp pi you are attacking and exploit demo on the attacking computer.
#vuln app readme

Save as vuln_app.py and run in a virtualenv: python3 -m venv v && source v/bin/activate && pip install flask && python vuln_app.py

It binds to 127.0.0.1:5000.

Open http://127.0.0.1:5000/ and test normal login admin / s3cret.



to fix the vulnerability 

# SAFE: use parameterized queries to avoid SQL injection
    cur = db.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
    row = cur.fetchone()


# replace the vulnerable lines:
# query = "SELECT id, username FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
# cur = db.execute(query)

# with this:
cur = db.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
row = cur.fetchone()