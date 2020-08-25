from sqlalchemy import Column, Integer, String, Float,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect
from app import db, admin
from flask_login import UserMixin, current_user, logout_user


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books = relationship("Book", backref='category', lazy=True)

    def __str__(self):
        return self.name


class Author(db.Model):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(10), nullable=False)
    lastname = Column(String(50), nullable=False)
    dateofbirth = Column(String(10))
    books = relationship("Book", backref='author', lazy=True)

    def __str__(self):
        return self.lastname + " " + self.firstname


class Book(db.Model):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(255), nullable=True)
    instock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)

    def __str__(self):
        return self.title


class Order(db.Model):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    orderday = Column(String(10))
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)

    def __str__(self):
        return self.name


class OrderDetail(db.Model):
    __tablename__ = "order_detail"

    order_id = Column(Integer, ForeignKey(Order.id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, default=0)

    def __str__(self):
        return self.quantity + "  " + self.price


class IsAccessible(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CategoryView(ModelView, IsAccessible):
    column_display_pk = True
    can_create = True
    form_columns = ("name",)


class AuthorView(ModelView, IsAccessible):
    column_display_pk = True
    can_create = True
    form_columns = ("firstname","lastname","dateofbirth",)


class BookView(ModelView, IsAccessible):
    column_display_pk = True
    can_create = True
    can_export = True


class OrderView(ModelView, IsAccessible):
    column_display_pk = True
    can_create = True
    can_export = True
    can_set_page_size = True


class ODetailView(ModelView, IsAccessible):
    column_display_pk = True
    can_create = True
    can_export = True


class LogoutView(IsAccessible):
    @expose("/")
    def index(self):
        logout_user()

        return redirect("/admin")


admin.add_view(CategoryView(Category, db.session))
admin.add_view(AuthorView(Author, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(OrderView(Order, db.session))
admin.add_view(ODetailView(OrderDetail, db.session))
admin.add_view(LogoutView(name="Logout"))


if __name__ == "__main__":
    db.create_all()
