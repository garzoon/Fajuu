from ..models.entrada_model import Entrada
from ..database.connection import *

def entrada_list():
    query = "SELECT * FROM entradas ORDER BY ent_id DESC"
    return fetch_all(query)

def entrada_select(ent_id):
    query = "SELECT * FROM entradas WHERE ent_id = %s ORDER BY ent_id DESC"
    parameters = (ent_id, )
    result = fetch_one(query, parameters)
    if result:
        return Entrada(*result)
    return None

def entrada_create(entrada : Entrada) -> Entrada:
    query = """INSERT INTO entradas (
        ent_id, 
        prov_copiaid, 
        ent_detalle_producto, 
        ent_fecha_entrada) VALUES (%s, %s, %s, %s)
    """
    parameters = (
        entrada.ent_id, 
        entrada.prov_copiaid, 
        entrada.ent_detalle_producto, 
        entrada.ent_fecha_entrada
    )
    execute_commit(query, parameters)
    return entrada


def entrada_delete (entrada: Entrada):
    query = "DELETE FROM entradas WHERE ent_id = %s"
    parameters = [entrada.ent_id, ]
    execute_commit(query, parameters)
    return entrada


def entrada_update(entrada: Entrada) -> Entrada:
    query = ("""UPDATE entradas SET  
        prov_copiaid            = %s, 
        ent_detalle_producto    = %s, 
        ent_fecha_entrada       = %s
        WHERE ent_id            = %s
    """)
    parameters = (
        entrada.prov_copiaid, 
        entrada.ent_detalle_producto, 
        entrada.ent_fecha_entrada,
        entrada.ent_id
    )
    execute_commit(query, parameters)
    return entrada