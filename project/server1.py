from os import close
import socket
import re
from numpy import empty
import pandas as pd
import threading
from datetime import datetime
from pytz import timezone
format = "%H:%M"
# Current time in UTC
now_utc = datetime.now(timezone('UTC'))
# Convert to Asia/Kolkata time zone
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
time=now_asia.strftime(format)
h=re.findall("[0-9]+",str(time))
H1=int(h[0])
H2=int(h[1])/60
total=H1+H2
print(total)

DISCONNECT_MSG = "!DISCONNECT"
HOST = ""       # server ip
PORT = 42050   # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except socket.error as error:
    # printing the error here
    print("Oops!. Please check the error and try again " + str(error))
print ("ticket booking  Server running", HOST, PORT)
s.listen()
print ("Sending Data ....")  

def  update (movie_name,seats):
    df=pd.read_csv("ticket.csv")
    x=df.iloc[movie_name]["leftseats"]
    df.at[movie_name, "leftseats"] -= seats
    df.to_csv("ticket.csv",index=7)
    x=df.at[movie_name, "price"]
    x=x*int(seats)
    print(df)
    return x
    
     

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(1024).decode()
        
        if msg == DISCONNECT_MSG:
            connected = False
            
        elif(str(msg)=="A"):
            print("option 1 selected")
            df=pd.read_csv("ticket.csv")
            df=df[df["hours"]>total][['mname','genre','price','time','place','Seats','leftseats']]
            conn.send(str(df).encode())
            if(df is not empty):
                mov=int(conn.recv(1024).decode())
                st=int(conn.recv(1024).decode())
                t=update(mov,st)
                d1=pd.read_csv("Snacks.csv")
                conn.send(str(d1).encode())
                sitem=int(conn.recv(1024).decode())# no.of items
                df=pd.read_csv("Snacks.csv")
                
                while(sitem>0):
                    i=int(conn.recv(1024).decode())#index of  items
                    x=df.at[i,"Price"] 
                    j=conn.recv(1024).decode()#quantity
                    t=t+int(x)*int(j)
                    sitem=sitem-1
                conn.send(str(t).encode())
                t=0
                    
                
        
        elif(str(msg)=="B"):
            print("option 2 selected")
            opt=conn.recv(1024).decode()
            if(opt=="D"):
                df=pd.read_csv("rating.csv")
                conn.send(str(df).encode())
            else:
                rname=conn.recv(1024).decode()
                rmov=conn.recv(1024).decode()
                rating=conn.recv(1024).decode()
                review=conn.recv(1024).decode()
                df=pd.read_csv("rating.csv")
                data=[pd.Series([rname,rmov,rating,review],index=df.columns)]
                df=df.append(data,ignore_index=True)
                df.to_csv("rating.csv",index=False)
                print(df)
                conn.send(str("Review inserted").encode())
            
        
        elif(str(msg)=="C"):
            print("option 3 selected")
            df=pd.read_csv("upcoming.csv")
            df=df[["mname"]]
            conn.send(str(df).encode())
            umov=conn.recv(1024).decode()
            d=pd.read_csv("upcoming.csv")
            d.set_index("mname", inplace = True)
            x=d.loc[umov]
            print(x)
            conn.send(str(x).encode())

        print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"
        

    conn.close()



while True:
    conn , addr =s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print("recieved from client")
    
        
       
        

    