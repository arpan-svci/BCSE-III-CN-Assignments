from threading import Thread
from multiprocessing import Pipe
msg=["hay","hello","hruu","kollol","aniket","satabda","rahul","nirmalya","end"]
import time
def send_msgs(conn,conn1,msgs):
    for msg in msgs:
        time.sleep(1.0)
        conn.send(msg)
        print(conn1.recv())
    conn.close()
def recv_message(conn,conn1):
    while True:
        msg=conn.recv()
        if msg=="end":
            conn1.send("success")
            break
        print(msg)
        conn1.send("success")
parent,child=Pipe()
parent1,child1=Pipe()
p1=Thread(target=send_msgs,args=(parent,child1,msg))
p2=Thread(target=recv_message,args=(child,parent1))
if __name__=='__main__':
    p1.start()
    p2.start()
    p1.join()
    p2.join()