import sys
import subprocess
import re
import math

descricao = sys.argv[1]

if re.search(r'^name=[^ \n]+$', sys.argv[1]) == None: descricao = input('Qual a descição do seu commit? ')
else: descricao = sys.argv[1][5:math.inf]

print(descricao)

branch = input('Qual a branch? ')

subprocess.run('git add .')
subprocess.run(f'git commit -m "{descricao}"')
subprocess.run(f'git push -u origin {branch}')

print(sys.argv[1])