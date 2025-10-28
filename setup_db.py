from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = 'cafes.db'

# Function to get cafes with optional filter/search
def get_cafes(filter_by=None, search_term=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT id, name, location, coffee_price, wifi, power_outlet FROM cafes"

    if filter_by == "wifi":
        query += " WHERE wifi='Yes'"
    elif filter_by == "power":
        query += " WHERE power_outlet='Yes'"
    elif search_term:
        query += " WHERE name LIKE ?"
        cursor.execute(query, (f"%{search_term}%",))
        cafes = cursor.fetchall()
        conn.close()
        return cafes

    cursor.execute(query)
    cafes = cursor.fetchall()
    conn.close()
    return cafes

def add_cafe_to_db(name, location, coffee_price, wifi, power_outlet):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cafes (name, location, coffee_price, wifi, power_outlet) VALUES (?, ?, ?, ?, ?)",
        (name, location, coffee_price, wifi, power_outlet)
    )
    conn.commit()
    conn.close()

def delete_cafe_from_db(cafe_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cafes WHERE id = ?", (cafe_id,))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    filter_by = request.args.get("filter")
    search_term = request.args.get("search")
    cafes = get_cafes(filter_by, search_term)
    return render_template("index.html", cafes=cafes)

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        coffee_price = request.form["coffee_price"]
        wifi = request.form.get("wifi", "No")
        power_outlet = request.form.get("power_outlet", "No")
        add_cafe_to_db(name, location, coffee_price, wifi, power_outlet)
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    delete_cafe_from_db(cafe_id)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
