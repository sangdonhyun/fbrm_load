import fbrm_dbms
import os
import sys
import datetime
import time
import ConfigParser
class progres():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.db = fbrm_dbms.fbrm_db()
        self.today = datetime.datetime.now()

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def get_live_rman(self):
        today_char = self.today.strftime('%Y-%m-%d')
        query  = "select db_name,session_key,session_recid,session_stamp,start_date,start_time,input_type,status from live.live_rman_catalog where start_date = '{}' ".format(today_char)
        print query
        ret= self.db.get_row(query)
        for backup in ret:

            db_name = backup[0]
            backup_type = backup[6]
            backup_start_time = backup[5]
            backup_time =datetime.datetime.strptime(backup_start_time,'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d %H')
            print db_name,backup_type,backup_time
            # if backup_type == 'ARCHIVELOG':



    def main(self):
        self.get_live_rman()

if __name__=='__main__':
    progres().main()