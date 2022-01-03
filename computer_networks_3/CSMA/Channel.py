import random
from _thread import *
from socket import *
from time import *

#creating server socket for channel
channel=socket(AF_INET,SOCK_STREAM)


#channel property

status="FREE"


host="localhost"
port=9000


#number of nodes connected to channel
onlineNodes=0


#try to bind to client
try:
    channel.bind((host,port))
except error as e:
    print("Error in binding"+str(e))

#reach this section only when binding is successful

#channel starts to listen for clients trying to connect
channel.listen(3)

def connection(node):

    global status
    #continuously listen to client request
    while True:
        status="BUSY"
        #sleep(random.choice(range(100)))
        data=node.recv(1024).decode('utf-8')
        print('$'+data)
        status = "FREE"
        if not data:
            break
        node.send(str(status).encode())

    node.close()

while True:
    NODE,ADDR=channel.accept()
    print("connected to" + str(ADDR))
    start_new_thread(connection,(NODE,))
    onlineNodes+=1
channel.close()