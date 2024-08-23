
from werkzeug.security import check_password_hash

class Usuario:
    def __init__(self, user_id, user_nombre, user_apellido, user_password, user_email, user_telefono, rol_copiaid, user_estado = "activo"):
        self.user_id = user_id
        self.user_nombre = user_nombre
        self.user_apellido = user_apellido
        self.user_password = user_password
        self.user_email = user_email
        self.user_telefono = user_telefono
        self.rol_copiaid = rol_copiaid
        self.user_estado = user_estado
        
    
