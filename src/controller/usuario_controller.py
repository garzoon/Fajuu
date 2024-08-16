from ..models.usuario_model import Usuario
from ..database.connection import *


def fullname(user_nombre, user_apellido):
        return f"{user_nombre} {user_apellido}"


def usuario_list() -> Usuario:
    query = "SELECT * FROM usuarios ORDER BY user_id DESC"

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def usuario_select(user_id) -> Usuario:
    if not element_exist('usuarios', 'user_id', user_id):
        raise Exception("Usuario no encontrado")
    
    query = "SELECT * FROM usuarios WHERE user_id = %s ORDER BY user_id DESC"
    parameters = (user_id, )

    connection = create_connection()
    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        return cur.fetchall()


def usuario_create(usuario: Usuario) -> Usuario:
    if element_exist('Usuarios', 'user_id', usuario.user_id):
        raise Exception(f"Usuario {usuario.user_id}{fullname(usuario.user_nombre, usuario.user_apellido)} ya existe")
    
    query = """INSERT INTO productos 
                    (user_nombre, 
                    user_apellido, 
                    user_password, 
                    user_ciudad, 
                    user_direccion, 
                    user_email, 
                    user_telefono, 
                    rol_copiaid, 
                    user_estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    parameters = (usuario.user_nombre, 
                  usuario.user_apellido, 
                  usuario.user_password, 
                  usuario.user_ciudad, 
                  usuario.user_direccion, 
                  usuario.user_email, 
                  usuario.user_telefono, 
                  usuario.rol_copiaid, 
                  usuario.user_estado)

    fetch_one(query, parameters)
    return usuario


def usuario_delete (usuario: Usuario) -> Usuario:
    if not element_exist('usuarios', 'user_id', usuario.user_id):
        raise Exception("Usuario no encontrado")

    query = "DELETE FROM usuarios WHERE user_id = %s"
    parameters = (usuario.user_id)

    fetch_one(query, parameters)
    return usuario


def usuario_update(usuario: Usuario) -> Usuario:
    if not element_exist('usuarios', 'user_id', usuario.user_id):
        raise Exception("Usuario no encontrado")

    query = ("""UPDATE usuarios
                SET 
                    user_nombre     = %s, 
                    user_apellido   = %s, 
                    user_password   = %s, 
                    user_ciudad     = %s, 
                    user_direccion  = %s, 
                    user_email      = %s, 
                    user_telefono   = %s,
                    rol_copiaid     = %s,
                    user_estado     = %s
                WHERE user_id = %s
                """)
    parameters = (usuario.user_nombre, 
                  usuario.user_apellido, 
                  usuario.user_password, 
                  usuario.user_ciudad, 
                  usuario.user_direccion, 
                  usuario.user_email, 
                  usuario.user_telefono, 
                  usuario.rol_copiaid, 
                  usuario.user_estado,
                  usuario.user_id)
    fetch_one(query, parameters)
    return usuario