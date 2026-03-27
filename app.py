import os
import psycopg2
from flask import Flask, render_template, request, redirect
# Note: Production mein 'dotenv' sirf local testing ke liye hota hai, 
# Render par hum direct 'os.environ' use karte hain.

app = Flask(__name__)

# Connection Function (Professional Way)
def get_db_connection():
    # DATABASE_URL hum Render ki settings mein se uthayenge
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_form():
    naam = request.form.get("username")
    paigam = request.form.get("usermessage")
    
    conn = get_db_connection()
    cur = conn.cursor()
    # %s use karna zaroori hai 'SQL Injection' se bachne ke liye
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (naam, paigam))
    conn.commit()
    cur.close()
    conn.close()
    
    return f"<h1>Shukriya {naam}! Aapka data Neon Cloud par save ho gaya hai.</h1>"
    
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
