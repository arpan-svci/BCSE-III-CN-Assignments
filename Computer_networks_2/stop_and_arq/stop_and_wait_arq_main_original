from threading import Thread
import time
import random
from multiprocessing import Queue
from crc import *

C_receiver=Queue()
D_receiver=Queue()

channel_recv=Queue()
channel_send=Queue()

A_sender_recv=Queue()
B_sender_recv=Queue()

probablity_of_success=0.9

def make_frame(sn,data,source,destination):
    k=bin(sn)[2:]
    l=bin(len(data))[2:]
    if len(k)<16:
        k=(16-len(k))*'0'+k
    if(len(l)<16):
        l=(16-len(l))*'0'+l
    generator='10011'
    data=codewords(datawords(data,generator),generator)
    return '1010101010101010'+k+source+destination+l+data

def get_data_from_frame(f):
    sn=int(f[16:32],2)
    length=f[34:50]
    data=f[50:]
    generator='10011'
    r=crc_decoding(data,int(length,2),generator)
    if(r=='correct'):
        isright=True
    else:
        isright=False
    data=data[50:50+int(length,2)]
    source=f[32]
    destination=f[33]
    return sn,data,isright,source,destination

class sender:
    def __init__(self,data,q,destination,source) -> None:
        self.destination=destination
        self.source=source
        self.event=0
        self.frame=0
        self.interval=1
        self.cansend=True
        self.sn=0
        self.data=data
        self.sender_send=Thread(target=self.send,name='sender_send')
        self.sender_receive=Thread(target=self.receive,args=(q,),name="sender_receive")
    def send(self):
        print("sending start")
        while self.cansend:
            time.sleep(random.random()/10)
            while self.event==0:
                pass
            if(self.event==1 and self.cansend):
                f=make_frame(self.sn,self.data[self.sn],self.source,self.destination)
                self.frame=0
                print(self.sn,self.source,self.destination)
                channel_recv.put(f)
                t1=time.time()
                while True:
                    if(self.frame==1):
                        break
                    if(time.time()-t1>self.interval or self.frame==2):
                        break
                self.frame=0           
        
    def receive(self,q:Queue):
        print("recive in send start")
        while self.cansend:
            k=q.get()
            if(k==self.sn):
                self.frame=1
                self.sn+=1
            elif k==len(self.data):
                self.cansend=False
            else:
                self.frame=1
                
class channel:
    def __init__(self,sender:list) -> None:
        self.list_of_sender=sender
        self.take_from_sender_send_to_receiver=Thread(target=self.take_from_sender_pass_to_receiver,name="take_from_sender_send_to_receiver")
        self.take_from_receiver_send_to_sender=Thread(target=self.take_from_receiver_pass_to_sender,name="take_from_receiver_send_to_sender")
    def take_from_sender_pass_to_receiver(self):
        q=[]
        print("receive_from_sender_pass_to_receiver start")
        while True:
            for _ in self.list_of_sender:
                _.event=1
            while channel_recv.empty():
                pass
            r=channel_recv.get()
            time.sleep(random.random()*0.2)
            if(r[33]=='C'):
                C_receiver.put(r)
            if(r[33]=='D'):
                D_receiver.put(r)
            for _ in self.list_of_sender:
                _.event=0
            # while not channel_recv.empty():
            #     k=channel_recv.get()
    def take_from_receiver_pass_to_sender(self):
        print("in receive_from_receiver_pass_to_sender start")
        while True:
            r=channel_send.get()
            sn,data,isright,source,destination=get_data_from_frame(r)
            if source=='A':
                A_sender_recv.put(sn)
            if source=='B':
                B_sender_recv.put(sn)

class receiver:
    def __init__(self,q:Queue) -> None:
        self.count=0
        self.process=Thread(target=self.receive_and_send,args=(q,))
    def receive_and_send(self,q):
        print("receiver start")
        while True:
            r=q.get()
            sn,data,isright,source,destination=get_data_from_frame(r)
            self.count+=1
            if isright and random.random()<probablity_of_success:
                channel_send.put(r)
            print(source,"to",destination,':',self.count)

if __name__=='__main__':
    datalist=["10001111",
    "1000101010",
    "10001010101",
    "1001010101100",
    "100101010101",
    "10100101",
    "10101011001",
    "100101001",
    "100101001",
    "11011101",
    '101001001',
    '101001010',
    '10100101010',
    '10011011',
    '00110',
    '10001',
    '1001010',
    '101011',
    '1100101111',
    '1010100101',
    '101010101001',
    '100101010010',
    '10010100101',
    '10100101010',
    '1010100101',
    '101001001',
    '10001010101',
    '101001010',
    '1001001010',
    '10100101010',
    '10101010100',
    '100010100101',
    '101001001010',
    '1000101001010',
    '101010101010',
    '1010001010001',
    '0010101010',
    '100001001001',
    '0001010100',
    '00101001010101',
    '0101010101010',
    '10010101010',
    "1000101010",
    "10001010101",
    "1001010101100",
    "100101010101",
    "10100101",
    "10101011001",
    "100101001",
    "100101001",
    "11011101",
    '101001001',
    '101001010',
    '10100101010',
    '10011011',
    '00110',
    '10001',
    '1001010',
    '101011',
    '1100101111',
    '1010100101',
    '101010101001',
    '100101010010',
    '10010100101',
    '10100101010',
    '1010100101',
    '101001001',
    '10001010101',
    '101001010',
    '1001001010',
    '10100101010',
    '10101010100',
    '100010100101',
    '101001001010',
    '1000101001010',
    '101010101010',
    '1010001010001',
    '0010101010',
    '100001001001',
    '0001010100',
    '00101001010101',
    '100101010010',
    '10010100101',
    '10100101010',
    '1010100101',
    '101001001',
    '10001010101',
    '101001010',
    '1001001010',
    '10100101010',
    '10101010100',
    '100010100101',
    '101001001010',
    '1000101001010',
    '101010101010',
    '1010001010001',
    '0010101010',
    '100001001001',
    '0001010100',
    '00101001010101']
    s1=sender(datalist,A_sender_recv,'C','A')
    s2=sender(datalist,B_sender_recv,'D','B')
    c=channel([s1,s2])
    C=receiver(C_receiver)
    D=receiver(D_receiver)
    s1.sender_send.start()
    s2.sender_send.start()
    s1.sender_receive.start()
    s2.sender_receive.start()
    c.take_from_receiver_send_to_sender.start()
    c.take_from_sender_send_to_receiver.start()
    C.process.start()
    D.process.start()
    s1.sender_send.join()
    s2.sender_send.join()
    s1.sender_receive.join()
    s2.sender_receive.join()
    c.take_from_receiver_send_to_sender.join()
    c.take_from_sender_send_to_receiver.join()
    C.process.join()
    D.process.join()
