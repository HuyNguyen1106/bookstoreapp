from app import admin, db
from app.models import Category, Author, Book, User, Order, OrderDetail, Role
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect


class IsAccessible(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == Role.ADMIN


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
# admin.add_view(OrderView(Order, db.session))
admin.add_view(ODetailView(OrderDetail, db.session))
admin.add_view(LogoutView(name="Logout"))