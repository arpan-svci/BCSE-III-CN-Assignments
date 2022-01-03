import math
import copy
import numpy as np
from NODE import Node
from CHANNEL import Channel


def complement(wt):
    wt2 = copy.deepcopy(wt)
    n = wt.shape[0]
    for i in range(n):
        for j in range(n):
            if wt2[i][j] == 1:
                wt2[i][j] = -1
            else:
                wt2[i][j] = 1
    return wt2


if __name__ == "__main__":
    msg1 = [1, -1, 1, 1, 0, -1, -1, -1, 1]
    msg2 = [1, 1, 0, -1, 1, -1, 0, -1, 1]
    msg3 = [1 ,-1, 0, -1, 1, -1 , 0, 1, -1]
    channel = Channel(6)
    s1 = Node(channel, True, 0, 0, msg1)
    s2 = Node(channel, True, 1, 1, msg2)
    s3 = Node(channel, True, 2, 2, msg3)
    r1 = Node(channel, False, 3, 0)
    r2 = Node(channel, False, 4, 1)
    r3 = Node(channel, False, 5, 2)
    for i in range(len(msg1)):
        s1.send(i,0)
        s2.send(i,1)
        s3.send(i,2)
        channel.encode()
        r1.receive(3)
        r2.receive(4)
        r3.receive(5)

    print("message received :",r1.msg_r)
    print("message received :",r2.msg_r)
    print("message received :",r3.msg_r)