from error import *
def vrc_codeword(data):
    codeword=''
    for i in data:
        i=list(i)
        one=0
        for j in range(0,len(i)):
            if(i[j]=='1'):
                one+=1
        if(one%2==0):
            i.append('0')
        else:
            i.append('1')
        codeword+=''.join(i)
    return codeword

def vrc_decoding(codeword,length):
    i=0
    status='correct'
    while(i<len(codeword)):
        one=0
        if(len(codeword)-i)<length:
            code=codeword[i:len(codeword)]
        else:
            code=codeword[i:i+length+1]
        for j in range(0,len(code)):
            if(code[j]=='1'):
                one+=1
        if(one%2!=0):
            status='error'
            break
        i=i+length+1
    return status
def insert_error_vrc(codeword,length,error):
    codeword=list(codeword)
    for i in error:
        pos=i%length+(int(i/length))*(length+1)
        if(codeword[pos]=='1'):
            codeword[pos]='0'
        else:
            codeword[pos]='1'
    return ''.join(codeword)

# data=data_packeting('11010110101',4)
# print(data)
# codeword=vrc_codeword(data)
# print(codeword)
# codeword=insert_error_vrc(codeword,4,[2,5])
# print(codeword)
# status=vrc_decoding(codeword,4)
# print(status)