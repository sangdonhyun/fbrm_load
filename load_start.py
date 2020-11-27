
import ora_backup_files
import session_longops_load
import rman_load
import time
import datetime
import fs_load
import daily_load
import ora_backup_files
import rman_backup_files
import logging
import threshold


def batch_load():

    ora_backup_files.fbrm_rman().main()
    session_longops_load.fbrm_rman().main()
    rman_load.fbrm_rman().main()
    rman_backup_files.rman_backupfiles().main()
    threshold.threshold().main()



def main():
    cnt = 1
    while True:
        try:
            batch_load()
        except:
            pass
        print '-' * 50
        print 'count :', cnt
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if cnt % 60 == 0:
            try:
                fs_load.fs_load().main()
            except:
                pass
        cnt=cnt+1


        print 'sleep 60'
        time.sleep(60)


if __name__=='__main__':
    main()



