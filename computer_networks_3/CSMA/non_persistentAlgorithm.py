import random
import time

#random wait time is generated under propagation time
def Random_wait(Tp):
    time.sleep(random.choice(range(Tp)))
#sensing the channel
def sensing(status, Tp):
    if status=="BUSY":
        print("Channel is Busy")
        Random_wait(Tp)
    else:
        return True