from flask import Flask, Blueprint, render_template, redirect, url_for, request
from ..controller.entrada_controller import entrada_create, entrada_delete, entrada_update
from ..models.entrada_model import Entrada

entrada_scope = Blueprint("entrada", __name__)

list_products= []

@entrada_scope.route('/', methods=['GET'])
def entrada():
    return render_template('entrada.html', list_products = list_products)


@entrada_scope.route('/cargar_entrada', methods = ['POST'])
def cargar():
    id_proveedor = request.form.get('inp-idProveedor')
    id_factura = request.form.get('inp-idFactura')
    id_producto = request.form.get('inp-idProducto')
    inp_cantidad_producto = request.form.get('inp-cantidad_producto')

    product = Entrada(None, id_factura, id_proveedor, id_producto, inp_cantidad_producto)

    list_products.append(product)

    print(product)

    return redirect(url_for('entrada.entrada'))

@entrada_scope.route('/enviar_entrada', methods = ['POST'])
def enviar():
    for product in list_products:         
        entrada_create(product)
    return redirect(url_for('entrada.entrada'))