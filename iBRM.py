import os

class ibrm():
    def __init__(self):
        pass



    def head(self):
        print '#'*50
        print '#' * 50
        print '#     '+'iBRM Home module version 1'.ljust(43)+'#'
        print '#' * 50
        print '#' * 50


    def process_check(self):
        cmd = 'tasklist | findstr "python.exe"'
        ret=os.popen(cmd).read()
        print ret

    def process_start(self):
        cmd = 'python daily_load.py'
        os.popen()

    def process_stop(self):
        cmd = 'taskkill /F /IM python.exe'
        os.popen(cmd).read()
        print self.process_check()
    def main(self):

        while True:
            self.head()
            print 'Menu >'
            print '1) process stop'
            print '2) process start'
            print '3) END'
            num = raw_input('>>')
            if num.strip() == '1':
                self.process_stop()
            elif num.strip() == '2':
                self.process_start()
            else:

                break




if __name__=='__main__':
    ibrm().main()