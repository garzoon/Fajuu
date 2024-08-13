from models.products_model import Product
from database.connection import *

def list(product: Product) -> Product:
    if not product_exist('prod_id', product.prod_id):
        raise Exception("Producto no encontrado")


def create(product: Product) -> Product:
    if product_exist('prod_id', product.prod_id):
        raise Exception(f"Producto {product.prod_id}:{product.prod_descripcion} ya existe")
    
    query = "INSERT INTO products (prod_descripcion, cate_copiaid, prov_copiaid, prod_unidad_medida, prod_precio) VALUES (%s, %s, %s, %s, %s)"
    parameters = (product.prod_descripcion, product.cate_copiaid, product.prov_copiaid, product.prod_unidad_medida, product.prod_precio)

    fetch_query(query, parameters)
    return product


def delete (product: Product) -> Product:
    if not product_exist('prod_id', product.prod_id):
        raise Exception("Producto no encontrado")

    query = f"DELETE FROM peroductos WHERE prod_id = ?"
    parameters = [product.prod_id]

    fetch_query(query, parameters)
    return product


def update(product: Product) -> Product:
    if not product_exist('prod_id', product.prod_id):
        raise Exception("Producto no encontrado")

    query = ("""UPDATE producto 
                SET 
                    prod_descripcion    = %s, 
                    cate_copiaid        = %s, 
                    prov_copiaid        = %s, 
                    prod_unidad_medida  = %s, 
                    prod_stock          = %s, 
                    prod_estado         = %s, 
                    prod_precio         = %s
                WHERE prod_id = %s
                """)
    parameters = (product.prod_descripcion, product.cate_copiaid, product.prov_copiaid, product.prod_unidad_medida, product.prod_stock, product.prod_estado, product.prod_precio, product.prod_id)
    fetch_query(query, parameters)
    return product