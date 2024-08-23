from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ...models import Usuario
from ...security import Bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')

        user = Usuario.query.filter_by(user_email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.user_id
            session['rol_copiaid'] = user.rol_copiaid
            
            if user.rol_copiaid == 1:  # Asumiendo que 1 es admin y 2 es usuario normal
                return redirect(url_for('admin.dashboard'))
            elif user.rol_copiaid == 2:
                return redirect(url_for('user.dashboard'))
            else:
                flash('Rol no reconocido.', 'danger')
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('auth.login'))
