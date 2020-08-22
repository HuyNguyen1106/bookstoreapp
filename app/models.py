from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from app import db, admin


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
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)

    def __str__(self):
        return self.title


admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Author, db.session))
admin.add_view(ModelView(Book, db.session))

if __name__ == "__main__":
    db.create_all()
