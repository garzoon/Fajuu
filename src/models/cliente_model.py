class Cliente:
    def __init__(self, clien_id ,clien_nit, clien_nombre, clien_apellido, clien_ciudad, clien_direccion, clien_email, clien_telefono, clien_estado="activo"):
        self.clien_id = clien_id
        self.clien_nit = clien_nit	
        self.clien_nombre = clien_nombre	
        self.clien_apellido = clien_apellido	
        self.clien_ciudad = clien_ciudad	
        self.clien_direccion = clien_direccion	
        self.clien_email = clien_email	
        self.clien_telefono = clien_telefono	
        self.clien_estado = clien_estado