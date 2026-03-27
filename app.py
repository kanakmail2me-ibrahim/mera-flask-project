import os
import psycopg2
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv # Secret files padhne ke liye

load_dotenv() # .env file se data load karein
app = Flask(__name__)

# Database se connect karne ka professional function
def get_db_connection():
    # 'DATABASE_URL' hum Render ki settings mein dalenge
    url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(url)
    return conn

# Table banane ka tareeka (Thoda sa SQL syntax badal jayega)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY, -- 'AUTOINCREMENT' ki jagah 'SERIAL'
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Server shuru hone se pehle database taiyar karein
init_db()

# 2. Saare Routes (Raste) yahan likhein
@app.route("/submit", methods=["POST"])
def submit_form():
    naam = request.form.get("username")
    email = request.form.get("usermessage")
    
    conn = get_db_connection()
    cur = conn.cursor()
    # SQL Injection se bachne ke liye hamesha %s use karein (Production Standard)
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (naam, email))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")
    
@app.route("/admin")
def admin_page():
    # 1. Database se saara data nikalna
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    saara_data = cursor.fetchall() # Yeh saari rows ko ek list mein le aayega
    conn.close()
    
    # 2. Data ko ek naye HTML page par bhejna
    return render_template("admin.html", users=saara_data)

@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    # Database se connect karein
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Us ID wale user ko mita dein
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    # Delete karne ke baad wapas Admin page par bhej dein
    return redirect("/admin")

# Upar 'from flask import ...' mein 'redirect' bhi add kar lijiye


# 3. Sabse AAKHIRI mein server chalaein
if __name__ == "__main__":
    app.run(debug=True)
