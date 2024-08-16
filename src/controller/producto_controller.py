from ..models.producto_model import Producto
from ..database.connection import *


def producto_list() -> Producto:

    query = "SELECT * FROM productos ORDER BY prod_id DESC"

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def producto_select(prod_id) -> Producto:
    if not element_exist('productos', 'prod_id', prod_id):
        raise Exception("Producto no encontrado")
    
    query = "SELECT * FROM producto WHERE prod_id = %s ORDER BY prod_id DESC"
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
                    prov_copiaid, 
                    prod_unidad_medida, 
                    prod_stock, 
                    prod_estado, 
                    prod_precio) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    parameters = (producto.prod_descripcion, 
                  producto.cate_copiaid, 
                  producto.prov_copiaid,  
                  producto.prod_unidad_medida, 
                  producto.prod_stock, 
                  producto.prod_estado, 
                  producto.prod_precio)

    fetch_one(query, parameters)
    return producto


def producto_delete (producto: Producto) -> Producto:
    if not element_exist('productos', 'prod_id', producto.prod_id):
        raise Exception("Producto no encontrado")

    query = "DELETE FROM productos WHERE prod_id = %s"
    parameters = (producto.prod_id)

    fetch_one(query, parameters)
    return producto


def producto_update(producto: Producto) -> Producto:
    if not element_exist('productos', 'prod_id', producto.prod_id):
        raise Exception("Producto no encontrado")

    query = ("""UPDATE productos
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
    parameters = (producto.prod_descripcion, 
                  producto.cate_copiaid, 
                  producto.prov_copiaid, 
                  producto.prod_unidad_medida, 
                  producto.prod_stock, 
                  producto.prod_estado, 
                  producto.prod_precio, 
                  producto.prod_id)
    fetch_one(query, parameters)
    return producto