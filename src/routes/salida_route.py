from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import json
from datetime import datetime

from ..controller import *
from ..models import Factura, Producto

salida_scope = Blueprint("salida", __name__)
PATH_URL_SALIDA = "salida" # Acortador de url

@salida_scope.route('/', methods=['POST', 'GET'])
def salida():

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

                # Verificar si el producto ya está en el diccionario
                if producto_id not in session['dic_productos_salida']:
                    producto_array = [producto_id, producto.prod_descripcion, producto_cantidad, producto.prod_unidad_medida]
                    session['dic_productos_salida'][producto_id] = producto_array[1:]
                    session.modified = True
                    flash("Producto agregado correctamente", "success")
                else:   
                    flash("Producto ya agregado", "error")
            else:   
                flash("Producto no encontrado", "error")
        else:   
            flash("Cliente no encontrado", "error")

    return render_template(f'{PATH_URL_SALIDA}/salida.html', dic_productos = session['dic_productos_salida'], cliente_id = session.get('cliente_id', ''))
            
@salida_scope.route('/salida_send', methods = ['POST', 'GET'])
def send_salida ():
    
    # Verifica si las claves existen en la sesión
    cliente_id = session.get('cliente_id')
    if cliente_id is None:
        flash("Faltan datos de cliente", "error")
        return redirect(url_for('salida.salida'))
    
    # Subir entrada a la base de datos
    productos_json = json.dumps(session['dic_productos_salida'])  # Convertir el diccionario Python en un JSON
    current_timestamp = datetime.now()
    current_timestamp_str = current_timestamp.strftime('%Y-%m-%d')
    factura_id = None
    salida = Factura(factura_id, cliente_id, productos_json, current_timestamp_str)
    factura_create(salida)
    
    
    # Actualizar valores de stock del producto en la base de datos
    for key, producto in session['dic_productos_salida'].items():
        resultado = producto_salida(key, producto[1])

        if isinstance(resultado, str):
            flash(resultado, "error")
            
            keys_session = ['cliente_id', 'dic_productos_salida']
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

    return redirect(url_for('salida.salida'))

@salida_scope.route('/salida_clear', methods=['POST', 'GET'])
def clear_salida():
    keys_session = ['cliente_id', 'dic_productos_salida']
    for key in keys_session:
        session.pop(key, None)
    return redirect(url_for('salida.salida'))
