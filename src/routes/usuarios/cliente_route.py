from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify

from ...controller import *
from ...models import Cliente

cliente_scope = Blueprint("cliente_scope", __name__)
PATH_URL_CLIENTE = "usuario/cliente" # Acortador de url

@cliente_scope.route('/', methods = ['POST', 'GET'])
def cliente():

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
            parameters.append(f"{cliente_estado}")

    cliente_search_result = fetch_all(query, parameters)

    list_cliente = []

    for cliente in cliente_search_result:
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

@cliente_scope.route('/cliente_create', methods = ['POST' ,'GET'])
def create_cliente():
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
            
            if not get_cliente_documento(cliente_identificacion): # Evitar el duplicado de identicacion
                cliente_create(cliente)
                flash(f"Cliente {cliente_identificacion} - {cliente_nombre} fue agregado", "success")
                return redirect(url_for('cliente_scope.cliente'))
            else: 
                flash(f"Ya existe un cliente con identificacion {cliente_identificacion}", "error")
                return redirect(url_for('cliente_scope.cliente_add'))
            
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar crear el cliente", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
            
    return render_template(f'{PATH_URL_CLIENTE}/cliente_create.html')
            
    
@cliente_scope.route('/cliente_delete/<int:id>', methods = ['GET', 'POST'])
def delete_cliente(id):
    try:
        cliente = cliente_select(id)
        cliente_delete(cliente)
        flash(f'Cliente {cliente.clien_id} - {cliente.clien_nombre} fue eliminado', "success")

    # Manejo de errores
    except mysql.connector.IntegrityError as ex:
        flash("No se puede eliminar el cliente porque está en uso", "warning")
    except mysql.connector.Error as ex:
        flash("Error al intentar eliminar el cliente", "warning")
    except Exception as ex:
        flash(f"Error inesperado: {ex}", "warning")
    return redirect(url_for('cliente_scope.cliente'))

@cliente_scope.route('/cliente_update/<int:id>', methods = ['GET', 'POST'])
def update_cliente(id):
    if request.method == 'POST':
        cliente_search = cliente_select(id)
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
            flash("No se puede actualizar el cliente porque está en uso", "warning")
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el cliente", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
        
    cliente = cliente_select(id)

    return render_template(f'{PATH_URL_CLIENTE}/cliente_update.html', cliente = cliente)

@cliente_scope.route('/cliente_details/<int:id>', methods = ['GET'])
def details_cliente(id):
    cliente = cliente_select(id)
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