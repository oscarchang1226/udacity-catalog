from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash, session, make_response

import utils
from dummy import items, item, categories, category


def render(template, **params):
    params["categories"] = utils.getCategories()
    if("u-cookie" in session and session["u-cookie"]):
        uid = session["u-cookie"].split("|")[1]
        h = session["u-cookie"].split("|")[0]
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
                salt = utils.generateRandomString()
                user = utils.createUser(
                    email=request.form["email"],
                    salt=salt,
                    hash=utils.generateHash(request.form["password"], salt)
                )
                if(user is None):
                    flash("Failed to register user")
                    return render("register.html")

                flash("Your account is registered!")
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
        email = request.form["email"]
        password = request.form["password"]
        if(email and utils.emailIsValid(email)):
            user = utils.getUserByEmail(email)
            if(user and password):
                print request.form
                try:
                    hash = utils.generateHash(str(password), str(user.salt))
                    credentials = hash == user.hash
                    if(credentials):
                        session["u-cookie"] = "%s|%s" % (user.hash, user.id)
                        return redirect(url_for("home"))
                    else:
                        flash("Credentials don't match. Please try again.")
                except Exception as inst:
                    flash("Something went wrong")
                    print inst
            else:
                if(user):
                    flash("Please enter login credentials.")
                else:
                    flash("Email is not registered.")
        else:
            flash("Email is invalid. Please enter a valid email.")

        return render("login.html", email=email)


@app.route("/logout", methods=["POST"])
def logout():
    if(request.method == "POST"):
        if("u-cookie" in session):
            flash("Logout Successful")
            session.pop("u-cookie")
        return redirect(url_for("home"))


@app.route("/categories/<int:category_id>/items")
def showCategoryItems(category_id):
    category = utils.getCategoryById(category_id)
    if(category):
        items = utils.getItemsByCategoryId(category_id)
        return render(
            "category-items.html", category=category, items=items
        )
    else:
        flash("Specified category not found.")
        return redirect(url_for("home"))


@app.route("/categories/new", methods=["GET", "POST"])
def newCategory():
    if(request.method == "GET"):
        if("u-cookie" not in session):
            flash("Please login to add a new category.")
            return redirect(url_for("login"))
        return render("new-category.html")

    if(request.method == "POST"):
        if("u-cookie" not in session):
            flash("Please login to add a new category.")
            return redirect(url_for("login"))
        params = dict()
        if("category_name" in request.form):
            params["category_name"] = request.form["category_name"]
        if("category_description" in request.form):
            params["category_description"] = request.form[
                                                "category_description"
                                            ]
        if("category_name" in params):
            categoryNameExist = utils.categoryNameExist(
                params["category_name"])
            if(categoryNameExist):
                flash("Category with the same name found. Click <a href=\"%s\">here</a>" % url_for("newItem"))  # NOQA
                return redirect(url_for("newCategory"))
            category_params = dict(
                name=params["category_name"],
                user_id=session["u-cookie"].split("|")[1]
            )
            category = None
            if("category_description" in params):
                category_params["description"] = params["category_description"]
            try:
                category = utils.createCategory(**category_params)
            except Exception as inst:
                flash("Something went wrong. Unable to add category.")
            if(category is None):
                return render("new-category.html", **params)
            else:
                flash("New category added: %s" % category.name)
                return redirect(url_for("newItem", category_id=category.id))
        else:
            flash("Please at least provide name for the category.")
            return redirect(url_for("newCategory"))


@app.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
def editCategory(category_id):
    if(request.method == "GET"):
        return render(
            "edit-category.html",
            category=utils.getCategoryById(category_id)
        )

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
def deleteCategory(category_id):
    if(request.method == "GET"):
        return render("delete-category.html", category=category)

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/items/new", methods=["GET", "POST"])
def newItem():
    if(request.method == "GET"):
        if("u-cookie" not in session):
            flash("Please login to add a new item.")
            return redirect(url_for("login"))
        params = dict()
        if("category_id" in request.args):
            params["category_id"] = int(request.args["category_id"])
        # Categories are already passed in by default.
        return render("new-item.html", **params)

    if(request.method == "POST"):
        if("u-cookie" not in session):
            flash("Please login to add a new item.")
            return redirect(url_for("login"))
        params = dict()
        if("item_name" in request.form):
            params["item_name"] = request.form["item_name"]
        if("item_description" in request.form):
            params["item_description"] = request.form["item_description"]
        if("item_category_id" in request.form):
            params["category_id"] = request.form["item_category_id"]
        if("item_name" in params and "category_id" in params):
            item_params = dict(
                name=params["item_name"],
                category_id=params["category_id"],
                user_id=session["u-cookie"].split("|")[1]
            )
            if("item_description" in params):
                item_params["description"] = params["item_description"]
            new_item = None
            try:
                new_item = utils.createItem(**item_params)
            except Exception as inst:
                flash("Unable to add new item.")
            if(new_item is not None):
                flash("New item added to %s: %s" % (
                    new_item.category.name,
                    new_item.name
                ))
                return redirect(url_for(
                    "showCategoryItems",
                    category_id=new_item.category_id
                ))
            return render("new-item.html", **params)
        else:
            flash("Both item name and item category is required.")
            return render("new-item.html", **params)


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
