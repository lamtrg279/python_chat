from socket import *
import json
import sys
from _thread import *
import time

#Function to let client connect and input chat commands
def clientThread(connection, clients, listOfConnections): 
  try:
    while True:
      username = connection.recv(1048).decode()
      #If new user, let user create new password
      if (username not in clients):
        message = "- User not found. Create new user.\nEnter new password: "
        connection.send(message.encode())
        password = connection.recv(1048).decode()
        #Save password to clients object
        clients[username] = password
        #Save username to corresponding socket connection
        listOfConnections[username] = connection
        message = "- Connected to server"
        connection.send(message.encode())
        #Save username and password to text file
        with open('account.txt', 'w') as file:
          file.write(json.dumps(clients))
      else :
        message = "- User found. Enter password: "
        connection.send(message.encode())
        password = connection.recv(1048).decode()
        #If password is correct
        if (clients[username] == password):
          connection.send("\n- Login success".encode())
        #Save username to corresponding socket connection
          listOfConnections[username] = connection
          message = "- Connected to server"
          connection.send(message.encode())
        else:
          #Wrong password
          connection.send("- Wrong credentials. Closing in 3s".encode())
          time.sleep(3)
      clientHandler(connection, listOfConnections, username) #Handling commands
  except Exception as e:
    print()

def clientHandler(connection, listOfConnections, username):
  try: 
    while True:
      #Prompt clinet
      print("Waiting for operation...")
      connection.send("\n* Please enter a command: PM (public message), DM (direct message), EX (exit)".encode())
      message = connection.recv(1048).decode()
      #If command is PM then proceed
      if message.split(" ")[0].upper() == "PM":
        connection.send("\n* Enter the public message: ".encode())
        message = connection.recv(1048).decode()
        #Send message to every user in listOfConnection except itself
        for user in listOfConnections:
          if listOfConnections[user] == connection: 
            continue
          header = ("\n*** Public Message ***")
          listOfConnections[user].send(header.encode())
          sender = "Public message from " + username + ": " + message
          listOfConnections[user].send(sender.encode())
          listOfConnections[user].send("\n\n* Please enter a command: PM (public message), DM (direct message), EX (exit)".encode())
        #Confirmation to client
        connection.send("-> Public message sent succesfully.".encode())
        print("Public message was sent successfully.\n")
      #If command is DM then proceed
      elif message.split(" ")[0].upper() == "DM":
        header = ("\n- Users online:")
        connection.send(header.encode())
        #Show every online user except itself
        for user in listOfConnections: 
          if (listOfConnections[user] == connection):
            continue
          connection.send(user.encode())
          connection.send("\n".encode())
        #If only 1 is online (which is itself) 
        if (len(listOfConnections) == 1):
          connection.send("!!! No user is online at the moment.\n".encode())
          continue
        #Prompt client to pick a user, then type in message
        connection.send("\n* Choose a user:".encode())
        target = connection.recv(1048).decode()
        #Case when user is not online or does not exist
        if target not in listOfConnections:
          connection.send("\n !!! User doesn't exist. Please start again and choose a currently online user.".encode())
          print("Direct message failed.")
          continue
        connection.send("\n* Enter the direct message: ".encode())
        message = connection.recv(1048).decode()
        #Send message
        header = ("\n*** Direct Message ***")
        listOfConnections[target].send(header.encode())
        sender = "Direct message from " + username + ": " + message
        listOfConnections[target].send(sender.encode())
        listOfConnections[target].send("\n\n* Please enter a command: PM (public message), DM (direct message), EX (exit)".encode())
        #Confirmation to client
        connection.send("-> Direct message sent successfully.\n".encode())
        print("Direct message was sent succesfully.\n")
      elif message.split(" ")[0].upper() == "EX":
        #Print out info that user exits
        print(username + " logged out.\n")
        connection.send("Exit".encode())
        #Remove connection 
        listOfConnections.pop(username)
        time.sleep(3)
        connection.close()
  except Exception as e:
    print()
      
def main():
  #Inport port
  arg1 = sys.argv[1]
  serverHost = 'localhost'
  serverPort = int(arg1)
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind((serverHost, serverPort))
  serverSocket.listen(10)
  print("\nListen on port "+ str(serverPort) + "\nWaiting ...\n")
  #Read usernames, passwords from file
  file = open('account.txt', 'r')
  data = file.read()
  listOfClients = json.loads(data)
  listOfConnections = {}
  #Listen to connection
  while True:
    connection, address = serverSocket.accept()
    print(str(address[0]) + ":" + str(address[1]) + ' connected')
    start_new_thread(clientThread, (connection, listOfClients, listOfConnections))
  serverSocket.close()
#Run main
if __name__ == '__main__':
  main()
