from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    salt = Column(String(250), nullable=False)
    hash = Column(String(250), nullable=False)
    registered_on = Column(DateTime, default=datetime.datetime.utcnow)
    img_url = Column(String(250))

    @property
    def serialize(self):
        """
            Return object in JSON format
        """
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(User)

    @property
    def serialize(self):
        """
            Return object in JSON format
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(User)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship(Category)

    @property
    def serialize(self):
        """
            Return object in JSON format
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class CategoryVisit(Base):
    __tablename__ = "category_visit"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship(Category)
    visits = Column(Integer, server_default="1")

    @property
    def serialize(self):
        """
            Return object in JSON format
        """
        return {
            "id": self.id,
            "visits": self.visits
        }


class ItemVisit(Base):
    __tablename__ = "item_visit"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    item = relationship(Item)
    visits = Column(Integer, server_default="1")

    @property
    def serialize(self):
        """
            Return object in JSON format
        """
        return {
            "id": self.id,
            "visits": self.visits
        }


engine = create_engine("sqlite:///catalog.db")

Base.metadata.create_all(engine)
