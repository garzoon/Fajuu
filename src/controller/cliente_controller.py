from ..models.cliente_model import Cliente
from ..database.connection import *

def cliente_list() -> Cliente:
    query = "SELECT * FROM clientes ORDER BY clien_id DESC"
    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def cliente_select(clien_id) -> Cliente:
    query = "SELECT * FROM clientes WHERE clien_id = %s ORDER BY clien_id DESC"
    parameters = (clien_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()
    
def cliente_select_document(clien_document) -> Cliente:
    query = "SELECT * FROM clientes WHERE clien_documento = %s ORDER BY clien_id DESC"
    parameters = (clien_document, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def cliente_create(cliente : Cliente) -> Cliente:
    query = """INSERT INTO clientes (
        clien_documento, 
        clien_nombre,  
        clien_ciudad, 
        clien_direccion, 
        clien_email, 
        clien_telefono, 
        clien_estado) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    parameters = (
        cliente.clien_documento, 
        cliente.clien_nombre,
        cliente.clien_ciudad, 
        cliente.clien_direccion, 
        cliente.clien_email, 
        cliente.clien_telefono, 
        cliente.clien_estado
    )

    fetch_query(query, parameters)
    return cliente


def cliente_delete (cliente : Cliente) -> Cliente:
    query = "DELETE FROM clientes WHERE clien_id = %s"
    parameters = [cliente.clien_id, ]

    fetch_query(query, parameters)
    return cliente


def cliente_update(cliente : Cliente) -> Cliente:
    query = ("""UPDATE clientes SET 
        clien_documento = %s, 
        clien_nombre    = %s, 
        clien_ciudad    = %s, 
        clien_direccion = %s, 
        clien_email     = %s, 
        clien_telefono  = %s, 
        clien_estado    = %s
        WHERE clien_id  = %s
    """)
    parameters = (
        cliente.clien_documento, 
        cliente.clien_nombre, 
        cliente.clien_ciudad, 
        cliente.clien_direccion, 
        cliente.clien_email, 
        cliente.clien_telefono, 
        cliente.clien_estado,
        cliente.clien_id
    )
    fetch_query(query, parameters)
    return cliente