from ..models.proveedor_model import Proveedor
from ..database.connection import *


def proveedor_list() -> Proveedor:
    query = "SELECT * FROM proveedor ORDER BY prov_id DESC"

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()

def proveedor_select_nit(prov_nit) -> Proveedor:
    query = "SELECT * FROM proveedor WHERE prov_nit = %s ORDER BY prov_id DESC"
    parameters = (prov_nit, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()
    
def proveedor_select_id(prov_id) -> Proveedor:
    query = "SELECT * FROM proveedor WHERE prov_id = %s ORDER BY prov_id DESC"
    parameters = (prov_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def proveedor_create(proveedor: Proveedor) -> Proveedor:
    query = """INSERT INTO proveedor(
        prov_nit, 
        prov_razonsocial,
        prov_email, 
        prov_telefono, 
        prov_estado) VALUES (%s, %s, %s, %s, %s)
    """
    parameters = (
        proveedor.prov_nit, 
        proveedor.prov_razonsocial,
        proveedor.prov_email, 
        proveedor.prov_telefono, 
        proveedor.prov_estado
    )

    fetch_query(query, parameters)
    return proveedor


def proveedor_delete (proveedor: Proveedor) -> Proveedor:
    query = "DELETE FROM proveedor WHERE prov_id = %s"
    parameters = (proveedor.prov_id, )

    fetch_query(query, parameters)
    return proveedor


def proveedor_update(proveedor: Proveedor) -> Proveedor:
    query = """UPDATE proveedor SET 
        prov_nit            = %s, 
        prov_razonsocial    = %s,
        prov_email          = %s, 
        prov_telefono       = %s,
        prov_estado         = %s 
        WHERE prov_id       = %s
    """
    parameters = (
        proveedor.prov_nit, 
        proveedor.prov_razonsocial, 
        proveedor.prov_email, 
        proveedor.prov_telefono, 
        proveedor.prov_estado,
        proveedor.prov_id
    )
    fetch_query(query, parameters)
    return proveedor