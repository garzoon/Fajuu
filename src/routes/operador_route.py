from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import json
from ..controller import *
from ..models import Usuario

operador_scope = Blueprint("operador_scope", __name__)
PATH_URL_USUARIO = "usuario/operador" # Acortador de url

@operador_scope.route('/', methods = ['POST', 'GET'])
def operador():

    connection = create_connection()
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
            parameters.append(f"%{operador_rol}%")
        if operador_estado:
            query += " AND user_estado LIKE %s"
            parameters.append(f"%{operador_estado}%")

    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        operador_list_result = cur.fetchall()

    list_operadores = []
    
    for operador in operador_list_result:
        operador = Usuario(*operador)
        rol = get_user_rol(operador.rol_copiaid)[0][0]
        item_operador = (
                        operador.user_id, 
                        operador.user_nombre,
                        operador.user_apellido,
                        rol,
                        operador.user_estado
                        )
        list_operadores.append(item_operador)

    return render_template(f'{PATH_URL_USUARIO}/operador.html', list_operadores = list_operadores)


@operador_scope.route('/operador_add', methods = ['GET'])
def operador_add():
    return render_template(f'{PATH_URL_USUARIO}/operador_create.html')


@operador_scope.route('/create', methods = ['POST' ,'GET'])
def create():
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
                flash(f"Usuario ({operador_identificacion}) {operador_nombre} {operador_apellido} fue agregado", "success")
                return redirect(url_for('operador_scope.operador'))
            else: 
                flash(f"Ya existe un usuario con el identificador {operador_identificacion}", "error")
        except Exception as ex:
            raise Exception(ex)
            
    
@operador_scope.route('/operador_delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    try:
        operador = Usuario(*usuario_select(id)[0])
        usuario_delete(operador)
        flash(f'Usuario ({operador.user_id}) {operador.user_nombre} {operador.user_apellido} fue eliminado', "success")
        return redirect(url_for('operador_scope.operador'))
    except Exception as ex:
            raise Exception(ex)

@operador_scope.route('/operador_update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        operador_search = Usuario(*usuario_select(id)[0])
        try:
            operador_id = operador_search.user_id
            operador_nombre = request.form.get('operador_nombre')
            operador_apellido = request.form.get('operador_apellido')
            operador_contrasenha = request.form.get('operador_contrasenha')
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
        except Exception as ex:
            raise Exception(ex)
        
    operador = Usuario(*usuario_select(id)[0])

    return render_template(f'{PATH_URL_USUARIO}/operador_update.html', operador = operador)

@operador_scope.route('/operador_details/<int:id>', methods = ['GET'])
def producto_details(id):
    operador = Usuario(*usuario_select(id)[0])
    rol = get_user_rol(operador.rol_copiaid)[0][0]
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
        return jsonify({'Error' : "producto no encontrado"}), 404