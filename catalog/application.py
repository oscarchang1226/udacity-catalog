from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash, session, make_response

import utils
from dummy import items, item, categories, category


def render(template, **params):
    params["categories"] = categories
    if("u-cookie" in session and session["u-cookie"]):
        uid = session["u-cookie"].split("|")[0]
        h = session["u-cookie"].split("|")[1]
        u = utils.getUserById(uid)
        if(u.hash == h):
            params["user"] = u
        else:
            session.pop("u-cookie", None)
    return render_template(template, **params)


app = Flask(__name__)


@app.route("/")
def home():
    # return "Show recently added items (10)"
    return render("home.html", items=utils.getItems())


@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == "GET"):
        # return "show register form"
        return render("register.html")

    if(request.method == "POST"):
        if(request.form["email"] and request.form["password"] and
           request.form["confirm"]):
            register = True
            if(not utils.emailIsValid(request.form["email"])):
                flash("Please enter valid email.")
                register = False
            if(not utils.passwordIsValid(request.form["password"])):
                flash("Please enter valid password. 3-20 alphanumeric characters.")  # NOQA
                register = False
            if(request.form["password"] != request.form["confirm"]):
                flash("Password not matched.")
                register = False
            if(utils.getUserByEmail(request.form["email"]) is not None):
                flash("Email has been registered.")
                register = False

            if(register):
                flash("Your account is registered!")
                salt = utils.generateRandomString()
                user = utils.createUser(
                    email=request.form["email"],
                    salt=salt,
                    hash=utils.generateHash(request.form["password"], salt)
                )
                session["u-cookie"] = "%s|%s" % (user.hash, user.id)
                return redirect(url_for("home"))
            else:
                return render("register.html", email=request.form["email"])
        else:
            return render("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        # return "Login form"
        if("u-cookie" in session and session["u-cookie"]):
            return redirect(url_for("home"))
        return render("login.html")

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/logout", methods=["POST"])
def logout():
    if(request.method == "POST"):
        return "logout user"


@app.route("/categories/<int:category_id>/items")
def showCategoryItems(category_id):
    return render(
        "category-items.html", category=category, items=items
    )


@app.route("/categories/new", methods=["GET", "POST"])
def newCategory():
    if(request.method == "GET"):
        return render("new-category.html")

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
def editCategory(category_id):
    if(request.method == "GET"):
        return render("edit-category.html", category=category)

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
def deleteCategory(category_id):
    if(request.method == "GET"):
        return render("delete-category.html", categor=category)

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/items/new", methods=["GET", "POST"])
def newItem(category_id):
    if(request.method == "GET"):
        # Categories are already passed in by default.
        return render("new-item.html")

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def editItem(item_id):
    if(request.method == "GET"):
        return render("edit-item.html", item=item)

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/items/<int:item_id>/delete", methods=["GET", "POST"])
def deleteItem(item_id):
    if(request.method == "GET"):
        return render("delete-item.html", item=item)

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/api/categories")
def categoriesApi():
    return "categories in json"


@app.route("/api/categories/<int:category_id>")
def categoryApi(category_id):
    return "category in json"


@app.route("/api/categories/<int:category_id>/items")
def categoryItems(category_id):
    return "category items in json"


@app.route("/api/items/<int:item_id>")
def itemApi(item_id):
    return "item in json"


if __name__ == "__main__":
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
