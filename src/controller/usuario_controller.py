from ..models.usuario_model import Usuario
from ..database.connection import *
from ..utils.security import encrypt_password, check_password

def usuario_list():
    query = "SELECT * FROM usuarios ORDER BY user_id DESC"
    return fetch_all(query)

def usuario_select(user_id):
    query = "SELECT * FROM usuarios WHERE user_id = %s ORDER BY user_id DESC"
    parameters = (user_id, )
    result = fetch_one(query, parameters)
    if result:
        return Usuario(*result)
    return None 


def usuario_create(usuario: Usuario) -> Usuario:
    hashed_password = encrypt_password(usuario.user_password)
    query = """INSERT INTO usuarios ( 
        user_id,
        user_nombre, 
        user_apellido, 
        user_password, 
        user_email, 
        user_telefono, 
        rol_copiaid) VALUES (%s, %s, %s, %s, %s, %s, %s
    )"""
    parameters = (
        usuario.user_id,
        usuario.user_nombre, 
        usuario.user_apellido, 
        hashed_password, 
        usuario.user_email, 
        usuario.user_telefono, 
        usuario.rol_copiaid
    )
    execute_commit(query, parameters)
    return usuario


def usuario_delete (usuario: Usuario) -> Usuario:
    query = "DELETE FROM usuarios WHERE user_id = %s"
    parameters = (usuario.user_id, )
    execute_commit(query, parameters)
    return usuario


def usuario_update(usuario: Usuario) -> Usuario:
    hashed_password = encrypt_password(usuario.user_password)
    query = """UPDATE usuarios SET 
        user_nombre     = %s, 
        user_apellido   = %s, 
        user_password   = %s,
        user_email      = %s, 
        user_telefono   = %s,
        user_estado     = %s
        WHERE user_id = %s
    """
    parameters = (
        usuario.user_nombre, 
        usuario.user_apellido, 
        hashed_password, 
        usuario.user_email, 
        usuario.user_telefono,
        usuario.user_estado,
        usuario.user_id
    )
    execute_commit(query, parameters)
    return usuario

    
def get_usuario_rol(rol_id):
    query = "SELECT rol_descripcion FROM tipo_usuario WHERE rol_id = %s"
    parameters = (rol_id, )
    return fetch_one(query, parameters)

def get_usuario_id(user_id):
    query = "SELECT * FROM usuarios WHERE user_id = %s AND user_estado = 'activo'"
    parameters = (user_id, )
    result = fetch_one(query, parameters)
    if result:
        return Usuario(*result)
    return None 