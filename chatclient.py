'''
Name: Lam Truong 15119071
Date 11/10
Assignment 3
'''

from socket import *
import sys
import os
from sys import *
from _thread import *
import time

#Function to receive message
def receive_messages(receive_socket):
    while True:
        message = receive_socket.recv(1024).decode()
        #If input wrong password, close in 3s
        if message == "- Wrong credentials. Closing in 3s" :
            print(message)
            time.sleep(3)
            receive_socket.close()
            os._exit(0)
        #If input command 'ex' then close in 3s
        elif message == 'Exit':
            print("Exiting...")
            time.sleep(3)
            os._exit(0)
        print(message)

#Function to send message
def send_messages(send_socket):
    while True:
        data = input()
        send_socket.send(data.encode())    

def main():
    arg1 = argv[1]
    arg2 = argv[2]
    arg3 = argv[3]
    #Check if port is a number
    try: 
        value = int(arg2)
    except ValueError:
        print("Port must be a number")
        exit()
    #Setup servername, port, and message from inputs 
    serverName = arg1
    serverPort = int(arg2)
    username = argv[3]
    #Set up client
    my_socket = socket()
    my_socket.connect((serverName, serverPort))
    my_socket.send(username.encode())
    #Start 2 threads
    start_new_thread(receive_messages, (my_socket, )) 
    start_new_thread(send_messages, (my_socket, ))
    time.sleep(1000)  #this delay lets the threads kick in, otherwise the thread count is zero and it crashes
    my_socket.close()
    sys,exit()
#Run main 
if __name__ == '__main__':
    main()