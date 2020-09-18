from app import db, utils
from sqlalchemy import desc
import hashlib
from datetime import datetime
from app.models import Category, Author, Book, Order, OrderDetail, User, Role


def read_categories():
    return Category.query.all()


def read_authors():
    return Author.query.all()


def read_book_by_id(book_id):
    return Book.query.get(book_id)


def top_seller():
    best = db.session.query(Book.title, Book.image, Book.price, db.func.sum(OrderDetail.price * OrderDetail.quantity).label('sum'))\
        .outerjoin(OrderDetail, Book.id == OrderDetail.book_id)\
        .group_by(Book.id)\
        .order_by(desc('sum'))
    best = best.limit(3).all()

    return best


def read_books(category_id=0, author_id=0, keyword=None, from_price=None, to_price=None, latest=True, most_view=None):
    q = Book.query

    if keyword:
        q = q.filter(Book.title.contains(keyword))

    if from_price and to_price:
        q = q.filter(Book.price.__gt__(from_price), Book.price.__lt__(to_price))

    if category_id > 0:
        q = q.filter(Book.category_id == category_id)

    if author_id > 0:
        q = q.filter(Book.author_id == author_id)

    if most_view:
        q = q.order_by(desc(Book.view_count))

    if latest:
        return q.order_by(Book.updated_at.desc()).limit(5).all()

    return q.all()


def update_book(book_id, title, description, price, image, category_id, author_id):
    try:
        book = Book.query.get(book_id)
        book.title = title
        book.description = description
        book.price = float(price)
        if 'img/' + image.filename != book.image:
            book.image = 'img/' + image.filename
            utils.upload_book_img(image)
        book.updated_at = datetime.now()
        book.category_id = int(category_id)
        book.author_id = int(author_id)

        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def add_book(title, description, price, image, category_id, author_id):
    try:
        book = Book()

        book.title = title
        book.description = description
        book.price = float(price)
        book.image = 'img/' + image.filename
        book.category_id = int(category_id)
        book.author_id = int(author_id)

        utils.upload_book_img(image)

        db.session.add(book)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def delete_book(book_id):
    try:
        book = Book.query.get(book_id)

        db.session.remove(book)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def read_users():
    users = User.query.all()
    return users


def read_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(name, username, password):
    try:
        user = User()

        user.name = name,
        user.username = username,
        user.password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

        db.session.add(user)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def add_order(items, address, phone):
    try:
        o = Order()
        o.ship_address = address
        o.ship_phone = phone
        db.session.add(o)
        db.session.commit()

        for item in items:
            d = OrderDetail()
            d.quantity = item['quantity']
            d.price = item['price']
            d.book_id = item['id']
            d.order_id = o.id

            db.session.add(d)

        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def validate_user(username, password):
    users = read_users()
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

    for user in users:
        if user.username == username and user.password == password:
            return user

    return None


def validate_admin(user):
    if user and user.user_role == Role.ADMIN:
        return True

    return False


if __name__ == "__main__":
    print(read_books())