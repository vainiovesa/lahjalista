import time
import math
import sqlite3
import secrets
import markupsafe
from flask import Flask
from flask import redirect, render_template, abort, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from classes import list_types
import giftlists
import classes
import config
import users
import gifts

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    list_count = giftlists.list_count()
    page_count = math.ceil(list_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    if "user_id" not in session:
        hide_list()
    lists = giftlists.get_lists(page_size, page)
    return render_template("index.html", page=page, page_count=page_count, lists=lists)

@app.route("/giftlist/<int:list_id>", methods=["GET", "POST"])
def listpage(list_id):
    giftlist = giftlists.get_list(list_id)
    if not giftlist:
        abort(404)

    giftlist_gifts = gifts.get_gifts(list_id)

    if request.method == "GET":
        return render_template("show_list.html", giftlist=giftlist, gifts=giftlist_gifts)

    if request.method == "POST":
        if "show" in request.form:
            password = request.form["password"]
            password_hash = giftlists.get_list_passwordhash(list_id)
            if check_password_hash(password_hash, password):
                session["list_id"] = list_id
            else:
                flash("VIRHE: Väärä salasana")
            return render_template("show_list.html", giftlist=giftlist, gifts=giftlist_gifts)

        if "add" in request.form:
            require_login()
            check_csrf()
            title = request.form["giftname"]
            if len(title) > 90 or len(title) < 3:
                abort(403)
            gifts.add_gift(title, list_id)
            return redirect("/giftlist/" + str(list_id))

        if "delete_gift" in request.form:
            require_login()
            check_csrf()
            gift_id = request.form["gift_id"]
            list_of_gift = gifts.get_list_id(gift_id)
            if list_of_gift != list_id:
                abort(403)
            if gifts.reserved(gift_id):
                flash("Lahja on jo varattu!")
            else:
                gifts.delete_gift(list_id, gift_id)
            return redirect("/giftlist/" + str(list_id))

        if "buy" in request.form:
            if not user_is_logged_in():
                flash("Vain rekisteröityneet käyttäjät voivat ilmoittaa ostavansa lahjoja")
                return redirect("/register")
            check_csrf()
            gift_id = request.form["gift_id"]
            list_of_gift = gifts.get_list_id(gift_id)
            gift_has_buyer = gifts.get_buyer(gift_id)
            if list_of_gift != list_id or gift_has_buyer:
                abort(403)
            buyer_id = session["user_id"]
            gifts.buy(gift_id, buyer_id)
            return redirect("/giftlist/" + str(list_id))

        if "cancel-buy" in request.form:
            require_login()
            check_csrf()
            gift_id = request.form["gift_id"]
            buyer_of_gift = gifts.get_buyer(gift_id)
            if buyer_of_gift != session["user_id"]:
                abort(403)
            gifts.cancel_buy(gift_id)
            return redirect("/giftlist/" + str(list_id))

@app.route("/find_giftlist")
def find_giftlist():
    name = request.args.get("name")
    giftlist_type = request.args.get("Lahjalistan tyyppi")
    if not giftlist_type:
        giftlist_type = ""
    results = giftlists.find(name, giftlist_type) if name or giftlist_type else []
    if not name:
        name = ""
    all_classes = classes.get_classes()
    return render_template("find.html", classes=all_classes, name=name,
                           type=giftlist_type, results=results)

@app.route("/new_giftlist")
def new_giftlist():
    all_classes = classes.get_classes()
    return render_template("new_giftlist.html", classes=all_classes, filled={})

@app.route("/create_giftlist", methods=["POST"])
def create_giftlist():
    require_login()
    check_csrf()
    if "name" not in request.form:
        abort(403)
    name = request.form["name"]
    if len(name) > 70 or len(name) < 4:
        abort(403)
    if "Lahjalistan tyyppi" not in request.form:
        abort(403)
    giftlist_type = request.form["Lahjalistan tyyppi"]
    if giftlist_type not in list_types:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if len(password1) < 1:
        abort(403)
    user_id = session["user_id"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        filled = {"name": name}
        return render_template("new_giftlist.html", filled=filled)
    password_hash = generate_password_hash(password1)
    added_classes = [("Lahjalistan tyyppi", giftlist_type)]
    try:
        giftlists.add_list(name, added_classes, user_id, password_hash)
    except sqlite3.IntegrityError:
        flash("Listan luomisessa tapahtui virhe")
        filled = {"name": name}
        return render_template("new_giftlist.html", filled=filled)

    return redirect("/")

@app.route("/edit/<int:list_id>")
def edit(list_id):
    require_login()
    giftlist = giftlists.get_list(list_id)
    if not giftlist:
        abort(404)
    if giftlist["user_id"] != session["user_id"]:
        abort(403)
    all_classes = classes.get_classes()
    return render_template("edit.html", classes=all_classes, giftlist=giftlist, filled={})

@app.route("/update_giftlist", methods=["POST"])
def update_giftlist():
    list_id = request.form["list_id"]
    giftlist = giftlists.get_list(list_id)
    all_classes = classes.get_classes()

    if "save" in request.form:
        require_login()
        check_csrf()
        name = request.form["name"]
        if len(name) > 70 or len(name) < 4:
            flash("VIRHE: Lahjalistan nimen tulee olla 4 - 70 merkkiä pitkä")
            filled = {"name": name}
            return render_template("edit.html", classes=all_classes,
                                   giftlist=giftlist, filled=filled)
        if "Lahjalistan tyyppi" not in request.form:
            flash("VIRHE: Valitse lahjalistan tyyppi")
            filled = {"name": name}
            return render_template("edit.html", classes=all_classes,
                                   giftlist=giftlist, filled=filled)
        giftlist_type = request.form["Lahjalistan tyyppi"]
        if giftlist_type not in list_types:
            abort(403)
        updated_classes = [("Lahjalistan tyyppi", giftlist_type)]
        giftlists.update_list(list_id, name, updated_classes)

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

@app.route("/delete_giftlist/<int:list_id>", methods=["POST"])
def delete_giftlist(list_id):
    if "cancel" in request.form:
        return redirect("/giftlist/" + str(list_id))

    if "delete" in request.form:
        require_login()
        check_csrf()
        giftlists.delete_list(list_id)
        return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if len(username) < 2 or len(username) > 50:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if len(password1) < 1:
        abort(403)
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")
    password_hash = generate_password_hash(password1)
    try:
        users.add(username, password_hash)
        flash("Kirjaudu vielä sisään")
        return redirect("/login")
    except sqlite3.IntegrityError:
        flash("Tunnus on jo varattu")
        return redirect("/register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={})

    if request.method == "POST":
        if "login" in request.form:
            hide_list()
            username = request.form["username"]
            password = request.form["password"]
            result = users.find(username)

            if len(result) != 0:
                result = result[0]
            else:
                flash("VIRHE: väärä tunnus tai salasana")
                filled = {"username": username}
                return render_template("login.html", filled=filled)

            user_id = result["id"]
            password_hash = result["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                session["csrf_token"] = secrets.token_hex(16)
                return redirect("/")
            else:
                flash("VIRHE: väärä tunnus tai salasana")
                filled = {"username": username}
                return render_template("login.html", filled=filled)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
    hide_list()
    return redirect("/")

@app.route("/user/<username>")
def show_user(username):
    user = users.get_user(username)
    buyings = gifts.users_buyings(username)
    if not user:
        abort(404)
    user_id = user["id"]
    lists = users.get_lists(user_id)
    return render_template("user.html", user=user, lists=lists, buyings=buyings)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def require_login():
    if "user_id" not in session:
        abort(403)

def user_is_logged_in():
    return "user_id" in session

def hide_list():
    if "list_id" in session:
        del session["list_id"]

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"] or "csrf_token" not in request.form:
        abort(403)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

if __name__ == "__main__":
    app.run(debug=True)
