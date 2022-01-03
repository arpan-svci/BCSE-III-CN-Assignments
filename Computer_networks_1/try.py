        from crc import *
        from error import *
        from lrc import *
        from vrc import *
        from checksum import *
        data=input()           #enter the data want to send
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
            s=input("do you want to insert error(yes/no):")
            if s=='yes':
                err=[]
                no=int(input('enter number of error less than {}:'.format(len_dataword)))
                for i in range(0,no):
                    err.append(int(input("enter error less tha {}:".format(len_dataword))))
                err=set(err)
                err=list(err)
                crc_codeword=insert_error_crc(crc_codeword,length,generator,err)
                lrc_codeword=inject_error(lrc_codeword,err)
                vrc_codewords=insert_error_vrc(vrc_codewords,length,err)
                checksum_codewords=inject_error(checksum_codewords,err)
            codeword='*'+crc_codeword+'*'+lrc_codeword+'*'+vrc_codewords+'*'+checksum_codewords+'*'