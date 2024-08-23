from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import json
from datetime import datetime
from ..controller import *
from ..models import Factura, Producto

salida_scope = Blueprint("salida", __name__)
PATH_URL_SALIDA = "salida" # Acortador de url

@salida_scope.route('/', methods=['POST', 'GET'])
def salida():
    # Lista donde se almacenaran los productos con su respectiva informacion
    if 'list_productos_salida' not in session:
        session['list_productos_salida'] = []
    if 'dic_productos_salida' not in session:
        session['dic_productos_salida'] = {}

    if request.method == 'POST':

        session['cliente_id'] = request.form.get('cliente_id')
        producto_id = request.form.get('producto_id')
        producto_cantidad = request.form.get('producto_cantidad')

        # Comprovaciones para evitar recopilar informacion falsa o duplicada
        if cliente_select(session['cliente_id']):
            if producto_select(producto_id):
                producto = Producto(*producto_select(producto_id)[0])

                # Lista de producto
                producto_array = [producto_id, producto.prod_descripcion, producto_cantidad, producto.prod_unidad_medida]
                session['list_productos_salida'].append(producto_array)
                session.modified = True

                # pasar la lista a un diccionario para tener mayor control de los productos 
                # en caso de querer eliminar un producto
                session['dic_productos_salida'] = {i + 1 : producto for i , producto in enumerate(session['list_productos_salida'])}
            else: flash("Producto no encontrado", "error")
        else: flash("Cliente no encontrado", "error")

    return render_template(f'{PATH_URL_SALIDA}/salida.html', dic_productos = session['dic_productos_salida'], cliente_id = session.get('cliente_id', ''))
            
@salida_scope.route('/salida_send', methods = ['POST', 'GET'])
def send_salida ():
    
    # Verifica si las claves existen en la sesión
    cliente_id = session.get('cliente_id')
    if cliente_id is None:
        flash("Faltan datos de cliente", "error")
        return redirect(url_for('salida.salida'))

    # Actualizar valores de stock del producto en la base de datos
    for productos in session['dic_productos_salida'].values():
        resultado = producto_salida(productos[0], productos[2])

        if isinstance(resultado, str):
            flash(resultado, "error")
            return redirect(url_for('salida.salida'))

    # Subir entrada a la base de datos
    productos_json = json.dumps(session['dic_productos_salida'])  # Convertir el diccionario Python en un JSON
    current_timestamp = datetime.now()
    current_timestamp_str = current_timestamp.strftime('%Y-%m-%d')
    salida = Factura(None, cliente_id, productos_json, current_timestamp_str)
    factura_create(salida)
    
    # Limpiar valores de la sesión
    keys_session = ['list_productos_salida', 'cliente_id', 'dic_productos_salida']
    for key in keys_session:
        session.pop(key, None)
    return redirect(url_for('salida.salida'))


@salida_scope.route('/salida_delete/<string:id>', methods=['POST'])
def delete_salida(id):
    if 'dic_productos_salida' in session and id in session['dic_productos_salida']:
        del session['dic_productos_salida'][id]
        session.modified = True
        flash("Producto eliminado correctamente", "success")
    else:
        flash("Producto no encontrado", "error")
        print(session['dic_productos_salida'])

    return redirect(url_for('salida.salida'))
