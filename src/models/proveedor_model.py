class Proveedor: 
    def __init__(self, prov_id, prov_nit, prov_razonsocial, prov_email, prov_telefono, prov_estado = "activo"):
        self.prov_id = prov_id 
        self.prov_nit = prov_nit
        self.prov_razonsocial = prov_razonsocial
        self.prov_email = prov_email	
        self.prov_telefono = prov_telefono	
        self.prov_estado = prov_estado