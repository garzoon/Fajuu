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
        


#Realizar proceso de conexion, creacion de cursor y fetch one (SOLO PARA CONSULTAS SELECT)
def fetch_one(query, parameters):
    connection = None
    cur = None
    try:
        connection = create_connection()
        if connection:
            cur = connection.cursor(dictionary=True)
            cur.execute(query, parameters)
            return cur.fetchone()
    except Error as ex:
        print(f"Error para ejecutar la consulta: {ex}")
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()
            print("conexion cerrada")

def fetch_query(query, parameters):
    connection = None
    cur = None
    try:
        connection = create_connection()
        if connection:
            cur = connection.cursor()
            cur.execute(query, parameters)
            connection.commit()  # Hacemos commit de la transacción
    except Error as ex:
        if connection:
            connection.rollback()  # Hacemos rollback en caso de error
        print(f"Error al ejecutar la consulta: {ex}")
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()
            print("conexion cerrada")

# Verificar que un producto existe en la base de datos
def element_exist(table: str, field: str, value) -> bool:
    query = f"SELECT * FROM {table} WHERE {field}= %s"
    parameters = (value, ) 

    record = fetch_one(query, parameters)
    return  bool(record)

