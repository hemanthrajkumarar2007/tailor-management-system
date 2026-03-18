from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect("tailor.db")
    conn.row_factory = sqlite3.Row
    return conn


# CREATE TABLE
conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
billno INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
phone TEXT,

shirt_length TEXT,
shoulder TEXT,
sleeve TEXT,
chest TEXT,
stomach TEXT,
shirt_hip TEXT,
collar TEXT,

pant_length TEXT,
waist TEXT,
pant_hip TEXT,
thigh TEXT,
knee TEXT,
bottom TEXT,
fork TEXT
)
""")

conn.commit()
conn.close()


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# ADD CUSTOMER
@app.route("/add", methods=["POST"])
def add():

    data = (
        request.form["name"],
        request.form["phone"],

        request.form["shirt_length"],
        request.form["shoulder"],
        request.form["sleeve"],
        request.form["chest"],
        request.form["stomach"],
        request.form["shirt_hip"],
        request.form["collar"],

        request.form["pant_length"],
        request.form["waist"],
        request.form["pant_hip"],
        request.form["thigh"],
        request.form["knee"],
        request.form["bottom"],
        request.form["fork"]
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO customers(
    name,phone,
    shirt_length,shoulder,sleeve,chest,stomach,shirt_hip,collar,
    pant_length,waist,pant_hip,thigh,knee,bottom,fork
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, data)

    conn.commit()
    conn.close()

    return "Customer Saved <br><a href='/'>Back</a>"


# SEARCH CUSTOMER
@app.route("/search", methods=["GET","POST"])
def search():

    rows = []

    if request.method == "POST":

        billno = request.form.get("billno")
        phone = request.form.get("phone")

        conn = get_db_connection()
        cursor = conn.cursor()

        if billno:
            cursor.execute("SELECT * FROM customers WHERE billno=?", (billno,))
        elif phone:
            cursor.execute("SELECT * FROM customers WHERE phone=?", (phone,))

        rows = cursor.fetchall()

        conn.close()

    return render_template("search.html", rows=rows)


# CUSTOMER LIST
@app.route("/customers")
def customers():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")

    rows = cursor.fetchall()

    conn.close()

    return render_template("customers.html", rows=rows)


# EDIT PAGE
@app.route("/edit/<int:billno>")
def edit(billno):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers WHERE billno=?", (billno,))

    customer = cursor.fetchone()

    conn.close()

    return render_template("edit.html", customer=customer)


# UPDATE CUSTOMER
@app.route("/update/<int:billno>", methods=["POST"])
def update(billno):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE customers SET

    shirt_length=?,
    shoulder=?,
    sleeve=?,
    chest=?,
    stomach=?,
    shirt_hip=?,
    collar=?,

    pant_length=?,
    waist=?,
    pant_hip=?,
    thigh=?,
    knee=?,
    bottom=?,
    fork=?

    WHERE billno=?
    """,(

    request.form["shirt_length"],
    request.form["shoulder"],
    request.form["sleeve"],
    request.form["chest"],
    request.form["stomach"],
    request.form["shirt_hip"],
    request.form["collar"],

    request.form["pant_length"],
    request.form["waist"],
    request.form["pant_hip"],
    request.form["thigh"],
    request.form["knee"],
    request.form["bottom"],
    request.form["fork"],

    billno
    ))

    conn.commit()
    conn.close()

    return "Customer Updated <br><a href='/customers'>Back</a>"


# DELETE CUSTOMER
@app.route("/delete/<int:billno>")
def delete(billno):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customers WHERE billno=?", (billno,))

    conn.commit()
    conn.close()

    return "Customer Deleted <br><a href='/customers'>Back to Customer List</a>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


