from math import log2,ceil
from multiprocessing import Pipe

class node:

    def __init__(self, senderNo, code):
        self.senderNo = senderNo
        self.code = code
        print("Station {} is created with code {}".format(senderNo,code))
        self.data = 0

    def assignData(self, data):
        self.data = data
        
    

def createStations(n):

    print("Generating walsh table....................\n\n")

    walshTable=[1]

    count = 2
    prevCount = 1
    power = 2**(ceil(log2(n)))

    print(walshTable,end='\n\n')

    while count <= power:

        temp = walshTable
        walshTable = [[None]*count for _ in range(count)]

        for i in range(count):

            for j in range(count):

                if i >= count/2 and j >= count/2:
                    if count>2:
                        walshTable[i][j] = (-1)*temp[i%prevCount][j%prevCount]
                    else:
                        walshTable[i][j] = (-1)*temp[0]
                else:
                    if count>2:
                        walshTable[i][j] = temp[i%prevCount][j%prevCount]
                    else:
                        walshTable[i][j] = temp[0]

        prevCount = count
        count*=2

        for i in range(len(walshTable)):
            print(walshTable[i])
        print()

        

    stations = []

    if n == 1:
        Node = node(0,walshTable)
        stations.append(Node)
        return stations

    for i in range(n):

        Node = node(i,walshTable[i])
        stations.append(Node)

    return stations

def assignData(n):

    for _ in range(n):

        idx = int(input("Enter the station number: "))
        data = int(input("Assign data bit (0 or 1) to the station number {}. Enter 0 or 1: ".format(idx)))
        
        if data == 1:
            stations[idx].assignData(1)
        if data == 0:
            stations[idx].assignData(-1)

def send(conn):

    global stations

    n = int(input("How many stations will send: "))

    assignData(n)

    codeLength = len(stations[0].code)

    data = [0]*codeLength

    for i in range(codeLength):

        for j in range(len(stations)):

            station = stations[j]

            data[i] += station.code[i]*station.data

    conn.send(data)

    for i in range(len(stations)):
        stations[i].assignData(0)

def receive(conn):

    data = conn.recv()

    m = len(stations[0].code)

    for i in range(len(stations)):

        station = stations[i]

        code = station.code

        sum = 0

        for j in range(m):
            sum += code[j]*data[j]

        bit = sum/m

        if bit == 1:
            ans = 1
        elif bit == -1:
            ans = 0
        else:
            ans = None

        if ans != None:
            print("Station {} sent {}".format(i,ans))
        else:
            print("Station {} sent nothing".format(i))




n = int(input("Enter the number of stations: "))

global stations

stations = createStations(n)

head,tail = Pipe()

channelSize = 0

while True:

    print("\n1. Send")
    print("2. Receive")
    print("3. Exit")

    c = int(input("Enter choice number: "))

    if c == 1:
        send(head)
        channelSize += 1
    elif c == 2:
        if channelSize == 0:
            print(print("No station sent any data"))
            continue
        receive(tail)
        channelSize -= 1
    else:
        break       