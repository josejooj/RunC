from database import pegarJson, salvarJson
from config import Main as config
import PySimpleGUI as sg
import subprocess
import copy
import re
import os

data = pegarJson()

try:
    data['FirstTimee']
except KeyError:
    data['FirstTime'] = False
    data['arquivo'] = {
        "caminho": (os.getcwd() + '/representativo/main.cpp').replace('\\', '/'),
        "comando_run": "g++ ${arquivo}"
    }
    data['compilador'] = {
        "nome": "GNU GCC Compiler",
        "comando_C": "gcc",
        "comando_C++": "g++"
    }
    salvarJson(data)

#sg.theme('DarkGreen3')

gnu_gcc_version = ''

try:
    proc = subprocess.Popen(f"{data['compilador']['comando_C']} --version", stdout=subprocess.PIPE, shell=True)
    a = proc.stdout.readline()
    gnu_gcc_version += a.decode('utf-8').replace('\n', '')
except FileNotFoundError:
    gnu_gcc_version = 'Não instalado'

layout = [
    [sg.Multiline('Status: Nada compilado ainda\n' + '-'*97, background_color='#303343', text_color='#FFFFFF', size=(50, 20), key='-CMD-', expand_y=True, expand_x=True)],
    [sg.Button('Rodar', size=(24,2), expand_y=True, expand_x=True, key='-RODAR-'), sg.Button('Abrir', size=(24,2), expand_y=True, expand_x=True, key='-ABRIR-')],
    [sg.Text(f"{data['compilador']['nome']} version: " + gnu_gcc_version)],
    [sg.Button('Configurações')]
]

class Application():
    def __init__(self):
        self.layout = copy.deepcopy(layout)
        self.window = sg.Window('RunDir', self.layout, resizable=True, return_keyboard_events=False)
        self.window.read(timeout=1)
        self.process = subprocess.Popen('cmd')
        self.terminal = ''
        self.loop()
    
    def _RODAR_(self):
        self.process = subprocess.Popen(f"{data['arquivo']['comando_run']}", shell=True, text=True, cwd=data['arquivo']['caminho'], stdout=subprocess.PIPE)
        self.window['-CMD-'].update(value=self.terminal)
    
    def loop(self):
        while True:
            self.event, self.value = self.window.read()
            if self.event in (None, sg.WINDOW_CLOSED): break
            elif self.event == '-RODAR-': self._RODAR_()
            elif self.event == 'Configurações': self.open(config)          
        
        self.window.close()

    def open(self, fn):
        self.window.close()
        fn(Application)

Application()