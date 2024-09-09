from flask import session
from src.database.connection import *
from src.controller import * 
from src.models import *
import json

factura = factura_select(1)
productos = json.loads(factura.fact_detalle_productos)

print(productos)