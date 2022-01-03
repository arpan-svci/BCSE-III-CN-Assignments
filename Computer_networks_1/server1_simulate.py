import socket
from crc import *
from error import *
from lrc import *
from vrc import *
from checksum import *
generator='10011'    #input the genertor by which error correction occur  
length=56
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
server_socket.bind(('localhost',80));
server_socket.listen(1);
k="Y";
while k=="Y":
    Error_crc=0
    Error_vrc=0
    Error_checksum=0
    Error_lrc=0
    print("server waiting for connection");
    clint_socket,adder=server_socket.accept();
    print("clint connected from:",adder);
    test=0
    while test<5000:
        test+=1
        data=clint_socket.recv(1024).decode(); #data from clint
        if not data or data=='end':
            break;
        try:
            if data[0]=='0' or data[0]=='1':
                codeword=[]
                flag=0
                for i in range(0,len(data)):
                    if(data[i]=='*'):
                        codeword.append(data[flag:i])
                        flag=i+1   
                crc=codeword[0]
                lrc=codeword[1]
                vrc=codeword[2]
                checksum=codeword[3]
                state_crc=crc_decoding(crc,length,generator)
                if(state_crc=='error'):
                    Error_crc+=1
                state_lrc=lrc_decoding(lrc,length)
                if(state_lrc=='error'):
                    Error_lrc+=1
                state_vrc=vrc_decoding(vrc,length)
                if(state_vrc=='error'):
                    Error_vrc+=1
                state_checksum=checksum_decoding(checksum,length)
                if(state_checksum=='error'):
                    Error_checksum+=1
                sending_data='crc={},lrc={},vrc={},checksum={}'.format(state_crc,state_lrc,state_vrc,state_checksum)
                print("crc_error=",Error_crc,"lrc_error=",Error_lrc,"vrc_error=",Error_vrc,'checksum_error=',Error_checksum)
            else:
                sending_data=input();   
            clint_socket.send(bytes(sending_data,'utf-8')); #sending data by server 
            if sending_data=="end":
                break;
        except:
            print("exited by the user");
    clint_socket.close();
    k=input("do you want to continue(Y/N):");
server_socket.close();