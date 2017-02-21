from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from database import Base, User, Category, Item

import string
import random
import hmac
import re
import bleach

PASSWORD_RE = re.compile(r"^[a-zA-Z0-9].{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def emailIsValid(email):
    """Return true if email is valid otherwise false"""
    return EMAIL_RE.match(email) is not None


def passwordIsValid(password):
    """Return true if password is valid otherwise false"""
    return PASSWORD_RE.match(password) is not None


def generateRandomString(n=5):
    """Return random characters with length n"""
    return "".join([random.choice(string.letters) for i in range(n)])


def generateHash(p, salt):
    """Return keyed hashed string with p and salt"""
    return hmac.new(salt, p).hexdigest()


def getUsers():
    """Return a query of users"""
    return session.query(User).order_by(User.registered_on.desc()).all()


def createUser(**params):
    """
    Create user and return new User.
    Return None if failed to add.
    """
    new_user = User(
        email=params["email"],
        salt=params["salt"], hash=params["hash"]
    )
    if("name" in params):
        new_user.name = params["name"]
    try:
        session.add(new_user)
        session.commit()
    except Exception as inst:
        new_user = None
        session.rollback()
        print inst
    return new_user


def getUserByEmail(email):
    """
    Return user with given email.
    Return none if not found.
    """
    user = session.query(User).filter_by(email=email)
    if(user.count() == 0):
        return None
    else:
        return user.one()


def getUserById(id):
    """
    Return User with given id.
    Return none if not found.
    """
    return session.query(User).get(id)


def deleteUser(id):
    """Delete user with given id"""
    user_to_delete = getUserById(id)
    if(user_to_delete is not None):
        session.delete(user_to_delete)
        session.commit()


def getCategories():
    """Get all categories"""
    return session.query(Category).order_by(Category.name).all()


def categoryNameExist(name):
    """
    Check if category name already exist.
    If an item is found, return the item, None otherwise.
    """
    category = None
    try:
        category = session.query(Category).filter(
            func.lower(Category.name) == func.lower(sanitize(name))).one()
    except Exception:
        return None
    return category


def createCategory(**params):
    """
    Creates a category and returns it
    Return None if fail.
    """
    category = Category()
    if("name" in params):
        category.name = params["name"]
    if("description" in params):
        category.description = params["description"]
    if("user_id" in params):
        category.user_id = params["user_id"]

    try:
        session.add(category)
        session.commit()
    except(Exception):
        category = None
    return category


def getCategoriesByUserId(id):
    """Return a list of items created by given user id"""
    return session.query(Category).filter_by(user_id=id).all()


def getCategoryById(id):
    """Return category by given category id"""
    category = session.query(Category).get(id)
    return category


def editCategory(id, **params):
    """Return edited category"""
    edit_category = getCategoryById(id)
    if("name" in params):
        edit_category.name = params["name"]
    if("description" in params):
        edit_category.description = params["description"]
    try:
        session.add(edit_category)
        session.commit()
    except(Exception):
        session.rollback()
        return None
    return edit_category


def deleteCategory(id):
    """Delete an category"""
    delete_category = getCategoryById(id)
    try:
        session.delete(delete_category)
        session.commit()
    except(Exception):
        session.rollback()


def itemNameExist(name, category_id):
    """
    Check if item name exist in a category.
    Return the item if an item is found, None otherwise.
    """
    item = None
    try:
        item = session.query(Item).filter_by(category_id=category_id).filter(
            func.lower(Item.name) == func.lower(name)
        ).one()
    except Exception:
        return None
    return item


def createItem(**params):
    """Create an item."""
    item = Item()
    if("name" in params):
        item.name = params["name"]
    if("description" in params):
        item.description = params["description"]
    if("user_id" in params):
        item.user_id = params["user_id"]
    if("category_id" in params):
        item.category_id = params["category_id"]

    try:
        session.add(item)
        session.commit()
    except Exception:
        session.rollback()
        item = None
    return item


def getItems():
    """Return items ordered by name"""
    return session.query(Item).order_by(Item.name).all()


def getItemsByCategoryId(category_id):
    """Return items under given category"""
    return session.query(Item).filter_by(
        category_id=category_id
    ).all()


def getItemsByUserId(user_id):
    """Return items created by given user"""
    return session.query(Item).filter_by(
        user_id=user_id
    ).all()


def getItemById(id):
    """Return item with given id"""
    item = session.query(Item).get(id)
    return item


def editItem(id, **params):
    """
    Edit an item and return item.
    Return None when exception caught
    """
    item = getItemById(id)
    if("name" in params):
        item.name = params["name"]
    if("description" in params):
        item.description = params["description"]
    try:
        session.add(item)
        session.commit()
    except Exception:
        session.rollback()
        return None
    return item


def deleteItem(id):
    """Delete an item with the given id."""
    delete_item = getItemById(id)
    try:
        session.delete(delete_item)
        session.commit()
    except Exception:
        session.rollback()


def sanitize(text):
    """Sanitize input by striping white spaces and using bleach"""
    try:
        text = text.strip()
        text = bleach.clean(text)
    except Exception:
        pass
    return text


def checkUserCredentials(e, p):
    """
    Check if user credentials are correct.
    Return user if correct, None otherwise.
    """
    user = getUserByEmail(e)
    try:
        hash = generateHash(str(p), str(user.salt))
        if(hash == user.hash):
            return user
    except Exception:
        pass
    return None


def checkIfUCookie(u):
    """
    Check if session u-cookie matches user.
    Return user if so, None otherwise.
    """
    uid = u.split("|")[1]
    user = getUserById(uid)
    try:
        hash = u.split("|")[0]
        if(hash == user.hash):
            return user
    except Exception:
        pass
    return None


def validateFormForCreateUser(form):
    """
    Validate create user form.
    Return error messages as array
    """
    messages = []
    if(getUserByEmail(form["email"]) is not None):
        messages.append("Email has been registered.")
    else:
        if(not emailIsValid(form["email"])):
            messages.append("Please enter valid email.")
        if(not passwordIsValid(form["password"])):
            messages.append(
                "Please enter valid password. 3-20 alphanumeric characters."
            )
        if(form["password"] != form["confirm"]):
            messages.append("Password not matched.")
    return messages


def initializeUser(form):
    """Sanitize and return parameters for a user"""
    try:
        salt = generateRandomString()
        params = dict(
            email=sanitize(form["email"]),
            salt=salt,
            hash=generateHash(sanitize(form["password"]), salt)
        )
        if form["name"]:
            params["name"] = sanitize(form["name"])
        if "img_url" in form and form["img_url"]:
            params["img_url"] = sanitize(form["img_url"])
        return params
    except Exception as inst:
        pass


def initializeCategory(form):
    """Sanitize and return parameters for a category"""
    params = dict(
        name=sanitize(form["name"]),
        user_id=sanitize(form["user_id"])
    )
    if form["description"]:
        params["description"] = sanitize(form["description"])
    return params


def initializeItem(form):
    """Sanitize and returns parameters for an item"""
    params = dict(
        name=sanitize(form["name"]),
        user_id=sanitize(form["user_id"]),
        category_id=sanitize(form["category_id"])
    )
    if form["description"]:
        params["description"] = sanitize(form["description"])
    return params


def checkForRequiredField(form, *fields):
    """Check if all required fields are available"""
    for f in fields:
        if(len(form[f].strip()) == 0):
            return False
    return True
