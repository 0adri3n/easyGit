import download
import upload
import server
import io
import yaml

# Add all usernames
users = []

# Custom the name on the terminal
serverName = "easyGit"

# Get user info
try:
    f = open("conf.yaml", "r")
    data_loaded = yaml.safe_load(f)
    f.close()
    user = data_loaded["user"]
except:
    f = io.open("conf.yaml", "w", encoding="utf-8")
    print("All users :")
    print(*users, sep = " ")
    print("\n")
    user = input("Enter your name : ")
    while user not in users:
        user = input("Enter a valid name (part of the list) : ")
    data = {'user': user}
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    f.close()


#Terminal

print("'help' to display all commands")

term = True
while term:

    command = input(user + "@" + serverName + " > ")

    if command == "help":

        print("\n'download' [Download files from a selected user]")
        print("'upload' [Upload files. Care, all your files in your directory on the server will be replaced.]")
        print("'see' [See files in a user's directory]")
        print("'exit' [Stop easyGit]\n")

    elif command == "download":
        
        print("[Reminder: existing users] :")
        for i in users:
            print(i, end=" | ")
        u = input("\nSelect a user to download his file(s) : ")
        while user not in users:
            print("Invalid user.")
            u = input("Select a user to download his file(s) : ")
        
        f = input("File name (! with extension like [main.py] !) that you want to download [To download ALL files enter *] : ")
        download.get(u, f)

    elif command == "upload":

        confirmation = input("Care, all your files in your directory on the server will be replaced. Are you sure ? [yes/no] : ")
        while confirmation != "yes" and confirmation != "no":
            print("Invalid choice.")
            confirmation = input("Care, all your files in your directory on the server will be replaced. Are you sure ? [yes/no] : ")
        if confirmation == "yes":
            server.cleardir(user)
            upload.send(user)
        else:
            print("Upload canceled.")
    
    elif command == "see":

        print("[Reminder: existing users] :")
        for i in users:
            print(i, end=" | ")
        u = input("\nSelect a user to display his files : ")
        while user not in users:
            print("Invalid choice.")
            u = input("Select a user to display his files : ")
        server.get_files(u)

    elif command == "exit":

        term = False
        print("Bye !")

    else:

        print("Command not found.")