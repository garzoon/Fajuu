from flask import Flask, render_template, request, redirect, url_for
from config import DevelopmentConfig
from .routes import *
from .security import init_bcrypt

app = Flask(__name__, static_folder=DevelopmentConfig.STATIC_FOLDER, template_folder=DevelopmentConfig.TEMPLATE_FOLDER)
app.config.from_object(DevelopmentConfig)
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'


init_bcrypt(app) # Encriptador

@app.route('/')
def index(): # El index va a redireccionar a login
    return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')


app.register_blueprint(entrada_scope, url_prefix="/entrada")
app.register_blueprint(factura_scope, url_prefix="/facturas")
app.register_blueprint(producto_scope, url_prefix="/producto")
app.register_blueprint(usuario_scope, url_prefix="/usuario")
app.register_blueprint(cliente_scope, url_prefix="/cliente")
app.register_blueprint(proveedor_scope, url_prefix="/proveedor")
app.register_blueprint(operador_scope, url_prefix="/operador")
if __name__ == "__main__":
    app.run()