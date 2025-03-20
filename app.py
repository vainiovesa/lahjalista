import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import giftlists
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    lists = giftlists.get_lists()
    return render_template("index.html", lists = lists)

@app.route("/giftlist/<int:list_id>")
def page(list_id):
    giftlist = giftlists.get_list(list_id)
    return render_template("show_list.html", giftlist = giftlist)

@app.route("/new_giftlist")
def new_giftlist():
    return render_template("new_giftlist.html")

@app.route("/create_giftlist", methods=["POST"])
def create_giftlist():
    name = request.form["name"]
    giftlist_type = request.form["type"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    user_id = session["user_id"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)
    giftlists.add_list(name, giftlist_type, user_id, password_hash)
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # TODO. Throws exception, if trying to log in with non-existent username
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")