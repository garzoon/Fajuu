from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import json
from datetime import datetime

from ..controller import *
from ..models import Entrada

# Decoradores
from ..utils.user_decorators import role_requiered

entrada_scope = Blueprint("entrada_scope", __name__)

@entrada_scope.route('/', methods=['POST', 'GET'])
@role_requiered([1, 2])
def entrada():
    # Inicializa diccionario de productos si no existe
    
    if 'dic_productos' not in session:
        session['dic_productos'] = {}

    if request.method == 'POST':
        
        session['proveedor_id'] = request.form.get('proveedor_id')
        session['factura_id'] = request.form.get('factura_id')
        producto_id = request.form.get('producto_id')
        producto_cantidad = request.form.get('producto_cantidad')

        proveedor = proveedor_select(session['proveedor_id'])

        if not proveedor:
            flash("Proveedor no encontrado", "error")
        elif proveedor.prov_estado == 'inactivo':
            flash("Proveedor inactivo", "error")
        else:
            if entrada_select(session['factura_id']):
                flash("Factura ya existe", "error")
            else:
                if not producto_select(producto_id):
                    flash("Producto no encontrado", "error")       
                else:
                    if producto_id not in session['dic_productos']:
                        producto = producto_select(producto_id)
                        producto_array = [producto_id, producto.prod_descripcion, producto_cantidad, producto.prod_unidad_medida]
                        session['dic_productos'][producto_id] = producto_array[1:]
                        session.modified = True
                        
                        print(session['dic_productos'])
                        flash("Producto agregado correctamente", "success")
                    else:
                        flash("Producto ya agregado", "error")
                        
    
    list_productos = get_productos()
    list_proveedores = proveedor_list()
    return render_template('entrada.html', dic_productos = session['dic_productos'], proveedor_id = session.get('proveedor_id', ''), 
                           factura_id = session.get('factura_id', ''), list_productos = list_productos, list_proveedores = list_proveedores)

            
@entrada_scope.route('/entrada_send', methods = ['POST', 'GET'])
@role_requiered([1, 2])
def send_entrada ():

    # Verifica si las claves existen en la sesión
    factura_id = session.get('factura_id')
    proveedor_id = session.get('proveedor_id')
    if factura_id is None or proveedor_id is None:
        flash("Faltan datos de factura o proveedor", "error")
        return redirect(url_for('entrada_scope.entrada'))

    # Subir entrada a la base de datos
    productos_json = json.dumps(session['dic_productos']) # Convertir la lista python en un lista json

    current_timestamp = datetime.now()
    current_timestamp_str = current_timestamp.strftime('%Y-%m-%d')
    entrada = Entrada(factura_id, proveedor_id, productos_json, current_timestamp_str)
    entrada_create(entrada)
    
    # Actualizar valores de stock del producto en la db
    for key, producto in session['dic_productos'].items():
        producto_entrada(key, producto[1])

    # Limpiar valores de la sesion
    keys_session = ['factura_id', 'proveedor_id', 'dic_productos']
    for key in keys_session:
        session.pop(key, None)
    flash("Factura de entrada agregada", "success")
    return redirect(url_for('entrada_scope.entrada'))


@entrada_scope.route('/entrada_delete/<string:id>', methods=['POST'])
@role_requiered([1, 2])
def delete_entrada(id):
    if 'dic_productos' in session and id in session['dic_productos']:
        del session['dic_productos'][id]
        session.modified = True
        
        print(session['dic_productos'])
        flash("Producto eliminado correctamente", "success")
    else:
        flash("Producto no encontrado", "error")

    return redirect(url_for('entrada_scope.entrada'))


@entrada_scope.route('/entrada_clear', methods=['POST', 'GET'])
@role_requiered([1, 2])
def clear_entrada():
    keys_session = ['factura_id', 'proveedor_id', 'dic_productos']
    for key in keys_session:
        session.pop(key, None)
    flash("Factura de entrada descartada", "success")
    return redirect(url_for('entrada_scope.entrada'))
