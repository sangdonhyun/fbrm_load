import fs_load
import srm_load
import time
import datetime

def main():
    fs_load.fs_load().main()
    srm_load.srm_load().main()



if __name__=='__main__':
    while True:
        main()
        time.sleep(30)
