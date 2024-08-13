from flask import Flask, render_template, request, redirect, url_for
from config import Config

app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)

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


@app.route('/entrada', methods = ['POST'])
def entrada():
    return render_template('entrada.html')






if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(debug=True, port=5000)

