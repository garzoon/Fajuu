from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from ...controller import *
from ...utils.security import check_password

# Decoradores
from ...utils.user_decorators import role_requiered

auth_scope = Blueprint("auth_scope", __name__)

@auth_scope.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_password = request.form.get('user_password')
        
        usuario = get_usuario_id(user_id)
        
        if usuario and check_password(usuario.user_password, user_password):
            session['user_id'] = usuario.user_id
            session['user_nombre'] = usuario.user_nombre
            session['user_apellido'] = usuario.user_apellido
            session['user_rol'] = usuario.rol_copiaid
            
            if usuario.rol_copiaid == 1:
                print("el usuario es admin")
                return redirect(url_for('auth_scope.admin_home'))
            else:
                print("el usuario es normal")
                return redirect(url_for('auth_scope.user_home'))
            
        else:
            flash("Identificación o contraseña incorrectos", "error")  
            
    return render_template('auth/login.html')

@auth_scope.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('auth_scope.login'))

@auth_scope.route('/home')
@role_requiered([1])
def admin_home():
    
    info_user = usuario_select(session['user_id'])
    return render_template('admin_home.html', info_user = info_user)

@auth_scope.route('/home_user')
@role_requiered([2])
def user_home():
    info_user = usuario_select(session['user_id'])
    return render_template('user_home.html', info_user = info_user)
        