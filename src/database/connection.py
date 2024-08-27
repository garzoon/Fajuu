import mysql.connector
from mysql.connector import Error 


def create_connection():
    try:
        connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'fajuu'
        )
        if connection.is_connected():
            print("Db conectada")
            return connection
        else:
            print("Db no conectada")
            return None
    except Exception as ex:
        print(f"Error para conectarse a la base de datos: {ex}")
        return None
        
def fetch_one(query, parameters):
    connection = None
    cursor = None
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor() # Retorna un diccionario
            cursor.execute(query, parameters)
            return cursor.fetchone()
        except Error as ex: 
            connection.rollback() 
            print(f"Error al ejecutar la consulta: {ex}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                print("Conexión cerrada")
                
def fetch_all(query, parameters = None):
    connection = None
    cursor = None
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()
        except Error as ex: 
            connection.rollback() 
            print(f"Error al ejecutar la consulta: {ex}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                print("Conexión cerrada")
        

def execute_commit(query, parameters):
    connection = None
    cur = None
    connection = create_connection() 
    if connection:
        try:
            cur = connection.cursor()
            cur.execute(query, parameters)
            connection.commit()
        except Error as ex: 
            connection.rollback() 
            print(f"Error al ejecutar la consulta: {ex}")
            raise
        finally:
            if cur:
                cur.close()
            if connection:
                connection.close()
                print("Conexión cerrada")

