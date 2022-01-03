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

probablity_of_success=0.1

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
    def __init__(self,data,q,destination,source,length) -> None:
        self.destination=destination
        self.source=source
        self.event=1
        self.frame=0
        self.cansend=True
        self.sn=0
        self.sf=0
        self.naklist=[]
        self.list=list(range(length))
        self.window_size=4
        self.window=[]
        self.interval=1
        self.data=data
        self.sender_send=Thread(target=self.send,name='sender_send')
        self.sender_receive=Thread(target=self.receive,args=(q,),name="sender_receive")
    def send(self):
        print("sending start")
        time.sleep(1)
        while self.cansend:
            while self.event==0:
                pass
            if(self.event==1 and self.cansend):
                f=make_frame(self.sn,self.data[self.sn],self.source,self.destination)
                channel_recv.put(f)
                print(self.source,self.destination,self.sf,self.sn)
                self.event=0
                if(self.sn-self.sf>=self.window_size-1):
                    time.sleep(2)
                    k=len(self.naklist)-1
                    while(self.list[self.naklist[k]]==-1):
                        self.naklist.pop()
                        k=len(self.naklist)-1
                    k=self.naklist.pop()
                    f=make_frame(k,self.data[k],self.source,self.destination)
                    while(self.list[k]!=-1):
                        channel_recv.put(f)
                        t1=time.time()
                        while time.time()-t1<self.interval:
                            if(self.list[k]==-1):
                                self.sn+=1
                                break
                else:
                    t1=time.time()
                    while(time.time()-t1<self.interval):
                        if(self.list[self.sn]==-1):
                            break
                    if(self.sn<len(self.data)-1):
                        self.sn+=1
                    elif(self.sf==len(self.data)-1):
                        self.cansend=False

    def receive(self,q:Queue):
        print("recive in send start")
        while True:
            k=q.get()
            if(k[1]==False):
                if self.sf<=k[0] and k[0]<=self.sn:
                    self.naklist.insert(0,k[0])
            elif k[1]==True:
                if k[0]==self.sf:
                    self.list[k[0]]=-1
                    while(self.list[self.sf]==-1):
                        self.sf+=1
                elif self.sf<=k[0] and k[0]<=self.sn:
                    self.list[k[0]]=-1
                
class channel:
    def __init__(self,sender) -> None:
        self.list_of_sender=sender
        self.count1=0
        self.count2=0
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
                if probablity_of_success<random.random():
                    C_receiver.put(r)
            if(r[33]=='D'):
                if probablity_of_success<random.random():
                    D_receiver.put(r)
            for _ in self.list_of_sender:
                _.event=0
    def take_from_receiver_pass_to_sender(self):
        print("in receive_from_receiver_pass_to_sender start")
        while True:
            r=channel_send.get()
            if r[0]=='A':
                A_sender_recv.put([r[2],r[3]])
            if r[0]=='B':
                B_sender_recv.put([r[2],r[3]])

class receiver:
    def __init__(self,q:Queue,length:int) -> None:
        self.naksent=False
        self.ackneeded=False
        self.process=Thread(target=self.receive_and_send,args=(q,))
        self.rn=0
        self.list=list(range(length))
        self.ptr=0
    def receive_and_send(self,q):
        print("receiver start")
        while True:
            r=q.get()
            sn,data,isright,source,destination=get_data_from_frame(r)
            print(source,destination,sn)
            if not isright:
                channel_send.put([source,destination,self.rn,False])
            elif sn!=self.rn:
                self.list[sn]=-1
                channel_send.put([source,destination,sn,True])
                k=self.rn
                while(k<sn):
                    if(self.list[k]!=-1):
                        channel_send.put([source,destination,k,False])
                        print('sent nak for',k)
                    k+=1
            elif sn==self.rn:
                channel_send.put([source,destination,sn,True])
                self.rn+=1
                

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
    length=len(datalist)
    s1=sender(datalist,A_sender_recv,'C','A',length)
    s2=sender(datalist,B_sender_recv,'D','B',length)
    c=channel([s1,s2])
    C=receiver(C_receiver,length)
    D=receiver(D_receiver,length)
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