import mysql.connector
from mysql.connector import Error 
import pymysql


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

def fetch_query(query, parameters):
    connection = None
    cur = None
    try:
        connection = create_connection() 
        if connection:
            cur = connection.cursor()
            cur.execute(query, parameters)
            connection.commit() 
    except pymysql.Error as ex: 
        if connection:
            connection.rollback() 
        print(f"Error al ejecutar la consulta: {ex}")
        raise
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()
            print("Conexión cerrada")

