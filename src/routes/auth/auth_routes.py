from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from ...controller import *
from ...utils.security import check_password

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
            session['user_email'] = usuario.user_email
            session['user_telefono'] = usuario.user_telefono
            
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
def admin_home():
    # if 'user_id' in session or session.get('user_rol') != 1:
    #     return redirect(url_for('auth_scope.login'))

    return render_template('admin_home.html')

@auth_scope.route('/home')
def user_home():
    # if 'user_id' in session or session.get('user_rol') != 2:
    #     return redirect(url_for('auth_scope.login'))
    return render_template('user_home.html')
        