import subprocess

#def ping():
#    return str(subprocess.run(["exit", "1"], shell=True)).replace('\\n', '\n').replace('\\r', '')

#a = ping()
#arquivo = open("pings.txt", "w")
#arquivo.write(f'{a}\n')
#print(f'{a}\n')]

proc = subprocess.Popen('ipconfig', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

o, e = proc.communicate()

print(str(proc.stdout))
print('Error: '  + e.decode('ascii'))
print('code: ' + str(proc.returncode))