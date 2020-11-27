import os
import fbrm_dbms
import glob
import ConfigParser
import datetime
class rman_comp():
    def __init__(self,sid):
        self.db=fbrm_dbms.fbrm_db()
        self.cfg = self.get_cfg()
        self.now = datetime.datetime.now()
        self.log_dir = self.get_log_dir()
        self.sid=sid


    def get_log_dir(self):
        td = self.now.strftime('%Y%m%d')
        fbrm_path = self.cfg.get('common', 'fbrm_path')
        log_dir = os.path.join(fbrm_path, 'data', 'FBRM_ORA_LOG')
        return log_dir
    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfg_file = os.path.join('config','config.cfg')
        cfg.read(cfg_file)
        return cfg

    def get_master_rman_job(self):
        to_day= self.now.strftime('%Y-%m-%d')
        query = """
        select 
            hostname,db_name,start_time,end_time,output_device_type,status,input_type 
            from fbrm.master_rman_backup_list 
            where start_time like '{DATE}%' and db_name = '{SID}'
            order by start_time desc
        """.format(DATE=to_day,SID=self.sid)
        rman_job_list=self.db.get_row(query)
        for rman_job in rman_job_list:
            print rman_job
        return rman_job_list
    def get_history(self):
        history_file='UPGR_UPGR_Backup_history.txt'

        with open(os.path.join(self.log_dir,history_file)) as f:
            lineset = f.readlines()
        return lineset

    def get_start_time(self,start_time):
        lineset = self.get_history()

        for line in lineset:
            if start_time in line:
                print line

    def get_log_list(self):
        td=self.now.strftime('%Y%m%d')
        log_list=glob.glob(os.path.join(self.log_dir,'*{DB_NAME}*{DATE}*.log'.format(DB_NAME=self.sid,DATE=td)))
        return log_list

    def main(self):



        rman_job_list=self.get_master_rman_job()
        for rman_job in rman_job_list:
            start_time=rman_job[2]
            print start_time
            self.get_start_time(start_time)
        log_list=self.get_log_list()
        for log_file in log_list:
            print log_file
            with open(log_file) as f:
                lineset = f.read()
            print lineset

if __name__=='__main__':
    rman_comp('UPGR').main()