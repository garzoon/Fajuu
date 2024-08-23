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
    query = """INSERT INTO facturas 
                    (fact_id, 
                    clien_copiaid, 
                    fact_detalle_productos, 
                    fact_fecha_emision, 
                    fact_fecha_vencimiento, 
                    fact_estado) VALUES (%s, %s, %s, %s, %s, %s)"""
    parameters = (factura.fact_id, 
                  factura.clien_copiaid, 
                  factura.fact_detalle_productos, 
                  factura.fact_fecha_emision, 
                  factura.fact_fecha_vencimiento, 
                  factura.fact_estado)	

    fetch_one(query, parameters)
    return factura


def factura_delete (factura: Factura) -> Factura:
    query = "DELETE FROM facturas WHERE fact_id = %s"
    parameters = (factura.fact_id)

    fetch_one(query, parameters)
    return factura


def factura_update(factura: Factura) -> Factura:
    query = ("""UPDATE usuarios
                SET 
                    clien_copiaid           = %s,
                    fact_detalle_productos  = %s,
                    fact_fecha_emision      = %s, 
                    fact_fecha_vencimiento  = %s, 
                    fact_estado             = %s
                WHERE fact_id = %s
                """)
    parameters = (factura.clien_copiaid,
                  factura.fact_detalle_productos,  
                  factura.fact_fecha_emision, 
                  factura.fact_fecha_vencimiento, 
                  factura.fact_estado,
                  factura.fact_id)
    fetch_one(query, parameters)
    return factura