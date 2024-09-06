from flask import Blueprint, render_template

# Decoradores
from ...utils.user_decorators import role_requiered

factura_scope = Blueprint("factura_scope", __name__)

@factura_scope.route('/')
@role_requiered([1, 2])
def factura():
    return render_template('factura/factura.html')
