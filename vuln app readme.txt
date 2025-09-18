run vuln app on rasp pi you are attacking and exploit demo on the attacking computer.
#vuln app readme

Save as vuln_app.py and run in a virtualenv: python3 -m venv v && source v/bin/activate && pip install flask && python vuln_app.py

It binds to 127.0.0.1:5000.

Open http://127.0.0.1:5000/ and test normal login admin / s3cret. alice / password123

admin'--      <<< tells it to ingore password
