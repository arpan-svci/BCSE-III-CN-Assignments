from socket import *

import non_persistentAlgorithm
import one_persistentAlgorithm

#creating node socket
import p_persistentAlgorithm

node=socket(AF_INET,SOCK_STREAM)

host='localhost'
port=9000

#trying connecting to server channel
try:
    node.connect((host,port))
except error as e:
    print("Error in connecting" + str(e))

#code moves to this section only after successful connection with server
prop_time=int(input("Enter Propagation time:"))
choice=int(input("Enter Choice\n 1. 1-Persistent Method \n 2. Non-Persistent Method \n 3. p-Persistent Method\n"))
if choice==1:
    while True:
        Input=str(input("$"))
        node.send(Input.encode())
        Response=node.recv(1024).decode('utf-8')
        if one_persistentAlgorithm.sensing(Response,prop_time):
            continue
        else:
            break
    node.close()

elif choice==2:
    while True:
        Input=str(input("$"))
        node.send(Input.encode())
        Response=node.recv(1024).decode('utf-8')
        if non_persistentAlgorithm.sensing(Response,prop_time):
            continue
        else:
            break
    node.close()

elif choice==3:
    p=float(input("Enter probability p:"))
    while True:
        Input=str(input("$"))
        node.send(Input.encode())
        Response=node.recv(1024).decode('utf-8')
        if p_persistentAlgorithm.sensing(Response,prop_time,p):
            continue
        else:
            break
    node.close()