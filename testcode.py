import os
import sqlite3
import pickle
from flask import Flask, request

app = Flask(__name__)

# --- VULNERABILITY 1: Hardcoded Secret Key ---
SECRET_KEY = "12345-very-weak-hardcoded-key"
app.config['SECRET_KEY'] = SECRET_KEY

# --- Database Setup ---
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, password TEXT)")
conn.commit()

@app.route("/")
def home():
    return "Vulnerable Python App for Testing!"

# --- VULNERABILITY 2: SQL Injection ---
@app.route("/user")
def get_user():
    username = request.args.get("name")
    query = f"SELECT * FROM users WHERE name = '{username}'"   # ❌ vulnerable
    result = cursor.execute(query).fetchall()
    return str(result)

# --- VULNERABILITY 3: Command Injection ---
@app.route("/ping")
def ping():
    host = request.args.get("host")
    return os.popen(f"ping -c 1 {host}").read()   # ❌ vulnerable

# --- VULNERABILITY 4: Insecure Deserialization ---
@app.route("/load", methods=["POST"])
def load_pickle():
    data = request.data
    obj = pickle.loads(data)  # ❌ unsafe
    return str(obj)

# --- VULNERABILITY 5: Path Traversal ---
@app.route("/read")
def read_file():
    filename = request.args.get("file")
    return open(filename, "r").read()  # ❌ no validation

# --- VULNERABILITY 6: Weak Hashing ---
import hashlib
@app.route("/hash")
def weak_hash():
    password = request.args.get("pwd")
    return hashlib.md5(password.encode()).hexdigest()   # ❌ MD5 is weak

# --- Debug Mode (not for production) ---
if __name__ == "__main__":
    app.run(debug=True)   # ❌ exposes debug console

