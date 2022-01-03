import numpy as np
import copy


class Node:
    def __init__(self, channel, is_sender,idx , sender_idx, message= ""):
        self.code = np.array(copy.deepcopy(channel.walsh_table[idx]), dtype="int32")
        self.channel = channel
        self.message = message
        self.name=sender_idx
        self.sender_code = np.array(channel.walsh_table[idx], dtype="int32")
        if not is_sender:
            self.sender_code = channel.walsh_table[sender_idx]
        self.msg_r = ""

    def send(self, idx,name):
        msg = self.message[idx] * self.code
        print("-------------------------------------------------------------------------")
        print(self.code, " x ", self.message[idx], " = ", msg, "  sent by ",name)
        print("-------------------------------------------------------------------------")
        print()
        self.channel.push_msg(msg)

    def receive(self,idx):
        ch =  str(int(np.dot(self.sender_code,
                                     self.channel.encoded_msg) / self.channel.num_nodes))
        print("-------------------------------------------------------------------------------------------")
        print(self.sender_code, " x ", self.channel.encoded_msg, " = ", ch, "    received by ",idx)
        print("-------------------------------------------------------------------------------------------")
        print()
        if ch == "-1":
            self.msg_r += "-1"
        elif ch == "0":
            self.msg_r += "0"
        else :
            self.msg_r += "1"
        self.msg_r+=" "
        # print(f"{self.msg_r} received")
