from flask import session
from src.database.connection import *
from src.controller import * 
from src.models import *
import json

num = 0

dic = {1 : ["pan", 12]}

print(dic[1][-1])
