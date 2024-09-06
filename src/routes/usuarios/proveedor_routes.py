from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from ...controller import *
from ...models import Proveedor

# Decoradores
from ...utils.user_decorators import role_requiered

proveedor_scope = Blueprint("proveedor_scope", __name__)
PATH_URL_PROVEEDOR = "usuario/proveedor" # Acortador de url

@proveedor_scope.route('/', methods = ['POST', 'GET'])
@role_requiered([1])
def proveedor():

    query = """SELECT * FROM proveedor WHERE 1=1"""
    parameters = []

    if request.method == 'POST':
        proveedor_id = request.form.get('proveedor_id')
        proveedor_nit = request.form.get('proveedor_nit')
        proveedor_razonSocial = request.form.get('proveedor_razonSocial')
        proveedor_estado = request.form.get('proveedor_estado')

        if proveedor_id:
            query += " AND prov_id LIKE %s"
            parameters.append(f"%{proveedor_id}%")

        if proveedor_nit:
            query += " AND prov_nit LIKE %s"
            parameters.append(f"%{proveedor_nit}%")

        if proveedor_razonSocial:
            query += " AND prov_razonsocial LIKE %s"
            parameters.append(f"%{proveedor_razonSocial}%")
            
        if proveedor_estado:
            query += " AND prov_estado LIKE %s"
            parameters.append(f"{proveedor_estado}")

    proveedor_list_result = fetch_all(query, parameters)

    list_proveedor = []
    
    for proveedor in proveedor_list_result:
        proveedor = Proveedor(*proveedor)
        item_proveedor = (
            proveedor.prov_id,
            proveedor.prov_nit,
            proveedor.prov_razonsocial,
            proveedor.prov_estado
        )
        list_proveedor.append(item_proveedor)

    return render_template(f'{PATH_URL_PROVEEDOR}/proveedor.html', list_proveedor = list_proveedor)


@proveedor_scope.route('/proveedor_create', methods = ['POST' ,'GET'])
@role_requiered([1])
def create_proveedor():
    if request.method == 'POST':
        try:
            # Asignacion de valores, mediante un reques del front
            proveedor_id = None
            proveedor_nit = request.form.get('proveedor_nit')
            proveedor_razonSocial = request.form.get('proveedor_razonSocial')
            proveedor_email = request.form.get('proveedor_email')
            proveedor_telefono = request.form.get('proveedor_telefono')
            
            # Objeto con base a los valores
            proveedor = Proveedor(
                proveedor_id,
                proveedor_nit,
                proveedor_razonSocial,
                proveedor_email,
                proveedor_telefono
            )
            
            if not get_proveedor_nit(proveedor_nit): # Evitar el duplicado de identicacion
                proveedor_create(proveedor)
                flash(f"Provedor {proveedor_nit} - {proveedor_razonSocial} fue agregado", "success")
                return redirect(url_for('proveedor_scope.proveedor'))
            else: 
                flash(f"Ya existe un proveedor con NIT {proveedor_nit}", "error")
                return redirect(url_for('proveedor_scope.create_proveedor'))
            
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar crear el proveedor", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
    return render_template(f'{PATH_URL_PROVEEDOR}/proveedor_create.html')       
    
@proveedor_scope.route('/proveedor_delete/<int:id>', methods = ['GET', 'POST'])
@role_requiered([1])
def delete_proveedor(id):
    try:
        proveedor = proveedor_select(id)
        proveedor_delete(proveedor)
        flash(f'Proveedor {proveedor.prov_id} - {proveedor.prov_razonsocial} fue eliminado', "success")

    # Manejo de errores
    except mysql.connector.IntegrityError as ex:
        flash("No se puede eliminar el proveedor porque está en uso", "error")
    except mysql.connector.Error as ex:
        flash("Error al intentar eliminar el proveedor", "error")
    except Exception as ex:
        flash(f"Error inesperado: {ex}", "error")
    return redirect(url_for('proveedor_scope.proveedor'))

@proveedor_scope.route('/proveedor_update/<int:id>', methods = ['GET', 'POST'])
@role_requiered([1])
def update_proveedor(id):
    if request.method == 'POST':
        proveedor_search = proveedor_select(id)
        try:
            proveedor_id = proveedor_search.prov_id
            proveedor_nit = request.form.get('proveedor_nit')
            proveedor_razonSocial = request.form.get('proveedor_razonSocial')
            proveedor_email = request.form.get('proveedor_email')
            proveedor_telefono = request.form.get('proveedor_telefono')
            proovedor_estado = request.form.get('proovedor_estado')

            proveedor = Proveedor(
                proveedor_id,
                proveedor_nit,
                proveedor_razonSocial,
                proveedor_email,
                proveedor_telefono,
                proovedor_estado
            )
            proveedor_update(proveedor)

            flash(f"Proveedor {proveedor_id} fue actualizado", "success")
            return redirect(url_for('proveedor_scope.proveedor'))
        
        # Manejo de errores
        except mysql.connector.IntegrityError as ex:
            flash("No se puede actualizar el proveedor porque está en uso", "error")
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el proveedor", "error")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "error")
        
    proveedor = proveedor_select(id)
    return render_template(f'{PATH_URL_PROVEEDOR}/proveedor_update.html', proveedor = proveedor)

@proveedor_scope.route('/proveedor_details/<int:id>', methods = ['GET'])
@role_requiered([1])
def details_proveedor(id):
    proveedor = proveedor_select(id)
    if proveedor:
        return jsonify({
            'id' : proveedor.prov_id,
            'nit' : proveedor.prov_nit,
            'razon_social' : proveedor.prov_razonsocial,
            'email' : proveedor.prov_email,
            'telefono' : proveedor.prov_telefono,
            'estado' : proveedor.prov_estado
        })
    else:
        return jsonify({'Error' : "proveedor no encontrado"}), 404