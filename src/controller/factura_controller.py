from ..models.factura_model import Factura
from ..database.connection import *

def factura_list() -> Factura:
    query = "SELECT * FROM facturas ORDER BY fact_id DESC"
    return fetch_all(query)

def factura_select(fact_id):
    query = "SELECT * FROM facturas WHERE fact_id = %s ORDER BY fact_id DESC"
    parameters = (fact_id, )
    result = fetch_one(query, parameters)
    if result:
        return Factura(*result)
    return None

def factura_create(factura: Factura) -> Factura:
    query = """INSERT INTO facturas (
        fact_id, 
        clien_copiaid, 
        fact_detalle_productos, 
        fact_valor_total,
        fact_fecha_emision) VALUES (%s, %s, %s, %s, %s)
    """
    parameters = (
        factura.fact_id, 
        factura.clien_copiaid, 
        factura.fact_detalle_productos, 
        factura.fact_valor_total,
        factura.fact_fecha_emision
    )	
    execute_commit(query, parameters)
    return factura

def factura_delete (factura: Factura) -> Factura:
    query = "DELETE FROM facturas WHERE fact_id = %s"
    parameters = (factura.fact_id, )
    execute_commit(query, parameters)
    return factura

def factura_update(factura: Factura) -> Factura:
    query = ("""UPDATE facturas SET 
        clien_copiaid           = %s,
        fact_detalle_productos  = %s,
        fact_valor_total        = %s,
        fact_fecha_emision      = %s
        WHERE fact_id           = %s
    """)
    parameters = (
        factura.clien_copiaid,
        factura.fact_detalle_productos,
        factura.fact_valor_total,
        factura.fact_fecha_emision,
        factura.fact_id
    )
    execute_commit(query, parameters)
    return factura