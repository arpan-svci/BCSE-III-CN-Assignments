import random
import threading
import time
class Node:
    def __init__(self, location, resource, is_sender, receiver):
        #attributes
        self.location = location
        self.resend_flag = False
        self.frame_size=4
        self.current_pointer=0
        self.back_off=0
        self.is_sender = is_sender
        #read file into string
        self.data = "uwhoifgoqwyifqoiywfoiyqvfoyvqwfuu"
        self.resource = resource
        self.sending_thread = threading.Thread(target=self.send_data)
        self.receiving_thread = threading.Thread(target=self.receive_data)
        self.recv_loc = receiver

        self.resource.add_to_table(self)
        self.receive_event = threading.Event()

        if is_sender:
            self.sending_thread.start()
        else:
            self.receiving_thread.start()


    def send_data(self):
        print("sender started")
        s = len(self.data)
        while self.current_pointer<=s-self.frame_size:
            packet  = self.data[self.current_pointer:self.current_pointer+self.frame_size]
            print(packet)
# tuple (1, data, senders' loc, receiver's loc)
            while self.resend_flag:
                if self.resource.channel[self.location][0]==0:
                    frame=(1, packet, self.location, self.recv_loc)
                    time.sleep((random.randint(0,self.back_off))*0.5)
                    self.resource.put_packet(frame)
                    self.resend_flag=True
                    self.back_off+=1
                else:
                    time.sleep(0.1)
            # if self.resource.channel[self.location][0]==0:
            # frame=(1, packet, self.location, self.recv_loc)
            #self.resource.put_packet(frame)
            self.current_pointer+= self.frame_size
            self.resend_flag=True
            self.back_off=0
            # else:
            #     time.sleep(0.2)

            time.sleep(0.1)
        
        self.resource.sender_count-=1


    def receive_data(self):
        print("receiver started")
        while self.resource.receive_event.is_set():
            # if self.receive_event.is_set():
            recv = self.resource.channel[self.location][3]
            send = self.resource.channel[self.location][2]
            if recv==self.location:
                print("receiver ", self.location, " receives " ,self.resource.channel[self.location][1], " from ",send)
                self.resource.reset(send)
                
            time.sleep(0.1)
        else:
            print("end")

            # self.receive_event.clear()
