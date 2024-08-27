from ..models.cliente_model import Cliente
from ..database.connection import *

def cliente_list():
    query = "SELECT * FROM clientes ORDER BY clien_id DESC"
    return fetch_all(query)

def cliente_select(clien_id):
    query = "SELECT * FROM clientes WHERE clien_id = %s ORDER BY clien_id DESC"
    parameters = (clien_id, )
    result = fetch_one(query, parameters)
    if result:
        return Cliente(*result)
    return None

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
    execute_commit(query, parameters)
    return cliente


def cliente_delete (cliente : Cliente) -> Cliente:
    query = "DELETE FROM clientes WHERE clien_id = %s"
    parameters = [cliente.clien_id, ]
    execute_commit(query, parameters)
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
    execute_commit(query, parameters)
    return cliente

    
def get_cliente_documento(clien_document) -> Cliente:
    query = "SELECT * FROM clientes WHERE clien_documento = %s ORDER BY clien_id DESC"
    parameters = (clien_document, )
    return fetch_one(query, parameters)

def get_cliente_estado(prov_id):
    query = "SELECT * FROM clientes WHERE clien_id = %s ORDER BY clien_id DESC"
    parameters = (prov_id, )
    return fetch_one(query, parameters)
