from flask import session
from src.database.connection import *
from src.controller import * 
from src.models import *
import json

list_proveedores = proveedor_list()
print(list_proveedores)