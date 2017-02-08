from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash, session, make_response

import utils
from dummy import items, item, categories, category


def render(template, **params):
    params["categories"] = categories
    return render_template(template, **params)


app = Flask(__name__)


@app.route("/")
def home():
    # return "Show recently added items (10)"
    return render("home.html", items=items)


@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == "GET"):
        # return "show register form"
        return render("register.html")

    if(request.method == "POST"):
        return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        # return "Login form"
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
