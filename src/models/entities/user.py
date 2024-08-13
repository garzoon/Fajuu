from werkzeug.security import check_password_hash, generate_password_hash

class User:

    def __init__(self, id, nombre, apellido, password, ciudad, direccion, email, telefono, estado, rol):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.password = password
        self.ciudad = ciudad
        self.direccion = direccion
        self.email = email
        self.telefono = telefono
        self.estado = estado
        self.rol = rol

    @classmethod # decarador para usar la clase sin necesidad de instansearla
    def check_password (self,hashed_password, password):
        return check_password_hash(hashed_password, password)
