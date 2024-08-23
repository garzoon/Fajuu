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

def get_estado_producto(prod_id) -> str:
    producto = producto_select(prod_id)
    if not producto:
        return None  # o algún valor indicativo si el producto no existe

    producto = Producto(*producto[0])
    if producto.prod_stock > 0:
        return 'disponible'
    return 'agotado'

def update_producto_estado(prod_id, estado) -> None:
    query = "UPDATE productos SET prod_estado = %s WHERE prod_id = %s"
    fetch_query(query, (estado, prod_id))

def producto_entrada(prod_id, prod_stock) -> None:
    producto = producto_select(prod_id)
    if not producto:
        return

    producto = Producto(*producto[0])
    new_stock = int(prod_stock) + int(producto.prod_stock)
    query = "UPDATE productos SET prod_stock = %s WHERE prod_id = %s"
    fetch_query(query, (new_stock, prod_id))

    # Actualizar el estado si es necesario
    if new_stock > 0:
        update_producto_estado(prod_id, 'disponible')

def producto_salida(prod_id, prod_stock) -> str:
    producto = Producto(*producto_select(prod_id)[0])
    
    if get_estado_producto(prod_id) == 'disponible': 
        # Verificar si el stock a retirar es menor o igual al stock actual
        if int(prod_stock) <= int(producto.prod_stock):
            new_stock = int(producto.prod_stock) - int(prod_stock)

            # Actualizar stock si es mayor que 0
            if new_stock > 0:
                query = "UPDATE productos SET prod_stock = %s WHERE prod_id = %s"
                parameters = (new_stock, prod_id)
                fetch_query(query, parameters)
                return "Stock actualizado con éxito"

            # Si el stock es 0 después de la operación, actualizar estado a 'agotado'
            elif new_stock == 0:
                update_producto_estado(prod_id, 'agotado')
                query = "UPDATE productos SET prod_stock = %s WHERE prod_id = %s"
                parameters = (new_stock, prod_id)
                fetch_query(query, parameters)
                return f"Producto {producto.prod_descripcion} agotado tras la salida"

        else:
            return f"Stock insuficiente para retirar {prod_stock} unidades de {producto.prod_descripcion}"
    
    else:
        return f"Producto {producto.prod_descripcion} ya está agotado"


     
