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
        
    if 'factura_valor_total' not in session:
        session['factura_valor_total'] = 0

    if request.method == 'POST':


        session['cliente_id'] = request.form.get('cliente_id')
        producto_id = request.form.get('producto_id')
        producto_cantidad = request.form.get('producto_cantidad')  
        
        cliente = cliente_select(session['cliente_id'])

        if not cliente:
            flash("Cliente no encontrado", "error")
        elif cliente.clien_estado == 'inactivo':
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
                    
                    session['factura_valor_total'] += valor_producto
                    
                    print(session['factura_valor_total'])
                    
                    session.modified = True
                    
                    flash("Producto agregado correctamente", "success")
                else:   
                    flash("Producto ya agregado", "error")
                    
    list_productos = get_productos()
    list_clientes = cliente_list()
    return render_template('salida.html', dic_productos = session['dic_productos_salida'], cliente_id = session.get('cliente_id', ''), 
                           list_productos = list_productos, list_clientes = list_clientes, total_factura = session.get('factura_valor_total'))
            
@salida_scope.route('/salida_send', methods = ['POST', 'GET'])
@role_requiered([1, 2])
def send_salida():
    
    cliente_id = session.get('cliente_id')
    if cliente_id is None:
        flash("Faltan datos de cliente", "error")
        return redirect(url_for('salida_scope.salida'))
    
    productos_json = json.dumps(session.get('dic_productos_salida', {}))  # Convertir el diccionario Python en un JSON
    
    current_timestamp = datetime.now().strftime('%Y-%m-%d')
    list_check = []
    
    for key, producto in session['dic_productos_salida'].items():
        resultado = producto_check(key, producto[1])
        list_check.append(resultado)
    
    if not all(list_check):
        flash("La factura no pudo ser enviada correctamente debido a problemas de stock", "warning")
        return redirect(url_for('salida_scope.salida'))
    
    salida = Factura(None, cliente_id, productos_json, session['factura_valor_total'], current_timestamp)
    factura_create(salida)
    
    for key, producto in session['dic_productos_salida'].items():
        producto_salida(key, producto[1])
    
    keys_session = ['cliente_id', 'dic_productos_salida', 'factura_valor_total']
    for key in keys_session:
        session.pop(key, None)
    
    flash("Factura enviada con éxito", "success")
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
