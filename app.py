from datetime import datetime
import os
import shutil
from database import pegarJson, salvarJson
from config import Main as config
import PySimpleGUI as sg
import subprocess

data = pegarJson()

gnu_gcc_version = ''

try:
    proc = subprocess.Popen(f"{data['compilador']['comando_C']} {data['compilador']['argumento_versao']}", stdout=subprocess.PIPE, shell=True)
    a = proc.stdout.readline()
    gnu_gcc_version += a.decode('utf-8').replace('\n', '')
except FileNotFoundError:
    gnu_gcc_version = 'Não instalado'

class Application():
    def __init__(self, gnu_v=''):
        if gnu_v: gnu_gcc_version = gnu_v
        self.data = pegarJson()
        self.layout = self.gerarlayout()
        self.window = sg.Window('RunC', self.layout, return_keyboard_events=False)
        self.window.read(timeout=1)
        self.terminal = self.formatTerminal('Pronto para compilar.')
        self.loop()
    
    def _RODAR_(self, openf=1):
        try:
            cam = f"{self.data['projeto']['comando_run'][0][1]} \"{self.data['projeto']['comando_run'][1]}\" -o output.exe {self.data['projeto']['comando_run'][0][2]}"
            proc = subprocess.Popen(cam,  cwd=self.data['projeto']['caminho'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
        except NotADirectoryError:
            err = b"NotADirectoryError: [WinError 267] O nome do diretorio e invalido\nTente consertar em Configuracoes > Projeto > Caminho do projeto"
        self.terminal += self.formatTerminal(err.decode('utf-8') if err.decode('utf-8') != '' else 'Compiled sucessfully')
        if self.values[2] and not err and openf: self.openFile()
        return err

    def loop(self):
        self.exportFolder = ''
        while True:
            self.event, self.values = self.window.read(timeout=100)
            self.data = pegarJson()
            if self.event in (None, sg.WINDOW_CLOSED): break
            elif self.event == '-RODAR-': self._RODAR_()
            elif self.event == 'Configurações': self.open(config)
            elif self.event == '-ABRIR-': self.openFile()
            elif self.event == '__TIMEOUT__': self.Timeout()
            if self.values['-EXPORTAR-'] != self.exportFolder: self.exportar()
        self.window.close()

    def exportar(self):
        showTerminal = "Exported sucessfully"
        self.exportFolder = self.values['-EXPORTAR-']
        try:
            paths = [
                self.data['projeto']['caminho'] + '/output.exe',
                self.exportFolder + '/output.exe'
            ]
            shutil.copyfile(paths[0], paths[1])
        except FileNotFoundError:
            err = self._RODAR_(0)
            if not err: 
                self.exportar()
                showTerminal = ''
            else: showTerminal = 'Error exporting file'
        if showTerminal: self.terminal += self.formatTerminal(showTerminal)
    
    def updateTerminal(self):
        if self.values['-CMD-'] != self.terminal: self.window['-CMD-'].update(value=self.terminal)

    def Timeout(self):
        if self.values[0] == True: self.data['projeto']['comando_run'][0] = ['C', self.data['compilador']['comando_C'], self.data['compilador']['argumento_C']]
        else: self.data['projeto']['comando_run'][0] = ['C++', self.data['compilador']['comando_C++'], self.data['compilador']['argumento_C++']]
        self.data['projeto']['auto_open'] = self.values[2]
        salvarJson(self.data)
        self.updateTerminal()

    def openFile(self):
        try:
            os.system('/K chcp 65001')
            os.startfile(f"{self.data['projeto']['caminho']}/output.exe")
        except FileNotFoundError:
            err = self._RODAR_(0)
            if not err: self.openFile()

    def open(self, fn):
        self.window.close()
        fn(Application)

    def formatTerminal(self, str):
        date = '[' + datetime.now().strftime("%H:%M:%S") + ']'
        return date + '-'*93 + date + '\n\n' + str + '\n\n' #+ '-'*123

    def gerarlayout(self):
        return [
            [sg.Multiline('Status: Nada compilado ainda\n' + '-'*123, disabled=True, font='Arial 10', background_color='#303343', text_color='#FFFFFF', size=(50, 20), key='-CMD-', expand_y=True, expand_x=True)],
            [sg.Button('Compilar', size=(24,2), expand_y=True, expand_x=True, key='-RODAR-'), sg.Button('Abrir', size=(24,2), expand_y=True, expand_x=True, key='-ABRIR-')],
            [sg.Text(f"{self.data['compilador']['nome']} version: " + gnu_gcc_version)],
            [sg.Button('Configurações'), sg.FolderBrowse('Exportar', k='-EXPORTAR-'), sg.Frame('', [
                [sg.Radio('C', 'lang', default=self.data['projeto']['comando_run'][0][0] == 'C'), sg.Radio('C++','lang', default=self.data['projeto']['comando_run'][0][0] == 'C++')]
            ]), sg.Frame('', [
                [sg.Checkbox('Abrir automático após compilar', default=data['projeto']['auto_open'])]
            ])]
        ]