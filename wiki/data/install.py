import platform
from requests import get
from urllib.request import urlretrieve
from zipfile import ZipFile
from os import mkdir, remove, rename, walk, getcwd
from os.path import exists, join
import subprocess
from pathlib import Path

def install():
    db_ver = '10.7.3'
    os_str = platform.system()

    params = {'os':os_str}
    endpoint = 'https://downloads.mariadb.org/rest-api/mariadb/' + db_ver + '/'
    req = get(endpoint, params=params)
    print('File list retrieved from', req.url)
    f_options = req.json()['release_data'][db_ver]['files']

    if os_str == 'Windows':
        print('Checking file list for correct file type')
        for file in f_options:
            if '.zip' in file['file_name'] and not 'debugsymbols' in file['file_name']:
                print('File found, downloading...')
                archive_path = './archive.zip'
                unzip_dir_path = getcwd()
                urlretrieve(file['file_download_url'], archive_path)
                print('Done.')
                print('Unzipping archive...')
                with ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(unzip_dir_path)
                print('Done.')
                remove(archive_path)
                for (dirpath, dirnames, filenames) in walk(unzip_dir_path):
                    if 'mariadb' in dirpath:
                        parent = Path(dirpath).parent.absolute()
                        rename(dirpath, parent.joinpath('mdb'))
                        break
                subprocess.run([join(unzip_dir_path, 'mdb/bin/mysql_install_db.exe')])
                break
    elif os_str == 'Linux':
        pass # Not implemented yet

if __name__ == '__main__':
    pass