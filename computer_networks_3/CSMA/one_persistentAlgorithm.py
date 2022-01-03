import  time

#is status of channel is busy then continue sensing, else allow transmission
def sensing(status,Tp):
    if status == "BUSY":
        print("Channel is Busy")
        time.sleep(2 * (Tp))
        sensing(status,Tp)
    else:
        return True