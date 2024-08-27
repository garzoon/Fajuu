from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from ...controller import *
from ...models import Usuario

operador_scope = Blueprint("operador_scope", __name__)
PATH_URL_USUARIO = "usuario/operador" # Acortador de url

@operador_scope.route('/', methods = ['POST', 'GET'])
def operador():

    query = """SELECT * FROM usuarios WHERE 1=1"""
    parameters = []

    if request.method == 'POST':
        operador_nombre = request.form.get('operador_nombre')
        operador_apellido = request.form.get('operador_apellido')
        operador_identificacion = request.form.get('operador_identificacion')
        operador_rol = request.form.get('operador_rol')
        operador_estado = request.form.get('operador_estado')

        if operador_nombre:
            query += " AND user_nombre LIKE %s"
            parameters.append(f"%{operador_nombre}%")

        if operador_apellido:
            query += " AND user_apellido LIKE %s"
            parameters.append(f"%{operador_apellido}%")

        if operador_identificacion:
            query += " AND user_id LIKE %s"
            parameters.append(f"%{operador_identificacion}%")

        if operador_rol:
            query += " AND rol_copiaid LIKE %s"
            parameters.append(f"{operador_rol}")
            
        if operador_estado:
            query += " AND user_estado LIKE %s"
            parameters.append(f"{operador_estado}")

    operador_list_result = fetch_all(query, parameters)

    list_operadores = []
    
    for operador in operador_list_result:
        operador = Usuario(*operador)
        rol = get_usuario_rol(operador.rol_copiaid)[0]
        item_operador = (
            operador.user_id, 
            operador.user_nombre,
            operador.user_apellido,
            rol,
            operador.user_estado
        )
        list_operadores.append(item_operador)

    return render_template(f'{PATH_URL_USUARIO}/operador.html', list_operadores = list_operadores)


@operador_scope.route('/operador_create', methods = ['POST' ,'GET'])
def create_operador():
    if request.method == 'POST':
        try:
            # Asignacion de valores, mediante un reques del front
            operador_identificacion = request.form.get('operador_identificacion')
            operador_nombre = request.form.get('operador_nombre')
            operador_apellido = request.form.get('operador_apellido')
            operador_contrasenha = request.form.get('operador_contrasenha')
            operador_email = request.form.get('operador_email')
            operador_telefono = request.form.get('operador_telefono')
            operador_rol = request.form.get('operador_rol')
            
            # Objeto con base a los valores
            operador = Usuario(
                operador_identificacion,
                operador_nombre,
                operador_apellido,
                operador_contrasenha,
                operador_email,
                operador_telefono,
                operador_rol                
            )
            
            if not usuario_select(operador_identificacion): # Evitar el duplicado de identicacion
                usuario_create(operador)
                flash(f"Usuario {operador_identificacion} - {operador_nombre} {operador_apellido} fue agregado", "success")
                return redirect(url_for('operador_scope.operador'))
            
            else: 
                flash(f"Ya existe un usuario con el identificador {operador_identificacion}", "error")
                return redirect(url_for('operador_scope.operador_add'))
            
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar crear el usuario", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
    return render_template(f'{PATH_URL_USUARIO}/operador_create.html')
            
    
@operador_scope.route('/operador_delete/<int:id>', methods = ['GET', 'POST'])
def delete_operador(id):
    try:
        operador = usuario_select(id)
        usuario_delete(operador)
        flash(f'Usuario ({operador.user_id} - {operador.user_nombre} {operador.user_apellido} fue eliminado', "success")
        return redirect(url_for('operador_scope.operador'))
    
    # Manejo de errores
    except mysql.connector.IntegrityError as ex:
        flash("No se puede eliminar el usuario porque está en uso", "warning")
    except mysql.connector.Error as ex:
        flash("Error al intentar eliminar el usuario", "warning")
    except Exception as ex:
        flash(f"Error inesperado: {ex}", "warning")
    return redirect(url_for('operador_scope.operador'))


@operador_scope.route('/operador_update/<int:id>', methods = ['GET', 'POST'])
def update_operador(id):
    if request.method == 'POST':
        operador_search = usuario_select(id)

        try:
            operador_id = operador_search.user_id
            operador_nombre = request.form.get('operador_nombre')
            operador_apellido = request.form.get('operador_apellido')
            operador_contrasenha = operador_search.user_password
            operador_email = request.form.get('operador_email')
            operador_telefono = request.form.get('operador_telefono')
            operador_estado = request.form.get('operador_estado')

            operador = Usuario(
                operador_id, 
                operador_nombre, 
                operador_apellido, 
                operador_contrasenha, 
                operador_email, 
                operador_telefono,
                operador_search.rol_copiaid, 
                operador_estado
            )
            usuario_update(operador)

            flash(f"Usuario {operador_id} fue actualizado", "success")
            return redirect(url_for('operador_scope.operador'))
        
        # Manejo de errores
        except mysql.connector.IntegrityError as ex:
            flash("No se puede actualizar el usuario porque está en uso", "warning")
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el usuario", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
        
    operador = usuario_select(id)
    return render_template(f'{PATH_URL_USUARIO}/operador_update.html', operador = operador)


@operador_scope.route('/operador_password/<int:id>', methods = ['GET', 'POST'])
def update_password_operador(id):
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
                flash(f"Usuario {operador_search.user_id} fue actualizado", "success")
                return redirect(url_for('operador_scope.operador'))
            else:
                flash("La contraseña es incorrecta", "error")
                return render_template(f'{PATH_URL_USUARIO}/operador_password.html')
        
        # Manejo de errores
        except mysql.connector.IntegrityError as ex:
            flash("No se puede actualizar el usuario porque está en uso", "warning")
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el usuario", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
        
    operador = usuario_select(id)
    return render_template(f'{PATH_URL_USUARIO}/operador_password.html', operador=operador)


@operador_scope.route('/operador_details/<int:id>', methods = ['GET'])
def details_operador(id):
    operador = usuario_select(id)
    rol = get_usuario_rol(operador.rol_copiaid)[0]
    if operador:
        return jsonify({
            'id' : operador.user_id,
            'nombre' : operador.user_nombre,
            'apellido' : operador.user_apellido,
            'email' : operador.user_email,
            'telefono' : operador.user_telefono,
            'rol' : rol,
            'estado' : operador.user_estado
        })
    else:
        return jsonify({'Error' : "usuario no encontrado"}), 404