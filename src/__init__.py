from flask import Flask, render_template, request, redirect, url_for
from config import DevelopmentConfig

from .routes import entrada_scope, factura_scope

app = Flask(__name__, static_folder=DevelopmentConfig.STATIC_FOLDER, template_folder=DevelopmentConfig.TEMPLATE_FOLDER)
app.config.from_object(DevelopmentConfig)

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

if __name__ == "__main__":
    app.run()