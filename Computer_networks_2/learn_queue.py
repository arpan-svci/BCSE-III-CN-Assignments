from multiprocessing import *
import time
def squre_list(list,q):
    for num in list:
        time.sleep(0.01)
        q.put(num*num)
def print_list(q):
    while not q.empty():
        print(q.get())
def cube_list(list,q):
    for num in list:
        time.sleep(0.01)
        q.put(num*num*num)
q=Queue()
p1=Process(target=squre_list,args=(range(25),q))
p2=Process(target=print_list,args=(q,))
p3=Process(target=cube_list,args=(range(25),q))
if __name__=='__main__':
    p1.start()
    p3.start()
    p2.start()
    p1.join()
    p3.join()
    p2.join()
    