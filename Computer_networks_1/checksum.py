from error import *
def complement(str):
    l=list(str)
    for i in range(0,len(l)):
        if l[i]=='0':
            l[i]='1'
        else:
            l[i]='0'
    return ''.join(l)

def checksum_codeword(data,length):
    sum=0
    checksum=''
    dataword=''
    for i in data:
        dataword+=i
        sum+=int(i,2)
    sum=bin(sum)[2:]
    if(len(sum)<length):
        sum='0'*(length-len(sum))+sum
        checksum=complement(sum)
    elif(len(sum)==length):
        checksum=complement(sum)
    else:
        x=len(sum)-length
        sum=bin(int(sum[0:x],2)+int(sum[x:],2))[2:]
        if(len(sum)<length):
            sum='0'*(length-len(sum))+sum
        checksum=complement(sum)
    return dataword+checksum

def checksum_decoding(data,length):
    i=0
    sum=0
    red=data[len(data)-length:len(data)]
    data=data[0:len(data)-length]
    while i<len(data):
        if(len(data)-i<=length):
            str=data[i:len(data)]
            sum+=int(str,2)
            sum+=int(red,2)
            break
        str=data[i:i+length]
        sum+=int(str,2)
        i+=length
    sum=bin(sum)[2:]
    if(len(sum)>length):
        k=len(sum)-length
        sum=int(sum[0:k],2)+int(sum[k:],2)
        sum=bin(sum)[2:]
    if(sum=='1'*length):
        return 'correct'
    else:
        return 'error'

# dataword='11001101'
# data=data_packeting(dataword,8)
# print(data)
# code=checksum_codeword(data,8)
# print(code)
# # code=inject_error(code,[2,4])
# # print(code)
# print(checksum_decoding(code,4))