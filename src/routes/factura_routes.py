from flask import Blueprint, render_template

factura_scope = Blueprint("factura_scope", __name__)

@factura_scope.route('/')
def factura():
    return render_template('factura/factura.html')
