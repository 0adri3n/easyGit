from ftplib import FTP

# Enter the server's IP and logs to FTP (username & password)
IP = ""
USER = ""
PASSWORD = ""

print("[SERVER] Connection to the server...")
ftp = FTP(IP, USER, PASSWORD) 
print("[SERVER] Connection established.")

def get_files(user):
    
    print(ftp.dir(user))

def remove_ftp_dir(path):
    for (name, properties) in ftp.mlsd(path=path):
        if name in ['.', '..']:
            continue
        elif properties['type'] == 'file':
            ftp.delete(f"{path}/{name}")
        elif properties['type'] == 'dir':
            remove_ftp_dir(f"{path}/{name}")
    ftp.rmd(path)

def cleardir(user):

    remove_ftp_dir(user)
    ftp.mkd(user)