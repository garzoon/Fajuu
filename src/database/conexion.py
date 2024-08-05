import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = '',
        db = 'fajuu'
    )

    if conexion.is_connected():
        print("conexion exitosa")
        infoServer = conexion.get_server_info()
        print("Información del servidor:", infoServer)
except Error as ex:
    print("Error durante la conexion:", ex)
finally:
    if conexion.is_connected: conexion.close()
        