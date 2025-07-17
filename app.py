from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('intentions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS intentions (id INTEGER PRIMARY KEY, text TEXT)''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect('intentions.db')
    c = conn.cursor()

    if request.method == "POST":
        intention = request.form.get("intention")
        if intention:
            c.execute("INSERT INTO intentions (text) VALUES (?)", (intention,))
            conn.commit()
        return redirect("/")

    c.execute("SELECT * FROM intentions ORDER BY id DESC")
    all_intentions = c.fetchall()
    conn.close()
    return render_template("index.html", intentions=all_intentions)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)