import os
import socketClient
import time
import datetime

def curl_evnt():
    ip_list= ['192.168.0.184','192.168.0.185']




    str="""
    
    """





    for ip in ip_list:
        lineset="""curl --user root:welcome1 -k -i https://{IP}:215/api/log/v1/logs
    curl --user root:welcome1 -k -i https://{IP}:215/api/log/v1/logs/audit
    curl --user root:welcome1 -k -i https://{IP}:215/api/log/v1/logs/fault
    curl --user root:welcome1 -k -i https://{IP}:215/api/log/v1/logs/system
    curl --user root:welcome1 -k -i https://{IP}:215//api/log/v1/logs/alert""".format(IP=ip)


        fname = 'event_{IP}.txt'.format(IP=ip)
        with open(fname,'w') as fw:
            for line in lineset.splitlines():
                print line
                ret=os.popen(line).read()
                fw.write(line+'\n')
                fw.write('-'*30+'\n')
                fw.write(ret+'\n')
                fw.write('-' * 30 + '\n')

if __name__=='__main__':
    cnt = 0
    while True:
        curl_evnt()
        print datetime.datetime.now()
        cnt = cnt +1
        print 'count :'.cnt
        time.sleep(60)
