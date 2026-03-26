from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 1. Sabse pehle Database ka kaam (Init)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Server shuru hone se pehle database taiyar karein
init_db()

# 2. Saare Routes (Raste) yahan likhein
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_form():
    naam = request.form.get("username")
    paigam = request.form.get("usermessage")
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (naam, paigam))
    conn.commit()
    conn.close()
    
    return f"<h1>Shukriya {naam}! Aapka message save ho gaya hai.</h1>"

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