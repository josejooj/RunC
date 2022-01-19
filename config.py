from typing import Text
from database import pegarJson, salvarJson
import PySimpleGUI as sg
import copy

data = pegarJson()

class Main():
    def __init__(self, app):
        self.data = pegarJson()
        self.data = self.data
        self.app = app
        self.layout = self.generateLayout()
        self.window = sg.Window('Configurações', self.layout)
        self.window.read(timeout=1)
        self.c = 0
        self.loop()

    def loop(self):
        i = 0
        while True:
            i = i + 1
            self.event, self.values = self.window.read(timeout=100)
            if self.event in (None, sg.WINDOW_CLOSED, 'Cancelar') or self.c == 1: break
            elif self.event == 'Salvar alterações': self.saveChanges()
            elif self.values[2] == True: 
                self.data['projeto']['comando_run'][0] = ['C', self.data['compilador']['comando_C'], self.data['compilador']['argumento_C']]
            else: 
                self.data['projeto']['comando_run'][0] = ['C++', self.data['compilador']['comando_C++'], self.data['compilador']['argumento_C++']]
            self.window['projectcmd'].update(value=self.data['projeto']['comando_run'][0][1])
            salvarJson(self.data)
        self.window.close()
        self.app()

    def saveChanges(self):
        layout = [
            [sg.Text('Tem certeza de que deseja salvar as alterações?')],
            [sg.Button('Sim'), sg.Button('Não')]
        ]
        popup = sg.Window('Popup', layout)
        popup.read(timeout=1)
        while True:
            e = popup.read()
            print(e)
            if e[0] in (None, sg.WINDOW_CLOSED, 'Não'): break
            else:
                self.data = pegarJson()
                self.data['projeto']['caminho'] = self.values[0]
                self.data['projeto']['comando_run'][1] = self.values[1]
                self.data['compilador']['nome'] = self.values[4]
                self.data['compilador']['argumento_versao'] = self.values[5]
                self.data['compilador']['comando_C'] = self.values[6]
                self.data['compilador']['argumento_C'] = self.values[7]
                self.data['compilador']['comando_C++'] = self.values[8]
                self.data['compilador']['argumento_C++'] = self.values[9]
                salvarJson(self.data)
                sg.Popup('Alterações feitas com sucesso!')
                break
        popup.close()
        self.c = 1
    def generateLayout(self):
        return [
            [sg.Frame('Projeto', [
                [sg.Frame('Pasta do projeto', [
                    [sg.Input(self.data['projeto']['caminho'], expand_x=True), sg.FolderBrowse('Procurar')]
                ], expand_x=True)],
                [sg.Frame('Comando para compilar', [
                    [sg.Input(self.data['projeto']['comando_run'][0][1], key='projectcmd', disabled=True, size=(5,1)), sg.Input(self.data['projeto']['comando_run'][1]), sg.Radio('C', 'lang', default=self.data['projeto']['comando_run'][0][0] == 'C'), sg.Radio('C++','lang', default=self.data['projeto']['comando_run'][0][0] == 'C++')]
                ])]
            ], expand_x=True)],
            [sg.T()],
            [sg.Frame('Compilador', [
                [sg.Frame('Nome do compilador: ', [
                    [sg.Input(self.data['compilador']['nome'])],
                ], size=(250, 50), expand_x=True),
                sg.Frame('Argumento de versão do compilador: ', [
                        [sg.Input(self.data['compilador']['argumento_versao'])]
                ], s=(230, 50))],
                [sg.Frame('Compilador para C', [
                    [sg.Frame('Comando para compilar: ', [
                        [sg.Input(self.data['compilador']['comando_C'])]
                    ], size=(180, 50)),
                    sg.Frame('Argumentos opcionais para o compilador: ', [
                        [sg.Input(self.data['compilador']['argumento_C'])]
                    ])]
                ], expand_x=True)],
                [sg.Frame('Compilador para C++', [
                    [sg.Frame('Comando para compilar: ', [
                        [sg.Input(self.data['compilador']['comando_C++'])]
                    ], size=(180, 50)),
                    sg.Frame('Argumentos opcionais para o compilador: ', [
                        [sg.Input(self.data['compilador']['argumento_C++'])]
                    ])]
                ])]
            ], expand_x=True)],
            [sg.Button('Salvar alterações'), sg.Button('Cancelar')]
        ]