from os import error
from error import *
def lrc_encoding(data):
    codeword=''
    checker=[]
    number=len(data)
    length=len(data[0])
    length_last_packet=len(data[-1])
    for i in range(0,length):
        one=0
        for j in range(0,number-1):
            if(data[j][i]=='1'):
                one+=1
        if(one%2==0):
            checker.append('0')
        else:
            checker.append('1')
    j=length-1
    for i in range(length_last_packet-1,-1,-1):
        if(data[number-1][i]=='1'):
            if(checker[j]=='0'):
                checker[j]='1'
            else:
                checker[j]='0'
        j-=1
    checker=''.join(checker)
    for i in data:
        codeword+=i
    codeword+=checker
    return codeword
def lrc_decoding(codeword,length):
    data=[]
    number=0
    len_codeword=len(codeword)
    buffer=len_codeword-length
    pairity=codeword[buffer:len_codeword]
    for i in range(0,buffer,length):
        if(i<=buffer-length):
            data.append(codeword[i:i+length])
            number+=1
        else:
            data.append(('0'*(length-(buffer-i)))+codeword[i:buffer])
            number+=1
    status='correct'
    for i in range(0,length):
        one=0
        k=''
        for j in range(0,number):
            if(data[j][i]=='1'):
                one+=1
        if(one%2==0):
            k='0'
        else:
            k='1'
        if(pairity[i]!=k):
            status='error'
            break
    return status

# data=data_packeting('11010110101',4)
# print(data)
# codeword=lrc_encoding(data)
# print(codeword)
# codeword=inject_error(codeword,[])
# print(codeword)
# print(lrc_decoding(codeword,4))

