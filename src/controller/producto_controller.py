from flask import flash
from ..models import Producto, Categoria
from ..database.connection import *

def producto_list():
    query = """SELECT * FROM productos ORDER BY prod_id DESC"""
    return fetch_all(query)

def producto_select(prod_id):
    query = """SELECT * FROM productos WHERE prod_id = %s"""
    parameters = (prod_id, )
    result = fetch_one(query, parameters)
    if result:
        return Producto(*result)
    return None 

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
    execute_commit(query, parameters)
    return producto


def producto_delete (producto: Producto) -> Producto:
    query = "DELETE FROM productos WHERE prod_id = %s"
    parameters = (producto.prod_id, )
    execute_commit(query, parameters)
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
    execute_commit(query, parameters)
    return producto

def get_productos():
    query = "SELECT prod_id, prod_descripcion FROM productos "
    return fetch_all(query)

def get_producto_categoria(cate_copiaid):
    query = "SELECT * FROM categorias WHERE cate_id = %s"
    parameters = (cate_copiaid, )
    result = fetch_one(query, parameters)
    if result:
        return Categoria(*result)
    return None 


def get_producto_estado(prod_id) -> str:
    producto = producto_select(prod_id)
    if not producto:
        return None 

    if producto.prod_stock > 0:
        return 'disponible'
    return 'agotado'

def update_producto_estado(prod_id, estado) -> None:
    query = "UPDATE productos SET prod_estado = %s WHERE prod_id = %s"
    parameters = (estado, prod_id)
    execute_commit(query, parameters)

def producto_entrada(prod_id, prod_stock) -> None:
    producto = producto_select(prod_id)
    if not producto:
        return "Producto no existe"

    new_stock = int(prod_stock) + int(producto.prod_stock)
    query = "UPDATE productos SET prod_stock = %s WHERE prod_id = %s"
    parameters = (new_stock, prod_id)
    execute_commit(query, parameters)

    if new_stock > 0:
        update_producto_estado(prod_id, 'disponible')

def producto_salida(prod_id, prod_stock) -> str:
    producto = producto_select(prod_id)
    
    if get_producto_estado(prod_id) == 'disponible': 
        # Verificar si el stock a retirar es menor o igual al stock actual
        if int(prod_stock) <= int(producto.prod_stock):
            new_stock = int(producto.prod_stock) - int(prod_stock)

            # Actualizar stock si es mayor que 0
            if new_stock > 0:
                query = "UPDATE productos SET prod_stock = %s WHERE prod_id = %s"
                parameters = (new_stock, prod_id)
                execute_commit(query, parameters)
                return flash("Stock actualizado con éxito", "success")

            # Si el stock es 0 después de la operación, actualizar estado a 'agotado'
            elif new_stock == 0:
                update_producto_estado(prod_id, 'agotado')
                query = "UPDATE productos SET prod_stock = %s WHERE prod_id = %s"
                parameters = (new_stock, prod_id)
                execute_commit(query, parameters)
                return flash(f"Producto {producto.prod_descripcion} agotado tras la salida", "success")

        else:
            return flash(f"Stock insuficiente para retirar {prod_stock} unidades de {producto.prod_descripcion}", "error")
    
    else:
        return flash(f"Producto {producto.prod_descripcion} está agotado", "error")


     
