from threading import Thread
import time
import random
from multiprocessing import Pipe
sender_send,channel_receive_from_sender=Pipe()
channel_send_to_reciver,receiver_receive=Pipe()
receiver_send,channel_receive_from_receiver=Pipe()
channel_send_to_sender,sender_receive=Pipe()
def make_frame(sn,data):
    return str(sn)+data
class sender:
    def __init__(self) -> None:
        self.event=0
        self.frame=0
        self.interval=1
        self.cansend=True
        self.sn=0
        self.data=["abc","def","ghi","jkl","mno","pqr","stu","vwx","yza","bcd"]
        self.sender_send=Thread(target=self.send,name='sender_send')
        self.sender_receive=Thread(target=self.receive,name="sender_receive")
    def send(self):
        print("sending start")
        while self.cansend:
            time.sleep(1)
            t=time.time()
            while self.event==0:
                pass
            if(self.event==1 and self.cansend):
                f=make_frame(self.sn,self.data[self.sn])
                self.frame=0
                sender_send.send(f)
                print("1 :"+f)
                t1=time.time()
                while True:
                    if(self.frame==1):
                        break
                    if(time.time()-t1>self.interval or self.frame==2):
                        break
                self.frame=0           
        
    def receive(self):
        print("recive in send start")
        q=[]
        while True:
            q.append(sender_receive.recv())
            k=q.pop(0)
            if(k==self.sn):
                self.frame=1
                self.sn+=1
            elif k==len(self.data):
                self.cansend=False
            else:
                self.frame=1
                
class channel:
    def __init__(self,sender:sender) -> None:
        self.take_from_sender_send_to_receiver=Thread(target=self.receive_from_sender_pass_to_receiver,args=(sender,),name="take_from_sender_send_to_receiver")
        self.take_from_receiver_send_to_sender=Thread(target=self.receive_from_receiver_pass_to_sender,name="take_from_receiver_send_to_sender")
    def receive_from_sender_pass_to_receiver(self,sender:sender):
        q=[]
        print("receive_from_sender_pass_to_receiver start")
        counter=0
        while True:
            sender.event=1
            q.append(channel_receive_from_sender.recv())
            r=q.pop(0)
            time.sleep(3*random.random())
            channel_send_to_reciver.send(r)
            counter+=1
    def receive_from_receiver_pass_to_sender(self):
        q=[]
        print("in receive_from_receiver_pass_to_sender start")
        while True:
            q.append(channel_receive_from_receiver.recv())
            r=q.pop(0)
            channel_send_to_sender.send(r)

class receiver:
    def __init__(self) -> None:
        self.sn=0
        self.right=True
        self.process=Thread(target=self.receive_and_send)
    def receive_and_send(self):
        print("receiver start")
        q=[]
        while True:
            q.append(receiver_receive.recv())
            data=q.pop(0)
            if(self.right):
                receiver_send.send(int(data[0]))

if __name__=='__main__':
    s1=sender()
    c=channel(s1)
    r1=receiver()
    s1.sender_send.start()
    s1.sender_receive.start()
    c.take_from_receiver_send_to_sender.start()
    c.take_from_sender_send_to_receiver.start()
    r1.process.start()
    s1.sender_send.join()
    r1.process.join()
    s1.sender_receive.join()
    c.take_from_receiver_send_to_sender.join()
    c.take_from_sender_send_to_receiver.join()