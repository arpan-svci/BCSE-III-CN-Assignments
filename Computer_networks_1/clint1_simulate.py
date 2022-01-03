from os import times
import socket;
from crc import *
from error import *
from lrc import *
from vrc import *
from checksum import *
import random
length=56
total_error=0
generator='10011'     #input the generator
clint_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
clint_socket.connect(('localhost',80));
try:
    print("send 'End' to terminate the connection");
    test=0
    while test<5000:
        test+=1
        data="100101101001010010110110110111010110101101011011010101101010110111001100111001110001110011100011001110001110011110011100110011011101100110011000111011000000001111111100110101100100110011110011001110001101"           #enter the data want to send
        if data[0]=='1'or data[0]=='0':
            len_dataword=len(data)
            data=data_packeting(data,length)
            crc_codeword=crc_encoding(data,generator)
            len_crc=len(crc_codeword)
            checksum_codewords=checksum_codeword(data,length)
            len_checksum=len(checksum_codewords)
            lrc_codeword=lrc_encoding(data)
            len_lrc=len(lrc_codeword)
            vrc_codewords=vrc_codeword(data)
            len_vrc=len(vrc_codewords)
            # s=input("do you want to insert error(yes/no):")
            s='yes'
            if s=='yes':
                total_error+=1
                # k=input("do you want to insert random error(yes/no)")
                k='yes'
                err=[]
                # no=int(input('enter number of error less than {}:'.format(len_dataword)))
                no=2   #number of error want to inject
                if(k=="no"):
                    for i in range(0,no):
                        err.append(int(input("enter error less tha {}:".format(len_dataword))))
                else:
                    for i in range (0,no):
                        err.append(random.randint(0,len_dataword-1))
                err=set(err)
                print(err)
                err=list(err)
                crc_codeword=insert_error_crc(crc_codeword,length,generator,err)
                lrc_codeword=inject_error(lrc_codeword,err)
                vrc_codewords=insert_error_vrc(vrc_codewords,length,err)
                checksum_codewords=inject_error(checksum_codewords,err)
            codeword=crc_codeword+'*'+lrc_codeword+'*'+vrc_codewords+'*'+checksum_codewords+'*'
            clint_socket.send(bytes(codeword,'utf-8'));
        else:
            clint_socket.send(bytes(data,'utf-8'));
        if data=='end':
            break;
        data=clint_socket.recv(1024).decode();  #response recive from server
        print("total no. of packets with error:",total_error)
except KeyboardInterrupt:
    print("exited by user");
clint_socket.close();