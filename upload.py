from ftplib import FTP, error_perm
import os.path, os

# Enter the server's IP and logs to FTP (username & password)
IP = ""
USER = ""
PASSWORD = ""

print("[UPLOAD] Connection to the server...")
ftp = FTP(IP, USER, PASSWORD) 
print("[UPLOAD] Connection established.")

def send(user):
    
    for name in os.listdir(user):

            localpath = user + "/" + name
            if os.path.isfile(localpath):
                print("Uploading", localpath)
                ftp.storbinary('STOR ' + localpath, open(localpath,'rb'))
            elif os.path.isdir(localpath):
                print("Folder creation :", localpath)

                try:
                    ftp.mkd(localpath)

                except error_perm as e:
                    if not e.args[0].startswith('550'): 
                        raise

                print("Switching folder in", localpath)
                send(localpath)           

