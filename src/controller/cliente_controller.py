from ..models.cliente_model import Cliente
from ..database.connection import *

def fullname(cliente : Cliente):
    return f"{cliente.clien_nombre} {cliente.clien_apellido}"

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


def cliente_create(cliente : Cliente) -> Cliente:
    query = """INSERT INTO clientes 
                (clien_nit, 
                clien_nombre, 
                clien_apellido, 
                clien_ciudad, 
                clien_direccion, 
                clien_email, 
                clien_telefono, 
                clien_estado) VALUES (%s, %s, %s, %s, %s)"""
    parameters = (cliente.clien_nit, 
                  cliente.clien_nombre, 
                  cliente.clien_apellido, 
                  cliente.clien_ciudad, 
                  cliente.clien_direccion, 
                  cliente.clien_email, 
                  cliente.clien_telefono, 
                  cliente.clien_estado)

    fetch_one(query, parameters)
    return cliente


def cliente_delete (cliente : Cliente) -> Cliente:
    query = "DELETE FROM clientes WHERE clien_id = %s"
    parameters = [cliente.clien_id]

    fetch_one(query, parameters)
    return cliente


def cliente_update(cliente : Cliente) -> Cliente:
    query = ("""UPDATE clientes 
                SET 
                    clien_nit       = %s, 
                    clien_nombre    = %s, 
                    clien_apellido  = %s, 
                    clien_ciudad    = %s, 
                    clien_direccion = %s, 
                    clien_email     = %s, 
                    clien_telefono  = %s, 
                    clien_estado    = %s
                WHERE clien_id = %s
                """)
    parameters = (cliente.clien_nit, 
                  cliente.clien_nombre, 
                  cliente.clien_apellido, 
                  cliente.clien_ciudad, 
                  cliente.clien_direccion, 
                  cliente.clien_email, 
                  cliente.clien_telefono, 
                  cliente.clien_estado)
    fetch_one(query, parameters)
    return cliente