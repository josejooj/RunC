from datetime import datetime
import subprocess
import os

def ask(string: str):
    os.system('CLS')
    print('     ##############################################')
    print('     #                                            #')
    print('     #        Github commit system v1.0           #')
    print('     #           Made by cleiton2040              #')
    print('     #                                            #')
    print('     ##############################################\n')
    return input(f"     {string}\n   > ")

data = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
user = ask("Qual o seu nome de usuário?")
desc = ask("Qual a descrição do seu commit?")
descricao = f"[{data}] - Commit requested by \"{user}\""
if desc: descricao += f" (\"{desc}\")"

print(descricao)

subprocess.run(f'git add .')
subprocess.run(f'git commit -m "{descricao}"')
subprocess.run(f'git push -u origin main')