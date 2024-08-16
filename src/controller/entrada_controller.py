from ..models.entrada_model import Entrada
from ..database.connection import *

def entrada_list() -> Entrada:

    query = "SELECT * FROM entradas ORDER BY ent_id DESC"

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def entrada_select(ent_id) -> Entrada:
    if not element_exist('entradas', 'ent_id', ent_id):
        raise Exception("Entrada no encontrado")
    
    query = "SELECT * FROM entradas WHERE ent_id = %s ORDER BY ent_id DESC"
    parameters = (ent_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def entrada_create(entrada : Entrada) -> Entrada:
    if element_exist('entradas', 'ent_id', entrada.ent_id):
        raise Exception(f"Entrada {entrada.ent_id} ya existe")
    
    query = """INSERT INTO entradas 
                    (ent_id, 
                    prov_copiaid, 
                    ent_detalle_producto, 
                    ent_fecha_entrada) VALUES (%s, %s, %s, %s)"""
    parameters = (entrada.ent_id, 
                  entrada.prov_copiaid, 
                  entrada.ent_detalle_producto, 
                  entrada.ent_fecha_entrada)

    fetch_query(query, parameters)
    return entrada


def entrada_delete (ent_id):
    if not element_exist('entradas', 'ent_id', ent_id):
        raise Exception("Entrada no encontrado")

    query = "DELETE FROM entradas WHERE ent_id = %s"
    parameters = [ent_id, ]

    fetch_query(query, parameters)
    return "Entrada eliminada"


def entrada_update(entrada: Entrada) -> Entrada:
    if not element_exist('entradas', 'ent_id', entrada.ent_id):
        raise Exception("Entrada no encontrado")

    query = ("""UPDATE entradas 
                SET  
                    prov_copiaid            = %s, 
                    ent_detalle_producto    = %s, 
                    ent_fecha_entrada       = %s
                WHERE ent_id = %s
                """)
    parameters = (entrada.prov_copiaid, 
                  entrada.ent_detalle_producto, 
                  entrada.ent_fecha_entrada,
                  entrada.ent_id)
    fetch_query(query, parameters)
    return entrada