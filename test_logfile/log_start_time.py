import os
import glob
import datetime

class log_start():
    def __init__(self):
        pass

    def get_start_time(self,f):
        start_time = None
        with open(f) as f:
            lineset = f.readlines()[:20]
        for line in lineset:
            if 'Production on' in line:
                start_time = line.split('Production on')[-1].strip()
        if not start_time == None:
            start_time = self.conv_date(start_time)
        return start_time


    def conv_date(self,d):

        start_time = datetime.datetime.strptime(d, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')

        return start_time

    def main(self):



        flist=glob.glob('E:\\Fleta\\data\\FBRM_ORA_LOG\\*')
        for f in flist:
            print f,self.get_start_time(f)

if __name__=='__main__':
    log_start().main()