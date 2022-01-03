import socket
import time
IP='localhost'
PORT=80
ADDR=(IP,PORT)
file_name="my_file.txt"
def main():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    file=open("client_data/"+file_name ,"r") #read particular file we need to send
    data=file.read()  
    time.sleep(1)           
    client.send(file_name.encode('utf-8')) #send name of the file to server
    print("[CLIENT] : filename is sent")
    time.sleep(1) 
    msg=client.recv(1024).decode('utf-8')
    print(msg)
    time.sleep(1) 
    client.send(data.encode('utf-8'))
    print("[CLIENT] : file data sent")
    msg=client.recv(1024).decode('utf-8');
    time.sleep(1) 
    print(msg)
    time.sleep(2)
    client.close()
        
if __name__=="__main__":
    main()