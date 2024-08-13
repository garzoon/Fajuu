import mysql.connector
from mysql.connector import Error   


# Establecer 
def create_connection():
    try:
        connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'fajuu'
        )
        if connection.is_connected():
            print("Conectado a la Db")
            return connection
        else:
            print("Conexion cerrada")
            return None
    except Exception as ex:
        print(f"Error para conectarse a la base de datos: {ex}")
        return None

#Realizar proceso de conexion, creacion de cursor y fetch de query
def fetch_query(query, parameters):
    connection = None
    cur = None
    try:
        connection = create_connection()
        if connection:
            cur = connection.cursor()
            cur.execute(query, parameters)
            print("Fetch exitoso")
            return cur.fetchone()
    except Error as ex:
        print(f"Error para ejecutar la consulta: {ex}")
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()


# Verificar que un producto existe en la base de datos
def product_exist(table: str, field: str, value: str) -> bool:
    query = f"SELECT * FROM {table} WHERE {field}=%s LIMIT 1"
    parameters = value

    record = fetch_query(query, parameters)
    
 
    return  bool(record)


query = "INSERT INTO productos (prod_descripcion, cate_copiaid, prov_copiaid, prod_unidad_medida, prod_precio) VALUES (%s, %s, %s, %s, %s)"
parameters = ("pan", 2, 2, "Kg", 2000)

fetch_query(query, parameters)

product_exist()
