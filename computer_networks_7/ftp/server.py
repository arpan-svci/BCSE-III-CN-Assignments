import socket
import time
IP='localhost'
PORT=80
ADDR=(IP,PORT)
def main():
    print(".....................server started.....................")
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("<<<<listining>>>>")
    while True:
        conn,addr=server.accept()
        print("New connection ,",addr,"connected")
        filename=conn.recv(1024).decode("utf-8") # read the name of the file sent by the client
        time.sleep(1) 
        print("[SERVER] : filename received:",filename)
        file=open("server_data/"+filename,"w")
        conn.send("[SERVER] : filename received successfully".encode("utf-8"))
        data=conn.recv(1024).decode('utf-8')
        time.sleep(1) 
        print("[SERVER] : data received")
        file.write(data)
        conn.send("[SERVER] : data received successfully".encode('utf-8'))
        time.sleep(5)
        conn.close()
        server.close()
        break
if __name__=="__main__":
    main()