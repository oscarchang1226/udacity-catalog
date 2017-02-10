from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, User, Category, Item

import string
import random
import hmac

engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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
        email=params["email"], name=params["name"],
        salt=params["salt"], hash=params["hash"]
    )
    try:
        session.add(new_user)
        session.commit()
    except(Exception):
        new_user = None
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


def createCategory(**params):
    """
    Creates a category and returns it
    Return None if fail.
    """
    category = Category(
        name=params["name"], description=params["description"],
        user=params["user"]
    )
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


def editCategory(id, **params):
    """Return edited category"""
    edit_category = getCategoryById(id)
    if(params["name"]):
        edit_category.name = params["name"]
    if(params["description"]):
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
