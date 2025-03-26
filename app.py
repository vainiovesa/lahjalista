import sqlite3
from flask import Flask
from flask import redirect, render_template, abort, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import giftlists
import config
import gifts
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    if "user_id" not in session:
        hide_list()
    lists = giftlists.get_lists()
    return render_template("index.html", lists = lists)

@app.route("/giftlist/<int:list_id>", methods=["GET", "POST"])
def page(list_id):
    giftlist = giftlists.get_list(list_id)
    gift = gifts.get_gifts(list_id)

    if request.method == "GET":
        return render_template("show_list.html", giftlist=giftlist, gift=gift)

    if request.method == "POST":
        if "show" in request.form:
            password = request.form["password"]
            sql = "SELECT password_hash FROM giftlists WHERE id = ?"
            result = db.query(sql, [list_id])
            password_hash = result[0]["password_hash"]
            if check_password_hash(password_hash, password):
                session["list_id"] = list_id
            return render_template("show_list.html", giftlist=giftlist, gift=gift)

        if "add" in request.form:
            title = request.form["giftname"]            
            try:
                gifts.add_gift(title, list_id)
            except sqlite3.IntegrityError:
                return "VIRHE: listassa ei voi olla kahta samannimistä lahjaa"
            return redirect("/giftlist/" + str(list_id))

        if "delete_gift" in request.form:
            gift_id = request.form["gift_id"]
            gifts.delete_gift(list_id, gift_id)
            return redirect("/giftlist/" + str(list_id))

@app.route("/find_giftlist")
def find_giftlist():
    name = request.args.get("name")
    giftlist_type = request.args.get("type")
    if not giftlist_type:
        giftlist_type = ""
    results = giftlists.find(name, giftlist_type) if name or giftlist_type else []
    if not name:
        name = ""
    return render_template("find.html", name=name, type=giftlist_type, results=results)

@app.route("/new_giftlist")
def new_giftlist():
    return render_template("new_giftlist.html")

@app.route("/create_giftlist", methods=["POST"])
def create_giftlist():
    if "create" in request.form:
        require_login()
        name = request.form["name"]
        giftlist_type = request.form["type"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        user_id = session["user_id"]
        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"
        password_hash = generate_password_hash(password1)
        try:
            giftlists.add_list(name, giftlist_type, user_id, password_hash)
        except sqlite3.IntegrityError:
            abort(403)

    return redirect("/")

@app.route("/edit/<int:list_id>")
def edit(list_id):
    require_login()
    giftlist = giftlists.get_list(list_id)
    if not giftlist:
        abort(404)
    if giftlist["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit.html", giftlist=giftlist)

@app.route("/update_giftlist", methods=["POST"])
def update_giftlist():
    list_id = request.form["list_id"]

    if "save" in request.form:
        require_login()
        name = request.form["name"]
        giftlist_type = request.form["type"]
        giftlists.update_list(list_id, name, giftlist_type)

    return redirect("/giftlist/" + str(list_id))

@app.route("/delete/<int:list_id>")
def delete(list_id):
    require_login()
    giftlist = giftlists.get_list(list_id)
    if not giftlist:
        abort(404)
    if giftlist["user_id"] != session["user_id"]:
        abort(403)
    return render_template("delete.html", giftlist=giftlist)

@app.route("/delete_giftlist", methods=["POST"])
def delete_giftlist():
    list_id = request.form["list_id"]

    if "cancel" in request.form:
        return redirect("/giftlist/" + str(list_id))

    if "delete" in request.form:
        require_login()
        giftlists.delete_list(list_id)
        return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    if "create" in request.form:
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if username == "" or password1 == "" or password2 == "":
            return "VIRHE: tyhjä tunnus tai salasana"
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
    
    if request.method == "POST" and "login" in request.form:
        hide_list()
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])

        if len(result) != 0:
            result = result[0]
        else:
            return "VIRHE: väärä tunnus tai salasana"

        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "Väärä tunnus tai salasana"

    if request.method == "POST" and "cancel" in request.form:
        return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    hide_list()
    return redirect("/")

def require_login():
    if "user_id" not in session:
        abort(403)

def hide_list():
    if "list_id" in session:
        del session["list_id"]
