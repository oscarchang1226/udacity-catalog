from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, User, Category, Item

import string
import random


engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
