from flask import Flask, render_template, request, redirect, url_for,flash
import sqlite3

app = Flask(__name__)
app.secret_key = "flash message"
DATABASE = 'crudapplication.db'


@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return render_template("index.html", items=items)

@app.route("/addPage")
def addPage():
    return render_template("add.html")

@app.route("/addItem", methods=["POST"])
def addItem():

    flash("Data Inserted Successfully")
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']
    
    with sqlite3.connect(DATABASE) as conn:
        curs = conn.cursor()
        curs.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        conn.commit()
    return redirect(url_for("addPage"))

@app.route("/edit/<int:item_id>")
def editItem(item_id):
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute("SELECT * FROM items WHERE itemNo=?", (item_id,))
    item = curs.fetchone()
    conn.close()
    return render_template("edit.html", item=item)

@app.route("/updateItem/<int:item_id>", methods=["POST"])
def updateItem(item_id):
    name = request.form["name"]
    quantity = request.form["quantity"]
    price = request.form["price"]

    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute("""
        UPDATE items SET name=?, quantity=?, price=? WHERE itemNo=?
    """, (name, quantity, price, item_id))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:item_id>")
def deleteItem(item_id):
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute("DELETE FROM items WHERE itemNo=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
