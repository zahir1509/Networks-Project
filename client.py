### ======================================= ###
'''Rishabh Goswami & Zahir Ali
client.py
Please install dependencies from requirements.txt and look at Readme.md for details.
The messages between client and server are encrypted using AES encryption

- Client first register itself on the server and set password, 
if the username already registered then client simply provide password to authenticate

- After authentication client can chose to input either string of text or a file to get the prediction 
whether the message/ messages are spam or ham.
'''
### ======================================= ###

import socket
import time
from Crypto.Cipher import AES
import os   
from mlmodel import terminalColor
import tqdm

os.system("")

SERVER_IP = '127.0.0.1'
PORT = 6969
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 1024
key = "EuZKgxZfCGPzCZEj"
IV = "POoddMaPkiPSQlsW"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print(f'{terminalColor.GREEN}Connected to server.{terminalColor.END}\n')


# Send file from client to server
def sendFile():
    filesize = os.path.getsize("./client/input.csv")
    #client.send(f'{filesize}'.encode())
    progress = tqdm.tqdm(range(filesize), desc=f"Sending File...", unit="B", unit_scale=True, unit_divisor=1024)
    filetosend = open("./client/input.csv", "rb")
    #data = filetosend.read(BUFFER_SIZE)
    while True:
        data = filetosend.read(BUFFER_SIZE)
        if not data:
            break
        client.sendall(data)
        progress.update(len(data))
        
    filetosend.close()
    

# Recieve the file from server to client 
def receiveFile():
    print(f'{terminalColor.GREEN}Receiving File...{terminalColor.END}')
    filetodown = open("./client/output.csv", "wb")
    while True:
        data = client.recv(BUFFER_SIZE)
        filetodown.write(data)
        if len(data) < BUFFER_SIZE:
            print(f"{terminalColor.CYAN}Transfer Complete.{terminalColor.END}")
            break
        
    filetodown.close()
    print('Output File Saved in client directory.')



# Get username from the user and send the username to the server    
def getuser():
    username = input('Enter your username: ')
    encryptedMessage = encrypted(username)
    client.send(encryptedMessage)
    data = receiveMessageReturn()
    if data == 'UserOK.':
        print(f'{terminalColor.CYAN}User verified.{terminalColor.END}')
        getpass()
    else:
        print(f'{terminalColor.CYAN}User does not exist. Please create a password for one-time registration.{terminalColor.END}')
        createpass()

# Get password from the user if user is registered and send the password to the server
def getpass():
    password = input('Enter your password: ')
    encryptedMessage = encrypted(password)
    client.send(encryptedMessage)

    data = receiveMessageReturn()
    if data == 'Password verified.':
        print(f'{terminalColor.GREEN}Password verified.{terminalColor.END}')
    else:
        print(f'{terminalColor.RED}Password not verified.{terminalColor.END}')
        if password == 'q':
            conn.close() #not needed
            return
        getpass()

# Get password from the user if user is NOT registered and send the password to the server
def createpass():
    password = input('Enter your password: ')
    encryptedMessage = encrypted(password)
    client.send(encryptedMessage)
    

    data = client.recv(1024)
    response = decrypted(data)
    print(response)

# Encrypt the message going from client to server
def encrypted(message,key = key,IV=IV):
    message = message.encode(FORMAT)
    encObj = AES.new(key.encode(FORMAT), AES.MODE_CFB, IV.encode(FORMAT))
    encryptedMessage = encObj.encrypt(message)
    
    return encryptedMessage

# Decrypt the messages coming from server to client
def decrypted(ciphertext,key = key,IV=IV):
    encObj = AES.new(key.encode(FORMAT), AES.MODE_CFB, IV.encode(FORMAT))
    message = encObj.decrypt(ciphertext)
    return message.decode(FORMAT)

def receiveMessage():
    encryptedResponse = client.recv(1024)
    response = decrypted(encryptedResponse)
    if len(response) > 0:
        print(response)

def receiveMessageReturn():
    encryptedResponse = client.recv(1024)
    response = decrypted(encryptedResponse)
    return response

def sendMessage(msg):
    encryptedMessage = encrypted(msg)
    client.send(encryptedMessage)


receiveMessage()  #Welcome to spamdetector, login to continue.

getuser()

receiveMessage()

# Check if user wants to send string of text or a file
msg = input('Type your Response: ')
sendMessage(msg)
receiveMessage()

if msg.lower() == 'text':
    msg = input('Enter the text to process: ')
    sendMessage(msg)
    receiveMessage()
    receiveMessage()

elif msg.lower() == 'file':
    sendFile()
    print(f"\nFile Sent.")
    print(f'\nPlease wait for the server to process and send output...\n') 
    time.sleep(5)  
    receiveFile()
    time.sleep(2)
    receiveMessage()

else:
    receiveMessage()

# Keep the terminal/ Console open until user input quit
while True:
    a = input(f'Type \'q\' or \'quit\' to close the console. \n')

    if a.lower() == 'q' or a.lower() == 'quit':
        client.close()
        break
    else:
        continue