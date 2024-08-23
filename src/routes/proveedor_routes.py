from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from ..controller import *
from ..models import Proveedor

proveedor_scope = Blueprint("proveedor_scope", __name__)
PATH_URL_PROVEEDOR = "usuario/proveedor" # Acortador de url

@proveedor_scope.route('/', methods = ['POST', 'GET'])
def proveedor():

    connection = create_connection()
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
            parameters.append(f"%{proveedor_estado}%")

    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        proveedor_list_result = cur.fetchall()

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


@proveedor_scope.route('/proveedor_add', methods = ['GET'])
def proveedor_add():
    return render_template(f'{PATH_URL_PROVEEDOR}/proveedor_create.html')


@proveedor_scope.route('/create', methods = ['POST' ,'GET'])
def create():
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
            
            if not proveedor_select_nit(proveedor_nit): # Evitar el duplicado de identicacion
                proveedor_create(proveedor)
                flash(f"Provedor {proveedor_nit} - {proveedor_razonSocial} fue agregado", "success")
                return redirect(url_for('proveedor_scope.proveedor'))
            else: 
                flash(f"Ya existe un proveedor con NIT {proveedor_nit}", "error")
                return redirect(url_for('proveedor_scope.proveedor_add'))
            
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar crear el proveedor", "error")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "error")
        return redirect(url_for('proveedor_scope.proveedor'))
            
    
@proveedor_scope.route('/proveedor_delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    try:
        proveedor = Proveedor(*proveedor_select_id(id)[0])
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
def update(id):
    if request.method == 'POST':
        proveedor_search = Proveedor(*proveedor_select_id(id)[0])
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
        
    proveedor = Proveedor(*proveedor_select_id(id)[0])

    return render_template(f'{PATH_URL_PROVEEDOR}/proveedor_update.html', proveedor = proveedor)

@proveedor_scope.route('/proveedor_details/<int:id>', methods = ['GET'])
def proveedor_details(id):
    proveedor = Proveedor(*proveedor_select_id(id)[0])
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