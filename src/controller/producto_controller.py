from ..models import Producto, Categoria
from ..database.connection import *

def get_product_category(cate_copiaid) -> Categoria:
    query = "SELECT * FROM categorias WHERE cate_id = %s"
    parameters = (cate_copiaid, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()
    

def producto_list() -> Producto:

    query = """SELECT * FROM productos ORDER BY prod_id DESC"""

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def producto_select(prod_id) -> Producto:
    if not element_exist('productos', 'prod_id', prod_id):
        raise Exception("Producto no encontrado")
    
    query = """SELECT * FROM productos WHERE prod_id = %s"""
    parameters = (prod_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def producto_create(producto: Producto) -> Producto:
    if element_exist('productos', 'prod_id', producto.prod_id):
        raise Exception(f"Producto {producto.prod_id}:{producto.prod_descripcion} ya existe")
    
    query = """INSERT INTO productos 
                    (prod_descripcion, 
                    cate_copiaid,
                    prod_unidad_medida,
                    prod_precio) VALUES (%s, %s, %s, %s)"""
    parameters = (producto.prod_descripcion, 
                  producto.cate_copiaid, 
                  producto.prod_unidad_medida,
                  producto.prod_precio)

    fetch_query(query, parameters)
    return producto


def producto_delete (producto: Producto) -> Producto:
    if not element_exist('productos', 'prod_id', producto.prod_id):
        raise Exception("Producto no encontrado")

    query = "DELETE FROM productos WHERE prod_id = %s"
    parameters = (producto.prod_id, )

    fetch_query(query, parameters)
    return "producto"


def producto_update(producto: Producto) -> Producto:
    if not element_exist('productos', 'prod_id', producto.prod_id):
        raise Exception("Producto no encontrado")

    query = ("""UPDATE productos
                SET 
                    prod_descripcion    = %s, 
                    cate_copiaid        = %s, 
                    prod_unidad_medida  = %s, 
                    prod_stock          = %s, 
                    prod_estado         = %s, 
                    prod_precio         = %s
                WHERE prod_id = %s
                """)
    parameters = (producto.prod_descripcion, 
                  producto.cate_copiaid, 
                  producto.prod_unidad_medida, 
                  producto.prod_stock, 
                  producto.prod_estado, 
                  producto.prod_precio, 
                  producto.prod_id)
    fetch_query(query, parameters)
    return producto
