from flask import session
from src.database.connection import *
from src.controller import * 
from src.models import *
import json


operador = Usuario(
                321,
                "juaa",
                "cuvides",
                "123",
                "juan@gmailcom",
                31234123141,
                1                
            )

usuario_create(operador)