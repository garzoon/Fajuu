from flask import session
from src.database.connection import *
from src.controller import * 
from src.models import *
import json

producto_id = "10"
producto_cantidad = 12
dic_productos = {}

if not producto_select(producto_id):
    print("Producto no encontrado", "error")       
else:
    if producto_id not in dic_productos:
        producto = producto_select(producto_id)
        producto_array = [producto_id, producto.prod_descripcion, producto_cantidad, producto.prod_unidad_medida]
        dic_productos[producto_id] = producto_array[1:]
        print(dic_productos)
    else:
        print("Producto ya agregado", "error")