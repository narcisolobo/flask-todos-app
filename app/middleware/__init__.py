from functools import wraps
from flask import flash, redirect, session, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in.", "auth")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
