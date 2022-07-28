### ======================================= ###
'''Rishabh Goswami & Zahir Ali
server.py
Please install dependencies from requirements.txt and look at Readme.md for details.
The messages between client and server are encrypted using AES encryption
'''
### ======================================= ###

import pandas as pd
import numpy as np
import socket
import csv
import time
import json
from mlmodel import pred_CSV_Email, pred_Text_Email, update_CSV_With_Results, accuracyscore, terminalColor
from Crypto.Cipher import AES
import os
import tqdm

os.system("")

IP = '127.0.0.1'
PORT = 6969
ADDR = (IP, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
FORMAT = 'utf-8'
BUFFER_SIZE = 1024
key = "EuZKgxZfCGPzCZEj"
IV = "POoddMaPkiPSQlsW"

print(f'Server is starting at {IP}:{PORT}')
server.listen()
print(f'Server is now listening')

# Loading usernam and password from users file.
userlist = {}
try: 
    with open('./server/users.json', 'r') as fp:
        userlist = json.load(fp)

except:
    print(f"{terminalColor.RED}Error while reading the json{terminalColor.END}")
    

#Checks if the user exists in the userlist
def checkuser(): 
    encryptedResponse = conn.recv(BUFFER_SIZE)
    username = decrypted(encryptedResponse)
    username = username.lower()
    if username in userlist.keys():
        encryptedMessage = encrypted('UserOK.')
        conn.send(encryptedMessage)
        check_password(username)
    else:
        encryptedMessage = encrypted('Email not registered')
        conn.send(encryptedMessage)
        create_password(username)

#Checks if the password is correct, moves to fetch name if correct, loops if wrong
def check_password(username): 
    encryptedResponse = conn.recv(BUFFER_SIZE)
    password = decrypted(encryptedResponse)
    if password == userlist[username]:
        encryptedMessage = encrypted('Password verified.')
        print(f'{terminalColor.GREEN}Password verified.{terminalColor.END}')
        conn.send(encryptedMessage)
    else:
        print(f'{terminalColor.YELLOW}Password not verified.{terminalColor.END}')
        encryptedMessage = encrypted('Password not verified.')
        conn.send(encryptedMessage)
        time.sleep(0.5)
        check_password(username)

# Take password from the client and save it in the user.json file
def create_password(username): #Creates a new password for the user
    encryptedResponse = conn.recv(BUFFER_SIZE)
    password = decrypted(encryptedResponse)
    userlist[username] =  password
    with open('./server/users.json', 'w') as fp:
        json.dump(userlist, fp)
    

    encryptedMessage = encrypted(f'{terminalColor.GREEN}User created.{terminalColor.END}')
    conn.send(encryptedMessage)

# Receive file from client
def receiveFile():
    print(f'Receiving File.')
    filetodown = open("./server/datafile.csv", "wb")
    while True:
        data = conn.recv(BUFFER_SIZE)
        if len(data) < BUFFER_SIZE:
            
            break
        filetodown.write(data)
        
    filetodown.close()

    print('File Saved.')

# Send file to the server
def sendFile():
    filesize = os.path.getsize("./server/datafile.csv")
    progress = tqdm.tqdm(range(filesize), desc=f"Sending Output File...", unit="B", unit_scale=True, unit_divisor=1024)
    filetosend = open("./server/datafile.csv", "rb")
    #data = filetosend.read(BUFFER_SIZE)
    while True:
        data = filetosend.read(BUFFER_SIZE)
        if not data:
            break
        conn.send(data)
        progress.update(len(data))
    filetosend.close()
    


# Encrypt the message
def encrypted(message,key = key,IV=IV):
    message = message.encode(FORMAT)
    encObj = AES.new(key.encode(FORMAT), AES.MODE_CFB, IV.encode(FORMAT))
    encryptedMessage = encObj.encrypt(message)
    return encryptedMessage

# Deccrypt the message
def decrypted(ciphertext,key = key,IV=IV):
    encObj = AES.new(key.encode(FORMAT), AES.MODE_CFB, IV.encode(FORMAT))
    message = encObj.decrypt(ciphertext)
    return message.decode(FORMAT)


#keeps the server running
while True: 

    conn, addr = server.accept() #accept incoming conn

    connected = True

    def receiveMessage():
        encryptedResponse = conn.recv(BUFFER_SIZE)
        response = decrypted(encryptedResponse)
        return response

    def sendMessage(message):
        encryptedMessage = encrypted(message)
        conn.send(encryptedMessage)
        
        
    print(f'******************************\nConnected by \033[96m{addr}\033[0m') #print the address of the client

    # Communication with the client    
    while connected:

        try:

            sendMessage(f"Welcome to spam detector!\nPlease {terminalColor.CYAN}login{terminalColor.END} to continue.")

            checkuser()

            mess = encrypted(f"Please select if you want to send a csv file to be processed, or just a single string of text: \n For text, type {terminalColor.CYAN}\'text\'{terminalColor.END}, after which you will be prompted to enter the text \n For csv file, place the file in the \'client\' directory and name it input.csv, and type {terminalColor.CYAN}\'file\'{terminalColor.END} \n")
            conn.send(mess)

            response = receiveMessage()

            if response.lower() == "text":

                sendMessage("You have chosen to send a text.")
                response = receiveMessage()
                if len(response)>0:
                    pred = pred_Text_Email(response)
                    if str(pred[0])=='ham':
                        predict = f"{terminalColor.GREEN}ham (NOT a spam){terminalColor.END}"
                    else:
                        predict = f"{terminalColor.RED}Spam{terminalColor.END}"
                    sendMessage(f'Prediction: {predict}\n')
                    sendMessage(f"Accuracy of the model : \033[96m{accuracyscore}\033[0m")
                else:
                    sendMessage(f'Error: You have not entered any text to predict\n')
                    sendMessage(f"Accuracy of the model : \033[96m{accuracyscore}\033[0m")

            elif response.lower() == "file":

                sendMessage(f"\nFile transfer is about to begin. Please wait.")
                receiveFile()
                print(f"{terminalColor.CYAN}Transfer Complete.{terminalColor.END}")
                pred, messages = pred_CSV_Email()
                update_CSV_With_Results(pred, messages)
                time.sleep(3)
                sendFile()
                print(f"{terminalColor.CYAN}File Sent.{terminalColor.END}")
                print(f"Accuracy of the model : \033[96m{accuracyscore}\033[0m")

            else:
                sendMessage(f"{terminalColor.RED}Invalid Option. Closing the connection!{terminalColor.END}")

            conn.close()

        except:
            connected = False #ends the connection if an error occurs
            conn.close()
            
            print(f'\n{terminalColor.RED}Connection Closed.{terminalColor.END}\nWaiting for new connection...\n')
            break


