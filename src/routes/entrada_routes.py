import flask

entrada = flask.blueprints('entrada', __name__)

@entrada.route('/entrada', methods = ['POST'])
def entrada():
    return flask.jsonify({"Message" : "Hola estoy en entradas"})