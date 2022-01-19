from database import pegarJson, salvarJson
import os

data = pegarJson()

try:
    data['FirstTime']
except KeyError:
    data['FirstTime'] = False
    data['projeto'] = {
        "caminho": (os.getcwd() + '/representativo').replace('\\', '/'),
        "comando_run": [['C++', "g++", "-std=c++11"], "main.cpp"],
        "auto_open": False
    }
    data['compilador'] = {
        "nome": "GNU GCC Compiler",
        "argumento_versao": "--version",
        "comando_C": "gcc",
        "argumento_C": "",
        "comando_C++": "g++",
        "argumento_C++": "-std=c++11"
    }
    salvarJson(data)

from app import Application

Application()