from flask import Blueprint, render_template

usuario_scope = Blueprint("usuario_scope", __name__)

@usuario_scope.route('/', methods = ['POST', 'GET'])
def usuario():
    return render_template('usuario/usuario.html')

 