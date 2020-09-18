from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from flask_login import login_user, logout_user
from app import app, dao, utils, login
from app.decorator import login_required, admin_required
import json


@app.route("/")
def index():
    return render_template("index.html", latest_books=dao.read_books(latest=True),
                           most_view_books=dao.read_books(latest=True,most_view=True),
                           top_seller=dao.top_seller())


@app.route("/books/search", methods=['get','post'])
def book_search():
    kw = None
    if request.method.lower() == 'post':
        kw = request.form.get("keyword")
    rs = dao.read_books(keyword=kw, latest=None)
    count = len(rs)
    return render_template("book_search.html", result=rs, size=count)


@app.route("/books")
@login_required
@admin_required
def book_list():
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    return render_template("books.html",
                           books=dao.read_books(keyword=kw, from_price=from_price, to_price=to_price))


@app.route("/books/<int:category_id>")
@login_required
@admin_required
def books_by_cate_id(category_id):
    return render_template("books.html",
                           books=dao.read_books(category_id=category_id))


@app.route("/books/<int:author_id>")
@login_required
@admin_required
def books_by_author_id(author_id):
    return render_template("books.html",
                           books=dao.read_books(author_id=author_id))


@app.route("/api/pay", methods=["post"])
def pay():
    if 'cart' in session and session['cart']:
        address = request.form.get("address")
        phone = request.form.get("phone")
        if dao.add_order(session['cart'].values(), address=address, phone=phone):
            del session['cart']
            return jsonify({"status": 200, "message": "successful"})

    return jsonify({"status": 500, "message": "failed"})


# @app.route('/api/paypal', methods=["post"])
# def payByPaypal():
#     if 'cart' in session and session['cart']:
#
#         return jsonify({"status": 200, "message": "successful"})
#
#     return jsonify({"status": 500, "message": "failed"})

@app.route("/books/add", methods=["get", "post"])
@login_required
@admin_required
def add_or_update_book():

    err = ""
    book_id = request.args.get("book_id")
    book = None
    if book_id:
        book = dao.read_book_by_id(book_id=int(book_id))

    if request.method.lower() == "post":
        # name = request.form.get("name")
        # price = request.form.get("price", 0)
        # images = request.form.get("images")
        # description = request.form.get("description")
        # category_id = request.form.get("category_id", 0)
        # import pdb
        # pdb.set_trace()
        if book_id: # Cap nhat
            data = dict(request.form.copy())
            data["book_id"] = book_id
            if dao.update_book(**data, image=request.files["image"]):
                return redirect(url_for("book_list"))
        else: # Them
            if dao.add_book(**dict(request.form), image=request.files["image"]):
                return redirect(url_for("book_list"))

        err = "Something wrong!!! Please back later!"

    return render_template("book-add.html",
                           categories=dao.read_categories(),
                           authors=dao.read_authors(),
                           book=book,
                           err=err)


@app.route("/api/books/<int:book_id>", methods=["delete"])
def delete_book(book_id):
    if dao.delete_book(book_id=book_id):
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": {"book_id": book_id}
        })

    return jsonify({
        "status": 500,
        "message": "Failed"
    })


@app.route("/books/export")
@login_required
@admin_required
def export_book():
    return send_file(utils.export_csv())


@app.route("/login", methods=["get", "post"])
def user_login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.validate_user(username=username, password=password)
        if user:
            login_user(user=user)

            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for("index"))
        else:
            err_msg = "DANG NHAP KHONG THANH CONG"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    return render_template("profile.html",user=dao.read_user_by_id(user_id))


@app.route("/register", methods=["get", "post"])
def register():
    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "The password does not match!"
        else:
            if dao.add_user(name=name, username=username,
                            password=password):
                return redirect(url_for('user_login'))
            else:
                err_msg = "Something wrong!!!"

    return render_template("register.html", err_msg=err_msg)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route("/api/cart", methods=['post'])
def add_to_cart():
    data = json.loads(request.data)
    book_id = data["id"]
    title = data["title"]
    author = data["author"]
    price = data["price"]

    try:
        q, s = utils.add_to_cart(id=book_id, title=title, author=author, price=price)

        return jsonify({"status": 200, "error_message": "successful", "quantity": q, "sum_cart": s})
    except Exception as ex:
        return jsonify({"status": 500, "error_message": str(ex)})


@app.route("/admin")
def admin_index():

    return render_template("admin/index.html")


@app.route("/login-admin", methods=["get","post"])
def login_admin():
    err = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.validate_user(username=username, password=password)
        if dao.validate_admin(user):
            login_user(user=user)
            redirect("/admin")
        else:
            err = "Please login with an admin account!"

    return render_template("admin/index.html", err_msg=err)


@login.user_loader
def user_load(user_id):
    return dao.read_user_by_id(user_id)


@app.context_processor
def common_data():
    q, s = utils.cart_stats()
    return {
        'categories': dao.read_categories(),
        'authors': dao.read_authors(),
        'cart_quantity': q,
        'cart_sum': s,
        'user': Role.USER,
        'admin': Role.ADMIN
    }


if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)


