import subprocess
import io
#def ping():
#    return str(subprocess.run(["exit", "1"], shell=True)).replace('\\n', '\n').replace('\\r', '')

#a = ping()
#arquivo = open("pings.txt", "w")
#arquivo.write(f'{a}\n')
#print(f'{a}\n')]

proc = subprocess.Popen('node .', cwd='C:\\Users\\grimm\\Desktop\\projetos\\clleitobot v13 ts\\runpy', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print('code: ' + str(proc.returncode))

proc.kill()