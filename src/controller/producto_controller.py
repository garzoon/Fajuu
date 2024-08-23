from flask import flash
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
    query = """SELECT * FROM productos WHERE prod_id = %s"""
    parameters = (prod_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def producto_create(producto: Producto) -> Producto: 
    query = """INSERT INTO productos 
        (prod_descripcion, 
        cate_copiaid,
        prod_unidad_medida,
        prod_precio) 
        VALUES (%s, %s, %s, %s)
    """
    parameters = (
        producto.prod_descripcion, 
        producto.cate_copiaid, 
        producto.prod_unidad_medida,
        producto.prod_precio
    )

    fetch_query(query, parameters)
    return producto


def producto_delete (producto: Producto) -> Producto:
    query = "DELETE FROM productos WHERE prod_id = %s"
    parameters = (producto.prod_id, )

    fetch_query(query, parameters)
    return "producto"


def producto_update(producto: Producto) -> Producto:
    query = ("""UPDATE productos SET 
        prod_descripcion    = %s, 
        cate_copiaid        = %s, 
        prod_unidad_medida  = %s, 
        prod_stock          = %s, 
        prod_estado         = %s, 
        prod_precio         = %s
        WHERE prod_id = %s
    """)
    parameters = (
        producto.prod_descripcion, 
        producto.cate_copiaid, 
        producto.prod_unidad_medida, 
        producto.prod_stock, 
        producto.prod_estado, 
        producto.prod_precio, 
        producto.prod_id
    )
    fetch_query(query, parameters)
    return producto

def get_estado_producto(prod_id):
    producto = Producto(*producto_select(prod_id)[0])
    if producto.prod_stock > 0:
        return 'disponible'
    else:
        query = "UPDATE productos SET prod_estado = %s WHERE prod_id = %s"
        fetch_query(query, ('agotado', prod_id))
        return 'agotado'

def producto_entrada(prod_id, prod_stock) -> Producto:
    producto = Producto(*producto_select(prod_id)[0])
    new_stock = int(prod_stock) + int(producto.prod_stock)
    query = ("UPDATE productos SET prod_stock = %s WHERE prod_id = %s")
    parameters = (new_stock, prod_id)
    return fetch_query(query, parameters)

def producto_salida(prod_id, prod_stock) -> str:
    if get_estado_producto(prod_id) == 'disponible':   
        producto = Producto(*producto_select(prod_id)[0])
        new_stock = int(producto.prod_stock) - int(prod_stock)
        
        if new_stock < 0:
            return "Stock insuficiente para la operación"
        
        query = "UPDATE productos SET prod_stock = %s WHERE prod_id = %s"
        parameters = (new_stock, prod_id)
        fetch_query(query, parameters)
        
        if new_stock == 0:
            query = "UPDATE productos SET prod_estado = %s WHERE prod_id = %s"
            fetch_query(query, ('agotado', prod_id))
        
        return "Factura de salida agregada"
    else:
        return "Producto agotado"

     
