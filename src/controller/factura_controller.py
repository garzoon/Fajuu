from ..models.factura_model import Factura
from ..database.connection import *

def factura_list() -> Factura:
    query = "SELECT * FROM facturas ORDER BY fact_id DESC"
    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def factura_select(fact_id) -> Factura:
    query = "SELECT * FROM facturas WHERE fact_id = %s ORDER BY fact_id DESC"
    parameters = (fact_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def factura_create(factura: Factura) -> Factura:
    query = """INSERT INTO facturas (
        fact_id, 
        clien_copiaid, 
        fact_detalle_productos, 
        fact_fecha_emision) VALUES (%s, %s, %s, %s)
    """
    parameters = (
        factura.fact_id, 
        factura.clien_copiaid, 
        factura.fact_detalle_productos, 
        factura.fact_fecha_emision
    )	

    fetch_query(query, parameters)
    return factura


def factura_delete (factura: Factura) -> Factura:
    query = "DELETE FROM facturas WHERE fact_id = %s"
    parameters = (factura.fact_id, )

    fetch_query(query, parameters)
    return factura


def factura_update(factura: Factura) -> Factura:
    query = ("""UPDATE facturas SET 
        clien_copiaid           = %s,
        fact_detalle_productos  = %s,
        fact_fecha_emision      = %s
        WHERE fact_id           = %s
    """)
    parameters = (
        factura.clien_copiaid,
        factura.fact_detalle_productos,  
        factura.fact_fecha_emision,
        factura.fact_id
    )
    fetch_query(query, parameters)
    return factura