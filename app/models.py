from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from app import db, admin


class Category(db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    #books = relationship("Book",backref='category',lazy=True)

    def __str__(self):
        return self.name


admin.add_view(ModelView(Category, db.session))


if __name__ == "__main__":
    db.create_all()