from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash, session, make_response

import utils
import google_utils

import json
# from dummy import items, item, categories, category


def render(template, **params):
    params["categories"] = utils.getCategories()
    params["google_client_id"] = google_utils.CLIENT_ID
    if("u-cookie" in session and session["u-cookie"]):
        u = utils.checkIfUCookie(session["u-cookie"])
        if(u):
            params["user"] = u
            if("other-acc" in session and session["other-acc"]):
                params["other_acc"] = session["other-acc"]
        else:
            session.pop("u-cookie", None)
            session.pop("other-acc", None)
    return render_template(template, **params)


def needToLogin(message="Please log in to proceed."):
    if("u-cookie" not in session):
        flash(message)
        return redirect(url_for("login"))
    else:
        u = utils.checkIfUCookie(session["u-cookie"])
        if(u is None):
            flash(message)
            return redirect(url_for("login"))


def checkOwner(ownerId):
    uid = int(session["u-cookie"].split("|")[1])
    return ownerId == uid


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
        messages = utils.validateFormForCreateUser(request.form)
        if(len(messages) == 0):
            user_params = utils.initializeUser(request.form)
            user = utils.createUser(**user_params)
            if(user is None):
                flash("Failed to register user")
                return render("register.html")

            flash("Your account is registered!")
            session["u-cookie"] = "%s|%s" % (user.hash, user.id)
            return redirect(url_for("home"))
        else:
            for m in messages:
                flash(m)
            return render("register.html", email=request.form["email"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        # return "Login form"
        if("u-cookie" in session and session["u-cookie"]):
            return redirect(url_for("home"))
        return render("login.html")

    if(request.method == "POST"):
        required = ["email", "password"]
        if(utils.checkForRequiredField(request.form, *required) and
           utils.emailIsValid(request.form["email"])):
            user = utils.getUserByEmail(request.form["email"])
            if(user):
                try:
                    credentials = utils.checkUserCredentials(
                        request.form["email"], request.form["password"]
                    )
                    if(credentials):
                        session["u-cookie"] = "%s|%s" % (user.hash, user.id)
                        return redirect(url_for("home"))
                    else:
                        flash("Credentials don't match. Please try again.")
                except Exception as inst:
                    flash("Something went wrong")
            else:
                flash("Email is not registered.")
        else:
            flash("Please enter your login credentials.")
        return render("login.html", email=request.form["email"])


@app.route("/gconnect", methods=["POST"])
def gconnect():
    if(request.method == "POST"):
        verified, u = google_utils.verify(request.form)
        if(verified):
            user = utils.getUserByEmail(u["email"])
            salt = u["at_hash"]
            hash = utils.generateHash(u["sub"], salt)
            if(user):
                user = utils.updateUserHash(user.id, salt, hash)
                if(user):
                    flash("Login Successful.")
                    session["u-cookie"] = "%s|%s" % (user.hash, user.id)
                    session["other-acc"] = "google"
                else:
                    flash("Failed to login with Google")
            else:
                u["salt"] = salt
                u["password"] = u["sub"]
                user_params = utils.initializeUser(u)
                user = utils.createUser(**user_params)
                if(user):
                    flash("Login Successful.")
                    session["u-cookie"] = "%s|%s" % (user.hash, user.id)
                    session["other-acc"] = "google"
                else:
                    flash("Failed to login with Google")
        else:
            flash("Failed to login with Google.")
        response = make_response(json.dumps(verified), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/logout", methods=["POST"])
def logout():
    if(request.method == "POST"):
        if("u-cookie" in session):
            flash("Logout Successful")
            session.pop("u-cookie")
            session.pop("other-acc")
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
        needToLogin("Please login to add a new category.")
        return render("new-category.html")

    if(request.method == "POST"):
        needToLogin("Please login to add a new category.")
        required = ["name", "user_id"]
        if(utils.checkForRequiredField(request.form, *required)):
            category = utils.categoryNameExist(request.form["name"])
            if(category is not None):
                flash("Category already exist.")
            else:
                category_params = utils.initializeCategory(request.form)
                category = utils.createCategory(**category_params)
                if(category is None):
                    flash("Unable to add category.")
                else:
                    flash("New category added: %s" % category.name)
                    return redirect(url_for(
                        "showCategoryItems", category_id=category.id
                    ))
        else:
            flash("Please provide the name of the category.")
            return render(
                "new-category.html",
                description=request.form["description"]
            )
        return render("new-category.html")


@app.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
def editCategory(category_id):
    if(request.method == "GET"):
        needToLogin("Please log in to edit a category.")
        category = utils.getCategoryById(category_id)
        if(checkOwner(category.user_id)):
            return render(
                "edit-category.html",
                category=utils.getCategoryById(category_id)
            )
        else:
            flash("Unable to edit category that is not created by you.")
            return redirect(url_for(
                "showCategoryItems", category_id=category.id))

    if(request.method == "POST"):
        needToLogin("Please log in to edit a category.")
        category = utils.getCategoryById(category_id)
        same_page_flag = True
        if(checkOwner(category.user_id)):
            required = ["name", "user_id"]
            if(utils.checkForRequiredField(request.form, *required)):
                category = utils.categoryNameExist(request.form["name"])
                if(category is not None and category.id != category_id):
                    flash("Category name already exist.")
                else:
                    same_page_flag = False
                    category_params = utils.initializeCategory(request.form)
                    category = utils.editCategory(
                        category_id, **category_params)
                    if(category is None):
                        flash("Unable to edit category.")
                    else:
                        flash("Category %s edited!" % category.name)
            else:
                flash("Please provide the name of the category.")
        else:
            flash("Unable to edit category that is not created by you.")
            same_page_flag = False

        if(same_page_flag):
            return render("edit-category.html",
                          category=utils.getCategoryById(category_id))
        else:
            return redirect(url_for(
                "showCategoryItems", category_id=category.id))


@app.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
def deleteCategory(category_id):
    if(request.method == "GET"):
        needToLogin("Please log in to delete a category.")
        category = utils.getCategoryById(category_id)
        if(checkOwner(category.user_id)):
            return render("delete-category.html",
                          category=category)
        else:
            flash("Unable to delete a category that is not created by you.")
            return redirect(url_for(
                "showCategoryItems", category_id=category.id))

    if(request.method == "POST"):
        needToLogin("Please log in to delete a category.")
        category = utils.getCategoryById(category_id)
        if(checkOwner(category.user_id)):
            items = utils.getItemsByCategoryId(category_id)
            for item in items:
                utils.deleteItem(item.id)
            utils.deleteCategory(category_id)
            flash("%s deleted along with %s items." % (
                category.name, len(items)
            ))
        else:
            flash("Unable to delete a category that is not created by you.")
        return redirect(url_for("home"))


@app.route("/items/new", methods=["GET", "POST"])
def newItem():
    if(request.method == "GET"):
        needToLogin("Please log in to add an item.")
        params = dict()
        if("category_id" in request.args):
            params["category_id"] = int(request.args["category_id"])
        # Categories are already passed in by default.
        return render("new-item.html", **params)

    if(request.method == "POST"):
        needToLogin("Please log in to add an item.")
        required = ["name", "user_id", "category_id"]
        same_page_flag = True
        params = None
        if(utils.checkForRequiredField(request.form, *required)):
            if(utils.itemNameExist(request.form["name"],
                                   request.form["category_id"])):
                flash("Item with same name found in same category.")
            else:
                same_page_flag = False
                item_params = utils.initializeItem(request.form)
                item = utils.createItem(**item_params)
                if(item is None):
                    flash("Unable to add item.")
                else:
                    flash("New item added: %s." % item.name)
        else:
            flash("Please provide a name and category for the item.")
        if(same_page_flag):
            params = dict(request.form)
            return render("new-item.html", **params)
        else:
            return redirect(url_for("home"))


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def editItem(item_id):
    if(request.method == "GET"):
        needToLogin("Please log in to edit an item.")
        item = utils.getItemById(item_id)
        if(checkOwner(item.user_id)):
            return render("edit-item.html", item=item)
        else:
            flash("Unable to edit item that is not created by you.")
            return redirect(url_for("home"))

    if(request.method == "POST"):
        needToLogin("Please log in to edit an item.")
        required = ["name", "user_id", "category_id"]
        same_page_flag = True
        params = None
        item = utils.getItemById(item_id)
        if(checkOwner(item.user_id)):
            if(utils.checkForRequiredField(request.form, *required)):
                e_item = utils.itemNameExist(
                    request.form["name"],
                    request.form["category_id"])

                if(e_item and e_item.id != item_id):
                    flash("Item name already exist.")
                else:
                    same_page_flag = False
                    item_params = utils.initializeItem(request.form)
                    item = utils.editItem(item_id, **item_params)
                    if(item):
                        flash("%s item edited." % item.name)
                    else:
                        flash("Unable to edit item.")
            else:
                flash("Please provide a name and category for the item.")
        else:
            flash("Unable to edit item that is not created by you.")
            same_page_flag = False
        if(same_page_flag):
            return render("edit-item.html", item=item)
        else:
            return redirect(url_for("home"))


@app.route("/items/<int:item_id>/delete", methods=["GET", "POST"])
def deleteItem(item_id):
    if(request.method == "GET"):
        needToLogin("Please log in to delete an item.")
        item = utils.getItemById(item_id)
        if(checkOwner(item.user_id)):
            return render("delete-item.html", item=item)
        else:
            flash("Unable to delete item that is not created by you.")
            return redirect(url_for("home"))

    if(request.method == "POST"):
        needToLogin("Please log in to delete an item.")
        item = utils.getItemById(item_id)
        if(checkOwner(item.user_id)):
            utils.deleteItem(item_id)
            flash("%s deleted." % item.name)
        else:
            flash("Unable to delete item that is not created by you.")
        return redirect(url_for("home"))


@app.route("/api/categories")
def categoriesApi():
    categories = utils.getCategories()
    return jsonify(categories=[c.serialize for c in categories])


@app.route("/api/categories/<int:category_id>")
def categoryApi(category_id):
    category = utils.getCategoryById(category_id)
    return jsonify(category=category.serialize)


@app.route("/api/categories/<int:category_id>/items")
def categoryItems(category_id):
    items = utils.getItemsByCategoryId(category_id)
    return jsonify(items=[i.serialize for i in items])


@app.route("/api/items/<int:item_id>")
def itemApi(item_id):
    item = utils.getItemById(item_id)
    return jsonify(item=item.serialize)


if __name__ == "__main__":
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
