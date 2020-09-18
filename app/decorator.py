from flask import session, redirect, url_for, request
from flask_login import current_user
from functools import wraps
from app.models import Role


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("user_login", next=request.url))

        return f(*args, **kwargs)

    return check


def admin_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.user_role == Role.ADMIN:
            return redirect(url_for("user_login", next=request.url))

        return f(*args, **kwargs)

    return check

