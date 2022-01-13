import sys
import subprocess

descricao = input('Qual a descição do seu commit?')
branch = input('Qual a branch?')

subprocess.run('git add .')
subprocess.run(f'git commit -m "{descricao}"')
subprocess.run(f'git push -u origin {branch}')

print(sys.argv[1])