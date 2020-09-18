from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
from datetime import datetime
import enum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Role(enum.Enum):
    ADMIN = 0
    USER = 1


class User(BaseModel, UserMixin):
    __tablename__ = "user"

    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    address = Column(String(255))
    phone = Column(String(10))
    user_role = Column(Enum(Role), default=Role.USER)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = "category"

    name = Column(String(50), nullable=False)
    books = relationship("Book", backref='category', lazy=True)

    def __str__(self):
        return self.name


class Author(BaseModel):
    __tablename__ = "author"

    firstname = Column(String(10), nullable=False)
    lastname = Column(String(50), nullable=False)
    dateofbirth = Column(String(10))
    books = relationship("Book", backref='author', lazy=True)

    def __str__(self):
        return self.lastname + " " + self.firstname


class Book(BaseModel):
    __tablename__ = "book"

    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(255), nullable=True)
    view_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    orders = relationship("OrderDetail", backref="book", lazy=True)

    def __str__(self):
        return self.title


class Order(BaseModel):
    __tablename__ = "order"

    name = Column(String(50))
    order_day = Column(DateTime, default=datetime.now())
    ship_address = Column(String(255), nullable=False)
    ship_phone = Column(String(10), nullable=False)
    details = relationship("OrderDetail", backref="order", lazy=True)

    def __str__(self):
        return str(self.id)


class OrderDetail(db.Model):
    __tablename__ = "order_detail"

    order_id = Column(Integer, ForeignKey(Order.id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id), primary_key=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)


if __name__ == "__main__":
    db.create_all()
