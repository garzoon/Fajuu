from .entrada_routes import entrada_scope
from .salida_route import salida_scope
from .auth.auth_routes import auth_scope
from .producto_routes import producto_scope

from .facturas.factura_routes import factura_scope
from .facturas.factura_proveedor_route import factura_proveedor_scope
from .facturas.factura_cliente_route import factura_cliente_scope

from .usuarios.usuario_routes import usuario_scope
from .usuarios.cliente_route import cliente_scope
from .usuarios.proveedor_routes import proveedor_scope
from .usuarios.operador_route import operador_scope
