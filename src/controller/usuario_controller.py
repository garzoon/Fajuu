from ..models.usuario_model import Usuario
from ..database.connection import *


def fullname(user_nombre, user_apellido):
        return f"{user_nombre} {user_apellido}"

def get_user_rol(rol_id):
    query = "SELECT rol_descripcion FROM tipo_usuario WHERE rol_id = %s"
    parameters = (rol_id, )
    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()

def usuario_list() -> Usuario:
    query = "SELECT * FROM usuarios ORDER BY user_id DESC"

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def usuario_select(user_id) -> Usuario:
    query = "SELECT * FROM usuarios WHERE user_id = %s ORDER BY user_id DESC"
    parameters = (user_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def usuario_create(usuario: Usuario) -> Usuario:
    query = """INSERT INTO usuarios (
                                user_id,
                                user_nombre, 
                                user_apellido, 
                                user_password, 
                                user_email, 
                                user_telefono, 
                                rol_copiaid) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    parameters = (usuario.user_id,
                  usuario.user_nombre, 
                  usuario.user_apellido, 
                  usuario.user_password, 
                  usuario.user_email, 
                  usuario.user_telefono, 
                  usuario.rol_copiaid)

    fetch_query(query, parameters)
    return usuario


def usuario_delete (usuario: Usuario) -> Usuario:
    query = "DELETE FROM usuarios WHERE user_id = %s"
    parameters = (usuario.user_id, )

    fetch_query(query, parameters)
    return usuario


def usuario_update(usuario: Usuario) -> Usuario:
    query = ("""UPDATE usuarios
                SET 
                    user_nombre     = %s, 
                    user_apellido   = %s, 
                    user_password   = %s,
                    user_email      = %s, 
                    user_telefono   = %s,
                    user_estado     = %s
                WHERE user_id = %s
                """)
    parameters = (usuario.user_nombre, 
                  usuario.user_apellido, 
                  usuario.user_password, 
                  usuario.user_email, 
                  usuario.user_telefono,
                  usuario.user_estado,
                  usuario.user_id)
    fetch_query(query, parameters)
    return usuario