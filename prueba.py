from flask import session
from src.database.connection import *
from src.controller import * 
from src.models import *
import json

rol = 1

print(get_user_rol(rol)[0][0])