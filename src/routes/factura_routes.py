from flask import Flask, Blueprint, render_template, redirect, url_for, request, jsonify

# Controllers
from ..controller.factura_controller import factura_list, factura_create, factura_delete, factura_update
from ..controller.entrada_controller import entrada_list, entrada_delete, entrada_update, entrada_select
from ..controller.proveedor_controller import proveedor_select
from ..controller.cliente_controller import cliente_select, fullname

from ..models import Proveedor, Cliente

factura_scope = Blueprint("factura_scope", __name__)

@factura_scope.route('/')
def factura():
    return render_template('factura/factura.html')





# FACTURAS DE PROVEEDOR

@factura_scope.route('/factura_proveedor', methods=['POST', 'GET'])
def factura_proveedor():
    # busqueda de factura de un proveedor
    list_entradas = []

    for i in entrada_list():
        proveedor = (proveedor_select(i[1]))
        proveedor = Proveedor(*proveedor[0]) # El operador * separa cada elemento de una tupla
        item_entrada = (i[0], i[1], proveedor.prov_razonsocial, i[3])
        list_entradas.append(item_entrada)
    return render_template('/factura/factura_proveedor/factura_proveedor.html', data = list_entradas)

@factura_scope.route('/factura_proveedor_delete/<int:id>', methods=['POST', 'GET'])
def factura_proveedor_delete(id):
    entrada_delete(id)
    return redirect(url_for('factura_scope.factura_proveedor'))
    
@factura_scope.route('/factura_proveedor_view/<int:id>', methods=['GET'])
def factura_proveedor_view(id):
    entrada = entrada_select(id)
    if entrada is None:
        return jsonify({"error": "Factura no encontrada"}), 404
    return jsonify(entrada)





# FACTURAS DE CLIENTE

@factura_scope.route('/factura_cliente', methods=['POST', 'GET'])
def factura_cliente():
    # busqueda de factura de un cliente

    list_facturas = []

    for i in factura_list():
        cliente = cliente_select(i[1])
        cliente = Cliente(*cliente[0])
        item_factura = (i[0], i[1], fullname(cliente), i[3], i[4], i[5])

        list_facturas.append(item_factura)

    return render_template('/factura/factura_cliente.html', data = list_facturas)



@factura_scope.route('/factura_volver', methods=['POST'])
def factura_volver():
    return render_template('factura/factura.html')


