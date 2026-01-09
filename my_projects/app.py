from flask import Flask, render_template, request
from flask import session, redirect, url_for
import mysql.connector
import bcrypt

app = Flask(__name__)
print("CONNECTING AS ROOT")
app.secret_key="mysecret"


# DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",
    database="expense_db"
)

cursor = db.cursor()

@app.route("/add", methods=["POST"])
def add():
    amount = request.form["amount"]
    category = request.form["category"]

    print("DATA:", amount, category)

    sql = "INSERT INTO expenses(amount,category,date) VALUES(%s,%s,CURDATE())"
    cursor.execute(sql,(amount,category))

    db.commit()

    return "Expense Added!"

@app.route("/view")
def view():
    cursor.execute("SELECT amount, category FROM expenses")
    expenses = cursor.fetchall()
    return render_template("view.html", expenses=expenses)

@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM expenses WHERE id=%s",(id,))
    db.commit()
    return "Deleted! <a href='/view'>Go Back</a>"

@app.route("/summary")
def summary():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    return render_template("summary.html", data=data)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        hashed = bcrypt.hashpw(p.encode(), bcrypt.gensalt())

        cursor.execute("INSERT INTO users(username,password) VALUES(%s,%s)",(u,hashed))
        db.commit()
        return "Registered! <a href='/login'>Login</a>"

    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        cursor.execute("SELECT password,role FROM users WHERE username=%s",(u,))
        user=cursor.fetchone()

        if user and bcrypt.checkpw(p.encode(), user[0].encode()):
            session["user"]=u
            session["role"]=user[1]

            if user[1]=="admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("home"))
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"]!="admin":
        return "Access Denied"

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM expenses")
    expenses = cursor.fetchone()[0]

    return render_template(
        "admin.html",
        users=users,
        expenses=expenses
    )


@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))

@app.route("/forgot", methods=["GET","POST"])
def forgot():
    if request.method=="POST":
        u = request.form["username"]
        newp = request.form["password"]

        hashed = bcrypt.hashpw(newp.encode(), bcrypt.gensalt())

        cursor.execute(
            "UPDATE users SET password=%s WHERE username=%s",
            (hashed, u)
        )
        db.commit()

        return "Password updated! <a href='/login'>Login</a>"

    return render_template("forgot.html")

@app.route("/chart")
def chart():
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    )
    data = cursor.fetchall()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    return render_template(
        "chart.html",
        categories=categories,
        amounts=amounts
    )


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
