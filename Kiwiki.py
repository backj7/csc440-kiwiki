import os
from pathlib import Path, PurePath
from wiki.data.install import install
import subprocess as sp
import sys

if __name__ == '__main__':
    pypy = PurePath(Path(sys.executable).resolve())
    riki_path = PurePath(Path(os.getcwd(), 'Riki.py'))
    db_path = PurePath(Path(os.getcwd()), 'mdb')
    db_exec_path = PurePath(db_path, 'bin/mysqld.exe')
    if not os.path.exists(db_path):
        install()
    db_server = sp.Popen([str(db_exec_path), ' --console'], stderr=sp.DEVNULL, stdout=sp.DEVNULL)
    riki_server = sp.Popen([str(pypy), str(riki_path)], stderr=sp.DEVNULL, stdout=sp.DEVNULL)

    print('Type quit to kill the server')
    command = ''
    while command != 'quit':
        command = input('> ')
        command = command.lower()

    riki_server.kill()
    db_server.kill()