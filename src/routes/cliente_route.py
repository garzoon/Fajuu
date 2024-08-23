from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import json
from ..controller import *
from ..models import Usuario

cliente_scope = Blueprint("cliente_scope", __name__)
PATH_URL_USUARIO = "usuario/cliente" # Acortador de url

@cliente_scope.route('/', methods = ['POST', 'GET'])
def cliente():
    return render_template(f'{PATH_URL_USUARIO}/cliente.html')