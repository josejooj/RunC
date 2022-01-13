import sys
import subprocess
import re

descricao = ''
for i in sys.argv:
    if re.search(r'^name=[^ \n]+$', i) == None and descricao != '': descricao = input('Qual a descição do seu commit? ')
    else: descricao = i[5:99999]

print(descricao)

subprocess.run('git add .')
subprocess.run(f'git commit -m "{descricao}"')
subprocess.run(f'git push -u origin main')

print(sys.argv[1])