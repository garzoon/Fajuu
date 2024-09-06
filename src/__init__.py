from flask import Flask, render_template, session
from config import DevelopmentConfig
from .routes import *
from .utils.security import init_bcrypt

from .controller.usuario_controller import usuario_select

app = Flask(__name__, static_folder=DevelopmentConfig.STATIC_FOLDER, template_folder=DevelopmentConfig.TEMPLATE_FOLDER)
app.config.from_object(DevelopmentConfig)
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'

init_bcrypt(app) # Encriptador

# Registro de los blueprints

app.register_blueprint(auth_scope)
app.register_blueprint(entrada_scope, url_prefix='/entrada')
app.register_blueprint(salida_scope, url_prefix='/salida')
app.register_blueprint(perfil_scope, url_prefix='/perfil')

app.register_blueprint(factura_scope, url_prefix='/facturas')
app.register_blueprint(factura_proveedor_scope, url_prefix='/facturas_proveedor')
app.register_blueprint(factura_cliente_scope, url_prefix='/facturas_cliente')

app.register_blueprint(producto_scope, url_prefix='/productos')

app.register_blueprint(usuario_scope, url_prefix='/usuarios')
app.register_blueprint(cliente_scope, url_prefix='/cliente')
app.register_blueprint(proveedor_scope, url_prefix='/proveedor')
app.register_blueprint(operador_scope, url_prefix='/operador')

@app.route('/ayuda')
def helps():
    return render_template('helps.html')


if __name__ == "__main__":
    app.run()