from typing import Text
from database import pegarJson, salvarJson
import PySimpleGUI as sg
import copy

data = pegarJson()

layout = [
    [sg.Frame('Arquivo', [
        [sg.Frame('Caminho do arquivo', [
            [sg.Input(data['arquivo']['caminho']), sg.FileBrowse('Procurar')]
        ])]
    ])]
]

class Main():
    def __init__(self, app):
        self.app = app
        self.layout = copy.deepcopy(layout)
        self.window = sg.Window('Configurações', self.layout)
        self.loop()

    def loop(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event in (None, sg.WINDOW_CLOSED):
                break
        self.app()
        self.window.close()