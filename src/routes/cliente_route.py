from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from ..controller import *
from ..models import Cliente

cliente_scope = Blueprint("cliente_scope", __name__)
PATH_URL_CLIENTE = "usuario/cliente" # Acortador de url

@cliente_scope.route('/', methods = ['POST', 'GET'])
def cliente():

    connection = create_connection()
    query = """SELECT * FROM clientes WHERE 1=1"""
    parameters = []

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        cliente_identificacion = request.form.get('cliente_identificacion')
        cliente_nombre = request.form.get('cliente_nombre')
        cliente_ciudad = request.form.get('cliente_ciudad')
        cliente_estado = request.form.get('cliente_estado')

        if cliente_id:
            query += " AND clien_id LIKE %s"
            parameters.append(f"%{cliente_id}%")

        if cliente_identificacion:
            query += " AND clien_documento LIKE %s"
            parameters.append(f"%{cliente_identificacion}%")

        if cliente_nombre:
            query += " AND clien_nombre LIKE %s"
            parameters.append(f"%{cliente_nombre}%")
            
        if cliente_ciudad:
            query += " AND clien_ciudad LIKE %s"
            parameters.append(f"%{cliente_ciudad}%")
            
        if cliente_estado:
            query += " AND clien_estado LIKE %s"
            parameters.append(f"%{cliente_estado}%")

    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        cliente_list_result = cur.fetchall()

    list_cliente = []
    
    for cliente in cliente_list_result:
        cliente = Cliente(*cliente)
        item_cliente = (
            cliente.clien_id,
            cliente.clien_documento,
            cliente.clien_nombre,
            cliente.clien_ciudad,
            cliente.clien_estado
        )
        list_cliente.append(item_cliente)

    return render_template(f'{PATH_URL_CLIENTE}/cliente.html', list_cliente = list_cliente)


@cliente_scope.route('/cliente_add', methods = ['GET'])
def cliente_add():
    return render_template(f'{PATH_URL_CLIENTE}/cliente_create.html')


@cliente_scope.route('/create', methods = ['POST' ,'GET'])
def create():
    if request.method == 'POST':
        try:
            # Asignacion de valores, mediante un reques del front
            cliente_id = None
            cliente_identificacion = request.form.get('cliente_identificacion')
            cliente_nombre = request.form.get('cliente_nombre')
            cliente_ciudad = request.form.get('cliente_ciudad')
            cliente_direccion = request.form.get('cliente_direccion')
            cliente_email = request.form.get('cliente_email')
            cliente_telefono = request.form.get('cliente_telefono')
            
            # Objeto con base a los valores
            cliente = Cliente(
                cliente_id,
                cliente_identificacion,
                cliente_nombre,
                cliente_ciudad,
                cliente_direccion,
                cliente_email,
                cliente_telefono
            )
            
            if not cliente_select_document(cliente_identificacion): # Evitar el duplicado de identicacion
                cliente_create(cliente)
                flash(f"Cliente {cliente_identificacion} - {cliente_nombre} fue agregado", "success")
                return redirect(url_for('cliente_scope.cliente'))
            else: 
                flash(f"Ya existe un cliente con identificacion {cliente_identificacion}", "error")
                return redirect(url_for('cliente_scope.cliente_add'))
            
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar crear el cliente", "error")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "error")
        return redirect(url_for('cliente_scope.cliente'))
            
    
@cliente_scope.route('/cliente_delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    try:
        cliente = Cliente(*cliente_select(id)[0])
        cliente_delete(cliente)
        flash(f'Cliente {cliente.clien_id} - {cliente.clien_nombre} fue eliminado', "success")

    # Manejo de errores
    except mysql.connector.IntegrityError as ex:
        flash("No se puede eliminar el cliente porque está en uso", "error")
    except mysql.connector.Error as ex:
        flash("Error al intentar eliminar el cliente", "error")
    except Exception as ex:
        flash(f"Error inesperado: {ex}", "error")
    return redirect(url_for('cliente_scope.cliente'))

@cliente_scope.route('/cliente_update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        cliente_search = Cliente(*cliente_select(id)[0])
        try:
            cliente_id = cliente_search.clien_id
            cliente_identificacion = request.form.get('cliente_identificacion')
            cliente_nombre = request.form.get('cliente_nombre')
            cliente_ciudad = request.form.get('cliente_ciudad')
            cliente_direccion = request.form.get('cliente_direccion')
            cliente_email = request.form.get('cliente_email')
            cliente_telefono = request.form.get('cliente_telefono')
            cliente_estado = request.form.get('cliente_estado')

            cliente = Cliente(
                cliente_id,
                cliente_identificacion,
                cliente_nombre,
                cliente_ciudad,
                cliente_direccion,
                cliente_email,
                cliente_telefono,
                cliente_estado
            )
            cliente_update(cliente)

            flash(f"Cliente {cliente_id} fue actualizado", "success")
            return redirect(url_for('cliente_scope.cliente'))
        
        # Manejo de errores
        except mysql.connector.IntegrityError as ex:
            flash("No se puede actualizar el cliente porque está en uso", "error")
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el cliente", "error")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "error")
        
    cliente = Cliente(*cliente_select(id)[0])

    return render_template(f'{PATH_URL_CLIENTE}/cliente_update.html', cliente = cliente)

@cliente_scope.route('/cliente_details/<int:id>', methods = ['GET'])
def cliente_details(id):
    cliente = Cliente(*cliente_select(id)[0])
    if cliente:
        return jsonify({
            'id' : cliente.clien_id,
            'documento' : cliente.clien_documento,
            'nombre' : cliente.clien_nombre,
            'ciudad' : cliente.clien_ciudad,
            'direccion' : cliente.clien_direccion,
            'email' : cliente.clien_email,
            'telefono' : cliente.clien_telefono,
            'estado' : cliente.clien_estado
        })
    else:
        return jsonify({'Error' : "cliente no encontrado"}), 404