from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import json
from datetime import datetime

from ..controller import *
from ..models import Entrada, Producto

entrada_scope = Blueprint("entrada", __name__)

@entrada_scope.route('/', methods=['POST', 'GET'])
def entrada():
    # Lista donde se almacenaran los productos con su respectiva informacion
    if 'list_productos' not in session:
        session['list_productos'] = []
    if 'dic_productos' not in session:
        session['dic_productos'] = {}

    if request.method == 'POST':

        session['proveedor_id'] = request.form.get('proveedor_id')
        session['factura_id'] = request.form.get('factura-id')
        producto_id = request.form.get('producto-id')
        producto_cantidad = request.form.get('producto-cantidad')

        # Comprovaciones para evitar recopilar informacion falsa o duplicada
        if proveedor_select_id(session['proveedor_id']):
            if not entrada_select(session['factura_id']):
                if producto_select(producto_id):
                    producto = Producto(*producto_select(producto_id)[0])

                    # Lista de producto
                    producto_array = [producto_id, producto.prod_descripcion, producto_cantidad, producto.prod_unidad_medida]
                    session['list_productos'].append(producto_array)
                    session.modified = True

                    # pasar la lista a un diccionario para tener mayor control de los productos 
                    # en caso de querer eliminar un producto
                    session['dic_productos'] = {i + 1 : producto for i , producto in enumerate(session['list_productos'])}
                else: flash("Producto no encontrado", "error")
            else: flash("Factura ya existe", "error")
        else: flash("Proveedor no encontrado", "error")

    return render_template('entrada.html', dic_productos = session['dic_productos'], provedor_id = session.get('proveedor_id', ''), factura_id = session.get('factura_id', ''))
            
@entrada_scope.route('/entrada_send', methods = ['POST', 'GET'])
def send_entrada ():

    # Verifica si las claves existen en la sesión
    factura_id = session.get('factura_id')
    proveedor_id = session.get('proveedor_id')
    if factura_id is None or proveedor_id is None:
        flash("Faltan datos de factura o proveedor", "error")
        return redirect(url_for('entrada.entrada'))

    # Actualizar valores de stock del producto en la db
    for productos in session['dic_productos'].values():
        producto_entrada(productos[0], productos[2])

    # Subir entrada a la base de datos
    productos_json = json.dumps(session['dic_productos']) # Convertir la lista python en un lista json

    current_timestamp = datetime.now()
    current_timestamp_str = current_timestamp.strftime('%Y-%m-%d')
    entrada = Entrada(factura_id, proveedor_id, productos_json, current_timestamp_str)
    entrada_create(entrada)

    # Limpiar valores de la sesion
    keys_session = ['list_productos', 'factura_id', 'proveedor_id', 'dic_productos']
    for key in keys_session:
        session.pop(key, None)
    flash("Entrada agregada", "success")
    return redirect(url_for('entrada.entrada'))


@entrada_scope.route('/entrada_delete/<string:id>', methods=['POST'])
def delete_entrada(id):
    if 'dic_productos' in session and id in session['dic_productos']:
        del session['dic_productos'][id]
        session.modified = True
        flash("Producto eliminado correctamente", "success")
    else:
        flash("Producto no encontrado", "error")
        print(session['dic_productos'])

    return redirect(url_for('entrada.entrada'))
