from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import json
from datetime import datetime

from ..controller import *
from ..models import Factura

# Decoradores
from ..utils.user_decorators import role_requiered

salida_scope = Blueprint("salida_scope", __name__)

@salida_scope.route('/salida', methods=['POST', 'GET'])
@role_requiered([1, 2])
def salida():

    if 'dic_productos_salida' not in session:
        session['dic_productos_salida'] = {}

    if request.method == 'POST':

        session['cliente_id'] = request.form.get('cliente_id')
        producto_id = request.form.get('producto_id')
        producto_cantidad = request.form.get('producto_cantidad')  

        if not cliente_select(session['cliente_id']):
            flash("Cliente no encontrado", "error")
        elif get_cliente_estado(session['cliente_id']) == 'inactivo':
            flash("Cliente inactivo", "error")
        else:
            if not producto_select(producto_id):
                flash("Producto no encontrado", "error")
            else:   
                if producto_id not in session['dic_productos_salida']:
                    producto = producto_select(producto_id)
                    
                    valor_producto = int(producto.prod_precio) * int(producto_cantidad)
                    
                    producto_array = [producto_id, producto.prod_descripcion, producto_cantidad, producto.prod_unidad_medida, valor_producto]
                    session['dic_productos_salida'][producto_id] = producto_array[1:]

                    if 'factura_valor_total' not in session:
                        session['factura_valor_total'] = 0
                    
                    session['factura_valor_total'] += valor_producto
                    
                    print(session['factura_valor_total'])
                    
                    session.modified = True
                    
                    flash("Producto agregado correctamente", "success")
                else:   
                    flash("Producto ya agregado", "error")
                    
    list_productos = get_productos()
    return render_template('salida.html', dic_productos = session['dic_productos_salida'], cliente_id = session.get('cliente_id', ''), 
                           list_productos = list_productos, total_factura = session.get('factura_valor_total'))
            
@salida_scope.route('/salida_send', methods = ['POST', 'GET'])
@role_requiered([1, 2])
def send_salida ():
    
    # Verifica si las claves existen en la sesión
    cliente_id = session.get('cliente_id')
    if cliente_id is None:
        flash("Faltan datos de cliente", "error")
        return redirect(url_for('salida.salida'))
    
    productos_json = json.dumps(session['dic_productos_salida'])  # Convertir el diccionario Python en un JSON
    current_timestamp = datetime.now()
    current_timestamp_str = current_timestamp.strftime('%Y-%m-%d')
    factura_id = None
    salida = Factura(factura_id, cliente_id, productos_json, session['factura_valor_total'], current_timestamp_str)
    factura_create(salida)
    
    # Actualizar valores de stock del producto en la base de datos
    for key, producto in session['dic_productos_salida'].items():
        resultado = producto_salida(key, producto[1])
        keys_session = ['cliente_id', 'dic_productos_salida', 'factura_valor_total']
        for key in keys_session:
            session.pop(key, None)
        if isinstance(resultado, str):
            resultado
            
            
    return redirect(url_for('salida_scope.salida'))

@salida_scope.route('/salida_delete/<string:id>', methods=['POST'])
@role_requiered([1, 2])
def delete_salida(id):
    if 'dic_productos_salida' in session and id in session['dic_productos_salida']:
        
        valor_del_producto = session['dic_productos_salida'][id][-1]
        del session['dic_productos_salida'][id]
        session['factura_valor_total'] -= valor_del_producto
        session.modified = True     
        
        flash("Producto eliminado correctamente", "success")
    else:
        flash("Producto no encontrado", "error")

    return redirect(url_for('salida_scope.salida'))

@salida_scope.route('/salida_clear', methods=['POST', 'GET'])
@role_requiered([1, 2]) 
def clear_salida():
    keys_session = ['cliente_id', 'dic_productos_salida', 'factura_valor_total']
    for key in keys_session:
        session.pop(key, None)
    return redirect(url_for('salida_scope.salida'))
