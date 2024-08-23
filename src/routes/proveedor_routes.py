from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import json
from ..controller import *
from ..models import Usuario

proveedor_scope = Blueprint("proveedor_scope", __name__)
PATH_URL_USUARIO = "usuario/proveedor" # Acortador de url

@proveedor_scope.route('/', methods = ['POST', 'GET'])
def proveedor():
    return render_template(f'{PATH_URL_USUARIO}/proveedor.html')