from ..database.connection import *
class Producto:
    def __init__(self, prod_id, prod_descripcion, cate_copiaid, prod_unidad_medida, prod_precio, prod_estado, prod_stock):
        self.prod_id = prod_id
        self.prod_descripcion = prod_descripcion
        self.cate_copiaid = cate_copiaid
        self.prod_unidad_medida = prod_unidad_medida
        self.prod_precio = prod_precio
        self.prod_estado = prod_estado
        self.prod_stock = prod_stock
    