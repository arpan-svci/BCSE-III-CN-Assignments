import math
import numpy as np
import copy


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


class Channel:
    def __init__(self, num_nodes):
        self.msgs = []
        self.walsh_table = np.ones((1, 1), dtype="int32")
        self.encoded_msg = []
        self.num_nodes = num_nodes
        self.create_table()

    def create_table(self):
        dims = int(math.pow(2, math.ceil(math.log(self.num_nodes, 2))))

        while dims > self.walsh_table.shape[0]:
            w3 = self.walsh_table
            w3 = complement(w3)
            r1 = np.concatenate((self.walsh_table, self.walsh_table), axis=1)
            r2 = np.concatenate((self.walsh_table, w3), axis=1)
            self.walsh_table = np.concatenate((r1, r2), axis=0)
        # print(self.walsh_table)

    def encode(self):
        # print(self.msgs)
        self.encoded_msg = np.array([sum(i) for i in zip(*self.msgs)], dtype="int32")
        self.msgs = []

    def push_msg(self, msg):
        self.msgs.append(copy.deepcopy(msg))
