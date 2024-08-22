from flask import Blueprint, render_template, redirect, url_for
import json

# Controllers
from ..controller import *
# Models
from ..models import Proveedor, Cliente


# Registro del blueprint
factura_scope = Blueprint("factura_scope", __name__)

@factura_scope.route('/')
def factura():
    return render_template('factura/factura.html')

# FACTURAS DE PROVEEDOR
PATH_URL_PROVEEDOR = "/factura/factura_proveedor" # Acortador de url

@factura_scope.route('/factura_proveedor', methods=['GET'])
def factura_proveedor():
    list_entradas = []

    for entrada in entrada_list():
        entrada = Entrada(*entrada)
        proveedor = Proveedor(*proveedor_select(entrada.prov_copiaid)[0])
        item_entrada = (
                        entrada.ent_id, 
                        entrada.prov_copiaid, 
                        proveedor.prov_razonsocial, 
                        entrada.ent_fecha_entrada)
        list_entradas.append(item_entrada)

    return render_template(f'{PATH_URL_PROVEEDOR}/factura_proveedor.html', list_entradas = list_entradas)


@factura_scope.route('/factura_proveedor_delete/<int:id>', methods=['GET'])
def factura_proveedor_delete(id):
    entrada = Entrada(*entrada_select(id)[0])
    entrada_delete(entrada)
    return redirect(url_for('factura_scope.factura_proveedor'))


@factura_scope.route('/factura_proveedor_view/<int:id>', methods=['GET'])
def factura_proveedor_view(id):
    entrada = Entrada(*entrada_select(id)[0])
    list_products = json.loads(entrada.ent_detalle_producto)
    if list_products:
        print(list_products)
        return render_template(f'{PATH_URL_PROVEEDOR}/factura_proveedor_view.html', list_products = list_products)
    else:
        raise Exception("Producto de entrada no encontrados")






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


