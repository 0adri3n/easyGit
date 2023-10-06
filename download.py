from ftplib import FTP
# Enter the server's IP and logs to FTP (username & password)
IP = ""
USER = ""
PASSWORD = ""

print("[DOWNLOAD] Connection to the server...")
ftp = FTP(IP, USER, PASSWORD) 
print("[DOWNLOAD] Connection established.")

import ftplib
import os
import re
from pathlib import Path


def _is_ftp_dir(ftp_handle, name, guess_by_extension=True):


    if guess_by_extension is True:
        if len(name) >= 4:
            if name[-4] == '.':
                return False

    original_cwd = ftp_handle.pwd() 
    try:
        ftp_handle.cwd(name) 
        ftp_handle.cwd(original_cwd)
        return True

    except ftplib.error_perm as e:
        print(e)
        return False

    except Exception as e:
        print(e)
        return False


def _make_parent_dir(fpath):
    dirname = os.path.dirname(fpath)
    while not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
            print("created {0}".format(dirname))
        except OSError as e:
            print(e)
            _make_parent_dir(dirname)


def _download_ftp_file(ftp_handle, name, dest, overwrite):
    _make_parent_dir(dest.lstrip("/"))
    if not os.path.exists(dest) or overwrite is True:
        try:
            with open(dest, 'wb') as f:
                ftp_handle.retrbinary("RETR {0}".format(name), f.write)
            print("downloaded: {0}".format(dest))
        except FileNotFoundError:
            print("FAILED: {0}".format(dest))
    else:
        print("already exists: {0}".format(dest))


def _file_name_match_patern(pattern, name):
    if pattern is None:
        return True
    else:
        return bool(re.match(pattern, name))


def _mirror_ftp_dir(ftp_handle, name, overwrite, guess_by_extension, pattern):
    for item in ftp_handle.nlst(name):
        if _is_ftp_dir(ftp_handle, item, guess_by_extension):
            _mirror_ftp_dir(ftp_handle, item, overwrite, guess_by_extension, pattern)
        else:
            if _file_name_match_patern(pattern, name):
                _download_ftp_file(ftp_handle, item, item, overwrite)
            else:
                pass


def download_ftp_tree(ftp_handle, path, destination, pattern=None, overwrite=False, guess_by_extension=True):

    path = path.lstrip("/")
    original_directory = os.getcwd()  # remember working directory before function is executed
    os.chdir(destination)  # change working directory to ftp mirror directory

    _mirror_ftp_dir(
        ftp_handle,
        path,
        pattern=pattern,
        overwrite=overwrite,
        guess_by_extension=guess_by_extension)

    os.chdir(original_directory)  # reset working directory to what it was before function exec


def get(user, file):

    if file != "*":
        Path(user).mkdir(parents=True, exist_ok=True)
        try:
            path = user + "/" + file
            filenames = ftp.nlst(user)
            if path in filenames:
                with open(path, "wb") as f:
                    ftp.retrbinary(f"RETR {path}", f.write)
                print("File downloaded.")
            else:
                print("File not found.")
        except:
            print("Error.")

    else:
        download_ftp_tree(ftp, user, Path(__file__).parent.resolve(), overwrite=False, guess_by_extension=True)