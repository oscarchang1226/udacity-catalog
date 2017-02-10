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

if(session.query(User).count() > 0):
    print "Deleting Users"
    session.query(User).delete()
    session.commit()


def generateRandomString(n=5):
    """Return random characters with length n"""
    return "".join([random.choice(string.letters) for i in range(n)])


def generateHash(p, salt):
    """Return keyed hashed string with p and salt"""
    return hmac.new(salt, p).hexdigest()


def getAllUsers():
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
