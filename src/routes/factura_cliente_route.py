from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import json

from ..controller import *
from ..models import Cliente, Factura

factura_cliente_scope = Blueprint("factura_cliente_scope", __name__)
PATH_URL_FACT_CLIENTE = "factura/factura_cliente" # Acortador de url

@factura_cliente_scope.route('/', methods = ['POST', 'GET'])
def factura():
    connection = create_connection()
    query = """SELECT * FROM facturas WHERE 1=1"""
    parameters = []

    if request.method == 'POST':
        factura_id = request.form.get('factura_id')
        cliente_id = request.form.get('cliente_id')
        factura_fecha = request.form.get('factura_fecha')

        if factura_id:
            query += " AND fact_id LIKE %s"
            parameters.append(f"%{factura_id}%")

        if cliente_id:
            query += " AND clien_copiaid LIKE %s"
            parameters.append(f"%{cliente_id}%")

        if factura_fecha:
            query += " AND fact_fecha_emision LIKE %s"
            parameters.append(f"%{factura_fecha}%")

    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        factura_list_result = cur.fetchall()

    list_facturas = []
    
    for factura in factura_list_result:
        factura = Factura(*factura)
        cliente = Cliente(*cliente_select(factura.clien_copiaid)[0])
        item_factura = (
            factura.fact_id, 
            factura.clien_copiaid,
            cliente.clien_nombre,
            factura.fact_fecha_emision
        )
        list_facturas.append(item_factura)

    return render_template(f'{PATH_URL_FACT_CLIENTE}/factura_cliente.html', list_facturas = list_facturas)

@factura_cliente_scope.route('/factura_cliente_delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    try:
        factura = Factura(*factura_select(id)[0])
        factura_delete(factura)
        flash(f'Factura de cliente {factura.fact_id} - {factura.clien_copiaid} fue eliminada', "success")
        return redirect(url_for('factura_cliente_scope.factura'))
    
    # Manejo de errores
    except mysql.connector.IntegrityError as ex:
        flash("No se puede eliminar la factura porque está en uso", "error")
    except mysql.connector.Error as ex:
        flash("Error al intentar eliminar la factura", "error")
    except Exception as ex:
        flash(f"Error inesperado: {ex}", "error")
    return redirect(url_for('operador_scope.operador'))

@factura_cliente_scope.route('/factura_cliente_details/<int:id>', methods = ['GET'])
def factura_cliente_details(id):
    factura = Factura(*factura_select(id)[0])
    dic_productos = json.loads(factura.fact_detalle_productos)
    cliente = Cliente(*cliente_select(factura.clien_copiaid)[0])
    if factura and cliente:
        return jsonify({
            'id' : factura.fact_id,
            'cliente_id' : factura.clien_copiaid,
            'nombre' : cliente.clien_nombre,
            'fecha' : factura.fact_fecha_emision,
            'dic_productos' : dic_productos
        })
    else:
        return jsonify({'Error' : "factura no encontrada"}), 404