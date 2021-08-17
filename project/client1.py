from os import rename
import socket
from datetime import datetime
from numpy import empty
from pytz import timezone

format = "%H:%M"
# Current time in UTC
now_utc = datetime.now(timezone('UTC'))
# Convert to Asia/Kolkata time zone
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
DISCONNECT_MSG = "!DISCONNECT"
HOST = socket.gethostbyname(socket.gethostname())      # The remote host
PORT = 42050              # The same port as used by the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("A.Ticket Booking\nB.Reviews & Rating\nC.Upcoming movies")

connected = True
while connected:
    msg = str(input("> "))
    if msg == DISCONNECT_MSG:
        connected = False
        
    elif (str(msg)=="A"):
        client.send(str(msg).encode())
        data=client.recv(1024).decode()
        print(data)
        
        if(data is not empty):
            mov=input("Enter the index of movie name")
            client.send(str(mov).encode())
            no_of_seats=input("Enter the no.of seats:")
            client.send(str(no_of_seats).encode())
            choise=input("Do you need to order snacks?(y/n):")
            if(choise=="y"):
                print(client.recv(1024).decode())
                sitem=input("select no.of items")
                client.send(str(sitem).encode())
                for i in range(1,int(sitem)+1):
                    item=input("select the"+ str(i)+" item index:")
                    client.send(str(item).encode())
                    qitem=input("enter the quantity of "+ str(i)+"th item:")
                    client.send(str(qitem).encode())
                x=client.recv(1024).decode()
                print("total amount is "+x)
            else:
                client.recv(1024).decode()
            
        
    elif (str(msg)=="B"):
        client.send(str(msg).encode())
        a=input("Select one of the below:\nIn order to view select D\n In order to give review select E")
        client.send(str(a).encode())
        if(a=="D"):
            client.send(str(msg).encode())
            data=client.recv(1024).decode()
            print(data)
        else:
            rname=input("Enter your name:\n")
            client.send(str(rname).encode())
            rmov=input("Enter the movie name:\n")
            client.send(str(rmov).encode())
            rating=input("Provide your rating out of 5:\n")
            client.send(str(rating).encode())
            review=input("Describe in a one word about the movie:\n")
            client.send(str(review).encode())
            print(client.recv(1024).decode())
    elif (str(msg)=="C"):
        client.send(str(msg).encode())
        print(client.recv(1024).decode())
        umov=input("Select the movie name: ")
        client.send(str(umov).encode())
        result=client.recv(1024).decode()
        print(result)
        
        
    else:
        msg = client.recv(1024).decode()
        print(f"[SERVER] {msg}")





        
   
    
    
