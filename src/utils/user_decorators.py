from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Inicie sesión para acceder a esta página")
            return redirect(url_for('auth_scope.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_requiered(roles):
    def decorator(f):
        @wraps(f)
        @login_required 
        def decorated_function(*args, **kwargs):
            if session.get('user_rol') not in roles:
                flash("No tienes permiso para acceder a esta pagina")
                return redirect(url_for('auth_scope.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator