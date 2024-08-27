from ..models.proveedor_model import Proveedor
from ..database.connection import *


def proveedor_list():
    query = "SELECT * FROM proveedor ORDER BY prov_id DESC"
    return fetch_all(query)

def proveedor_select(prov_id):
    query = "SELECT * FROM proveedor WHERE prov_id = %s ORDER BY prov_id DESC"
    parameters = (prov_id, )
    result = fetch_one(query, parameters)
    if result:
        return Proveedor(*result)
    return None 

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
    execute_commit(query, parameters)
    return proveedor

def proveedor_delete (proveedor: Proveedor) -> Proveedor:
    query = "DELETE FROM proveedor WHERE prov_id = %s"
    parameters = (proveedor.prov_id, )
    execute_commit(query, parameters)
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
    execute_commit(query, parameters)
    return proveedor


def get_proveedor_nit(prov_nit):
    query = "SELECT * FROM proveedor WHERE prov_nit = %s ORDER BY prov_id DESC"
    parameters = (prov_nit, )
    return fetch_one(query, parameters)

def get_proveedor_estado(prov_id):
    query = "SELECT prov_estado FROM proveedor WHERE prov_id = %s ORDER BY prov_id DESC"
    parameters = (prov_id, )
    return fetch_one(query, parameters)
    