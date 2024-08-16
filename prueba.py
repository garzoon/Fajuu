from src.database.connection import *
from src.models.proveedor_model import Proveedor

def proveedor_select(id):
    conexion = create_connection()
    cursor = conexion.cursor()

    query = "SELECT * FROM proveedor WHERE prov_id = %s"
    property = (id,)
    cursor.execute(query, property)
    proveedor = cursor.fetchall()
    cursor.close()

    return proveedor

conexion = create_connection()
cursor = conexion.cursor()

query = "SELECT * FROM entradas ORDER BY ent_id DESC"
cursor.execute(query)

facturas = cursor.fetchall()




for i in facturas:
    cliente = proveedor_select(i[1])
    print(cliente)
    fullname = f"{cliente[0][2]} {cliente[0][3]}"
    item_entrada = (i[0], i[1], fullname, i[3])
    print(item_entrada)



# print(item_entrada)







