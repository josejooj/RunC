from database import pegarJson, salvarJson
import PySimpleGUI as sg
import subprocess
import threading
import re
import os

data = pegarJson()

try:
    data['FirstTime']
except KeyError:
    data['FirstTime'] = False
    data['CaminhoDiretorio'] = (os.getcwd() + '/representativo').replace('\\', '/')
    data['CaminhoOutput'] = (os.getcwd() + '/representativo/output.txt').replace('\\', '/')
    data['ComandoRun'] = 'python main.py'
    salvarJson(data)

sg.theme('DarkGreen3')

nodeversion = str(subprocess.check_output('node -v'))
nodeversion = str(re.sub(r"'|b\'|\\n|\\r", '', nodeversion))
menu_layout = [
    ['Configurações', ['Caminho do diretório', 'Caminho do Output', 'Comando para iniciar']]
]

layout = [
    [sg.Menu(menu_layout)],
    [sg.Multiline('Status: Parado\n' + '-'*97, background_color='#303343', text_color='#FFFFFF', size=(50, 20), key='-CMD-', expand_y=True, expand_x=True)],
    [sg.Button('Rodar', size=(24,2), expand_y=True, expand_x=True, key='-RODAR-'), sg.Button('Parar', size=(24,2), expand_y=True, expand_x=True, key='-PARAR-')],
    [sg.Text('Node version: ' + nodeversion)]
]

class Application():
    def __init__(self):
        self.window = sg.Window('RunDir', layout, resizable=True, return_keyboard_events=False)
        self.window.read(timeout=1)
        self.process = subprocess.Popen('cmd')
        self.processRuning = 0
        self.loop()
    
    def _RODAR_(self):
        self.process = subprocess.Popen(f"{data['ComandoRun']}", cwd=data['CaminhoDiretorio'])
        formated = str(self.value['-CMD-']).replace('Status: Parado', 'Status: Rodando')
        self.window['-CMD-'].update(value=formated)

    def _PARAR_(self):
        if(self.process.poll() == None): self.process.kill()
        formated = str(self.value['-CMD-']).replace('Status: Rodando', 'Status: Parado')
        self.window['-CMD-'].update(value=formated)
    
    def loop(self):
        while True:
            self.event, self.value = self.window.read()
            if self.event in (None, sg.WINDOW_CLOSED):
                break
            elif self.event == '-RODAR-': self._RODAR_()
            elif self.event == '-PARAR-': self._PARAR_()
            elif self.event == 'Caminho do diretório': self._CAMINHO_DO_DIRETORIO_()
            elif self.event == 'Caminho do Output': self._CAMINHO_DO_ARQUIVO_()
        
        self.window.close()

    def checkProcess(self):
        if self.process.poll() != None and self.processRuning != 0:
            self._PARAR_()

    def _CAMINHO_DO_DIRETORIO_(self):
        data = pegarJson()
        layoutt = [
            [sg.Text('Caminho atual do diretório:')],
            [sg.FolderBrowse(data['CaminhoDiretorio'], key='caminho', size=(60, 1))],
            [sg.Button('Salvar alterações', key='save'), sg.Button('Cancelar')],
            [sg.Text('\nO caminho do diretório é onde o comando de inicializar será executado\n\nEx¹: Você tem um projeto em node, para rodar ele, bote o caminho da pasta raiz dele aqui,\ne o comando como node ., npm start, como você usa normalmente\n\nEx²: Você tem um projeto em Python, aqui você insere o diretório onde o arquivo principal está,\ne no comando insere "python <nome do arquivo>"')]
        ]
        popup = sg.Window('Caminho do diretório', layoutt, modal=True)
        popup.read(timeout=1)

        while True:
            e = popup.read()
            
            if e[0] == 'insertcam':
                popup['caminho'].update(value=os.getcwd())
            else:
                if e[0] == 'save':
                    data['CaminhoDiretorio'] = e[1]['caminho']
                    salvarJson(data)
                    sg.Popup('Caminho alterado com sucesso!')
                popup.close()
                break

    def _CAMINHO_DO_ARQUIVO_(self):
        data = pegarJson()
        arquivo_layout = [
            [sg.Text('Caminho atual do arquivo de output:')],
            [sg.InputText(data['CaminhoOutput'])]
        ]
        popup = sg.Window('Caminho do arquivo de output', arquivo_layout)
        popup.read()

    def set_interval(func, sec):
        def func_wrapper():
            set_interval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()
    return t

Application()