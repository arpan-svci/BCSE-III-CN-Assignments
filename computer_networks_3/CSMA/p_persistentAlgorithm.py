import random
import time

k=[0]
kmax=15
collisionNo=0

#random wait under propagation time
def Random_wait(Tp):
    print("Wait random period of time")
    time.sleep(random.choice(range(Tp)))

#backoff algorithm
def BackOff(Tp):
    global collisionNo
    collisionNo+= 1
    while collisionNo<=kmax:
        k.append(collisionNo)
        print("wait according to binary exponential backoff")
        time.sleep(random.choice(k)*2*Tp)

#sensing the channel
def sensing(status,Tp,probability):
    #if channel is busy then continue sensing
    if status=="BUSY":
        print("Channel is Busy")
        sensing(status,Tp,probability)
    #whenever channel is free
    while status=="FREE":
        print("Channel is Free")
        R = random.choice(range(1))
        if R <= probability:
            return True#allow transmission permission
        else:
            #wait one slot
            print("Wait one slot")
            time.sleep(2*Tp)
            #channel is busy then use backoff algorithm to wait
            if status == "BUSY":
                print("Collision Occured")
                BackOff(Tp)
