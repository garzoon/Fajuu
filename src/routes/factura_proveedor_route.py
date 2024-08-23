from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import json

from ..controller import *
from ..models import Proveedor, Entrada

factura_proveedor_scope = Blueprint("factura_proveedor_scope", __name__)
PATH_URL_FACT_PROVEEDOR = "factura/factura_proveedor" # Acortador de url

@factura_proveedor_scope.route('/', methods = ['POST', 'GET'])
def factura():

    connection = create_connection()
    query = """SELECT * FROM entradas WHERE 1=1"""
    parameters = []

    if request.method == 'POST':
        entrada_id = request.form.get('entrada_id')
        proveedor_id = request.form.get('proveedor_id')
        entrada_fecha = request.form.get('entrada_fecha')

        if entrada_id:
            query += " AND ent_id LIKE %s"
            parameters.append(f"%{entrada_id}%")

        if proveedor_id:
            query += " AND prov_copiaid LIKE %s"
            parameters.append(f"%{proveedor_id}%")

        if entrada_fecha:
            query += " AND ent_fecha_entrada LIKE %s"
            parameters.append(f"%{entrada_fecha}%")

    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        entrada_list_result = cur.fetchall()

    list_entradas = []
    
    for entrada in entrada_list_result:
        entrada = Entrada(*entrada)
        proveedor = Proveedor(*proveedor_select_id(entrada.prov_copiaid)[0])
        item_entrada = (
            entrada.ent_id, 
            entrada.prov_copiaid,
            proveedor.prov_razonsocial,
            entrada.ent_fecha_entrada
        )
        list_entradas.append(item_entrada)

    return render_template(f'{PATH_URL_FACT_PROVEEDOR}/factura_proveedor.html', list_entradas = list_entradas)


@factura_proveedor_scope.route('/factura_proveedor_delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    try:
        entrada = Entrada(*entrada_select(id)[0])
        entrada_delete(entrada)
        flash(f'Factura de proveedor {entrada.ent_id} - {entrada.prov_copiaid} fue eliminada', "success")
        return redirect(url_for('factura_proveedor_scope.factura'))
    
    # Manejo de errores
    except mysql.connector.IntegrityError as ex:
        flash("No se puede eliminar la factura porque está en uso", "error")
    except mysql.connector.Error as ex:
        flash("Error al intentar eliminar la factura", "error")
    except Exception as ex:
        flash(f"Error inesperado: {ex}", "error")
    return redirect(url_for('operador_scope.operador'))

@factura_proveedor_scope.route('/factura_proveedor_details/<int:id>', methods = ['GET'])
def factura_proveedor_details(id):
    entrada = Entrada(*entrada_select(id)[0])
    dic_productos = json.loads(entrada.ent_detalle_producto)
    proveedor = Proveedor(*proveedor_select_id(entrada.prov_copiaid)[0])
    if entrada and proveedor:
        return jsonify({
            'id' : entrada.ent_id,
            'proveedor_id' : entrada.prov_copiaid,
            'razon_social' : proveedor.prov_razonsocial,
            'fecha' : entrada.ent_fecha_entrada,
            'dic_productos' : dic_productos
        })
    else:
        return jsonify({'Error' : "factura no encontrado"}), 404