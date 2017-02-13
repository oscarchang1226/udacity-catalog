from utils import session, User, Category, Item


def deleteAll():
    session.query(Item).delete()
    session.query(Category).delete()
    session.query(User).delete()
    session.commit()


deleteAll()
