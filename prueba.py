from src.database.connection import *
from src.controller import * 
from src.models import *

producto = Producto(*producto_select(1)[0])
print(producto.prod_precio)