from flask import Blueprint, render_template

# Decoradores
from ...utils.user_decorators import role_requiered

usuario_scope = Blueprint("usuario_scope", __name__)

@usuario_scope.route('/', methods = ['POST', 'GET'])
@role_requiered([1])
def usuario():
    return render_template('usuario/usuario.html')

 