from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from ..models import Usuario
from ..controller import *

# Decoradores
from ..utils.user_decorators import role_requiered

perfil_scope = Blueprint("perfil_scope", __name__)

@perfil_scope.route('/', methods = ['GET'])
@role_requiered([1, 2])
def perfil():
    list_usuario = usuario_select(session.get('user_id'))
    return render_template('/perfil/perfil.html', list_usuario = list_usuario)

@perfil_scope.route('perfil_update/<int:id>', methods = ['POST', 'GET'])
@role_requiered([1, 2])
def update_perfil(id):
    if request.method == 'POST':
        usuario_search = usuario_select(id)
        
        try:
            user_id = usuario_search.user_id
            user_nombre = request.form.get('user_nombre')
            user_apellido = request.form.get('user_apellido')
            user_password = usuario_search.user_password
            user_email = request.form.get('user_email')
            user_telefono = request.form.get('user_telefono')
            user_rol = usuario_search.rol_copiaid
            user_estado = usuario_search.user_estado
            
            usuario = Usuario(
                user_id,
                user_nombre,
                user_apellido,
                user_password,
                user_email,
                user_telefono,
                user_rol,
                user_estado
            )
            usuario_update(usuario)
            flash(f"Usuario actualizado", "success")
            return redirect(url_for('perfil_scope.perfil'))
            
            
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el producto", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
        
    usuario = usuario_select(id)
    return render_template('/perfil/perfil_update.html', usuario = usuario)

@perfil_scope.route('/perfil_password/<int:id>', methods = ['GET', 'POST'])
@role_requiered([1, 2])
def update_password_usuario(id):
    if request.method == 'POST':
        operador_search = usuario_select(id)

        try:
            operador_old_contrasenha = request.form.get('operador_old_contrasenha')
            operador_contrasenha = request.form.get('operador_contrasenha')

            if check_password(operador_search.user_password, operador_old_contrasenha):
                operador = Usuario(
                    operador_search.user_id, 
                    operador_search.user_nombre, 
                    operador_search.user_apellido, 
                    operador_contrasenha, 
                    operador_search.user_email, 
                    operador_search.user_telefono,
                    operador_search.rol_copiaid, 
                    operador_search.user_estado
                )
                usuario_update(operador)
                flash(f"Usuario actualizado", "success")
                return redirect(url_for('perfil_scope.perfil'))
            else:
                flash("La contraseña es incorrecta", "error")
                return render_template('/perfil/perfil_password.html')
        
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el usuario", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
        
    operador = usuario_select(id)
    return render_template('/perfil/perfil_password.html', operador=operador)

