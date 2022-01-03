import random
import threading
import time

PREAMBLE = "10101010" * 7
SFD = "10101011"


class Node:
    def __init__(self, location, resource, is_sender, receiver, data=""):
        # attributes
        self.location = location
        self.resend_flag = True
        self.frame_size = 8
        self.current_pointer = 0
        self.back_off = 0
        self.P = 0.7
        self.is_sender = is_sender
        # read file into string
        self.data = data
        self.resource = resource
        self.num_collision = 0
        self.sending_thread = threading.Thread(target=self.send_data)
        self.receiving_thread = threading.Thread(target=self.receive_data)
        self.recv_loc = receiver
        self.time_taken = 0

        self.resource.add_to_table(self)
        self.receive_event = threading.Event()

        if is_sender:
            self.sending_thread.start()
        else:
            self.receiving_thread.start()

    def send_data(self):
        print("sender started")
        s = len(self.data)
        self.time_taken = time.time()
        while self.current_pointer <= s - self.frame_size:
            packet = self.data[self.current_pointer:self.current_pointer + self.frame_size]
            if len(packet) < self.frame_size:
                packet = packet + " " * (self.frame_size - len(packet))
            print("data sent :",packet)
            # tuple (1, data, senders' loc, receiver's loc, SFD, Preamble)
            while self.resend_flag:
                if self.resource.channel[self.location][0] == 0:
                    frame = (1, packet, self.location, self.recv_loc, SFD, PREAMBLE)
                    if random.random() > self.P:
                        time.sleep((random.randint(0, self.back_off)) * 2)
                    else:
                        self.resource.put_packet(frame)
                        self.resend_flag = True
                        self.back_off += 1
                else:
                    time.sleep(0.1)
                    # time.sleep(random.random()*2)
            # if self.resource.channel[self.location][0]==0:
            # frame=(1, packet, self.location, self.recv_loc)
            # self.resource.put_packet(frame)
            self.current_pointer += self.frame_size
            self.resend_flag = True
            self.back_off = 0
            # else:
            #     time.sleep(0.2)

            time.sleep(0.1)
        self.time_taken = time.time() - self.time_taken
        self.resource.sender_count -= 1

    def receive_data(self):
        print("receiver started")
        message = ""
        while self.resource.receive_event.is_set():
            # if self.receive_event.is_set():
            recv = self.resource.channel[self.location][3]
            send = self.resource.channel[self.location][2]
            if recv == self.location:
                with self.resource.lock:
                    print("receiver ", self.location, " receives data", self.resource.channel[self.location][1], " from ",
                          send)
                    print()
                    message += self.resource.channel[self.location][1]
                    self.resource.reset(send)

            time.sleep(0.1)
        else:
            print("end")
            print("data :",message)
            # self.receive_event.clear()
