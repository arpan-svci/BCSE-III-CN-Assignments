from error import *
def bitexor(c1,c2):
    if c1==c2:
        return '0'
    else:
        return '1'

def xor(s1,s2):
    s=''
    for i in range (0,len(s1)):
        s=s+bitexor(s1[i],s2[i])
    return s;

def datawords(data,generator):
    dataword=data;
    for i in range (0,len(generator)):
        dataword=dataword+'0'
    return dataword

def codewords(datawords,generator):
    zero=''
    generator_lenth=len(generator)
    length=len(datawords)
    zero='0'*generator_lenth;
    div=datawords[0:generator_lenth]
    curser=generator_lenth
    while curser<=length:
        if div[0]=='0':
            remain=xor(zero,div)
        else:
            remain=xor(generator,div)
        if curser==length:
            break
        div=remain[1:generator_lenth]+datawords[curser]
        curser+=1
    codeword=datawords[0:length-generator_lenth]+remain
    return codeword
def crc_encoding(data,generator):
    encoding_data=''
    for i in data:
        encoding_data+=codewords(datawords(i,generator),generator)
    return encoding_data

def crc_decoding(codeword,length,generator):
    dataword=''
    length_code=length+len(generator)
    i=0
    while i<len(codeword):
        if(len(codeword)-i<length_code):
            code=codeword[i:len(codeword)]
            dataword+=codewords(code,generator)
            break
        code=codeword[i:i+length_code]
        dataword+=codewords(code,generator)
        i+=length_code
    i=0
    state="correct"
    while i<len(dataword):
        if(len(dataword)-i)<length_code:
            if(dataword[len(dataword)-len(generator):len(dataword)]!='0'*len(generator)):
                state='error'
            break
        if dataword[i+length:i+length_code]!='0'*len(generator):
            state='error'
            break
        i=i+length+len(generator)
    return state
def insert_error_crc(codeword,length,generator,err):
    l=list(codeword)
    lenth_generator=len(generator)
    cap=(len(codeword)/(length+lenth_generator))*length
    for i in err:
        pos=i%length+(int(i/length))*(length+lenth_generator)
        if l[pos]=='0':
            l[pos]='1'
        else:
            l[pos]='0'
    return ''.join(l)
