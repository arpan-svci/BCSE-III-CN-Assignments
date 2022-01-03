from P_Persistent import Node
import threading
import queue
import time

PREAMBLE = "10101010" * 7
SFD = "10101011"


class Resource:
    def __init__(self, size):
        self.lock = threading.Lock()
        self.size = size
        self.channel = [(0, 0, 0, 0)] * self.size
        self.table = {}
        self.sender_count = 0
        self.q = queue.Queue()
        self.slider_thread = threading.Thread(target=self.slide_control)
        self.receive_event = threading.Event()
        self.receive_event.set()
        self.slider_thread.start()

    def slide(self):
        # print("sliding")
        with self.lock:
            n = self.q.qsize()
            while n > 0:
                i = self.q.get()
                # self.q.task_done()
                if i - 1 >= 0:
                    # check if empty
                    if self.channel[i - 1][2] == 0:
                        self.channel[i - 1] = self.channel[i]
                        self.q.put(i - 1)
                    elif self.channel[i - 1][2] != self.channel[i][2]:
                        # collision occurred
                        # print("..............collision...............")
                        self.table[self.channel[i][2]].resend_flag = True
                        self.table[self.channel[i][2]].num_collision += 1
                        self.table[self.channel[i - 1][2]].resend_flag = True
                        self.table[self.channel[i - 1][2]].num_collision += 1
                        self.channel = [(0, 0, 0, 0)] * self.size
                        self.q = queue.Queue()
                        print("collision occur")
                        print()
                        break

                if i + 1 < self.size:
                    # check if empty
                    if self.channel[i + 1][2] == 0:
                        self.q.put(i + 1)
                        self.channel[i + 1] = self.channel[i]
                    elif self.channel[i + 1][2] != self.channel[i][2]:
                        # collision occurred
                        # print("..............collision...............")
                        self.table[self.channel[i][2]].resend_flag = True
                        self.table[self.channel[i][2]].num_collision += 1
                        self.table[self.channel[i + 1][2]].resend_flag = True
                        self.table[self.channel[i + 1][2]].num_collision += 1
                        self.channel = [(0, 0, 0, 0)] * self.size
                        self.q = queue.Queue()
                        print("collision occur")
                        print()
                        break

                n = n - 1

            # print(self.channel)

    def slide_control(self):
        time.sleep(4)
        time_taken = time.time()
        while self.sender_count > 0:
            self.slide()
            time.sleep(0.3)
        else:
            self.receive_event.clear()
            time_taken = time.time() - time_taken
            print("Channel time: ", time_taken)
        for idx, val in self.table.items():
            if val.is_sender:
                print(f"Sender {val.location} takes ", val.time_taken)
                print(f"Sender {val.location} makes ", val.num_collision, "collisions")

    def put_packet(self, packet: tuple):
        print("packet sent by ", packet[2])
        print()
        with self.lock:
            index = packet[2]
            self.q.put(index)
            self.channel[index] = packet
            # print(self.channel)

    def add_to_table(self, node: Node):
        self.table[node.location] = node
        if node.is_sender:
            self.sender_count += 1
            print(self.sender_count, " sender nodes")

    def reset(self, send):
        self.channel = [(0, 0, 0, 0)] * self.size
        self.q = queue.Queue()
        self.table[send].resend_flag = False
