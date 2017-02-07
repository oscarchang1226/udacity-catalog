from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash, session, make_response

import utils
from dummy import items, item, categories, category


def render(template, **params):
    params["categories"] = categories
    return render_template(template, **params)

app = Flask(__name__)


@app.route("/")
def showItems():
    # return "Show recently added items (10)"
    return render("home.html", items=items)


@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == "GET"):
        # return "show register form"
        return render_template("register.html")

    if(request.method == "POST"):
        return redirect(url_for("showItems"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        # return "Login form"
        return render_template("login.html")

    if(request.method == "POST"):
        return redirect(url_for("showItems"))


@app.route("/logout", methods=["POST"])
def logout():
    if(request.method == "POST"):
        return "logout user"


@app.route("/categories/<int:category_id>/items")
def showCategoryItems(category_id):
    return "Show category items"


@app.route("/categories/<int:category_id>/items/new", methods=["GET", "POST"])
def newItem(category_id):
    if(request.method == "GET"):
        return "show new item form"

    if(request.method == "POST"):
        return "add new item"


@app.route("/categories/new", methods=["GET", "POST"])
def newCategory():
    if(request.method == "GET"):
        return "Show new category form"

    if(request.method == "POST"):
        return "Add new category"


@app.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
def editCategory(category_id):
    if(request.method == "GET"):
        return "Show edit category form"

    if(request.method == "POST"):
        return "Update category"


@app.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
def deleteCategory(category_id):
    if(request.method == "GET"):
        return "Show delete category form"

    if(request.method == "POST"):
        return "Delete category and all it's item"


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def editItem(item_id):
    if(request.method == "GET"):
        return "Show item edit form"

    if(request.method == "POST"):
        return "Update item"


@app.route("/items/<int:item_id>/delete", methods=["GET", "POST"])
def deleteItem(item_id):
    if(request.method == "GET"):
        return "delete item form"

    if(request.method == "POST"):
        return "delete item"


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
