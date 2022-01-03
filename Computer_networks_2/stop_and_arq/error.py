def inject_error(str,pos):
    l=list(str)
    length=len(str)
    for i in pos:
        k=int(i%length)
        if l[k]=='1':
            l[k]='0'
        else:
            l[k]='1'
    str=''.join(l)
    return str

def data_packeting(data,length):
    packets=[]
    i=0;
    while i<len(data):
        if(len(data)<length):
            packets.append(data[0:len(data)])
            break
        if len(data)-i<length:
            k=len(data)-i
            packets.append(data[i:len(data)])
            return packets
        packets.append(data[i:i+length])
        i=i+length
    return packets