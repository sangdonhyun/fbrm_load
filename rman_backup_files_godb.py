import os
import glob
import sys
import fbrm_dbms
import datetime
import ConfigParser
import zipfile
import table_create
import time


class rman_backupfiles():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.db = fbrm_dbms.fbrm_db()
        self.today = datetime.datetime.now()
    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def now_rman_list(self):
        t_day = self.today.strftime('%Y-%m-%d')
        y_datetime=self.today - datetime.timedelta(days=1)


        y_day = y_datetime.strftime('%Y-%m-%d')

        query = "select  u_id,hostname,db_name,session_key,session_recid,session_stamp,start_date,start_time,input_type,db_key,output_bytes,status from live.live_rman_catalog where start_date in ('{}','{}') order by start_time desc".format(t_day,y_day)
        query = "select  u_id,hostname,db_name,session_key,session_recid,session_stamp,start_date,start_time,input_type,db_key,output_bytes,status from live.live_rman_catalog where db_name = 'GODB' order by start_time desc"
        rman_list = self.db.get_row(query)
        return rman_list





    def main(self):
        fbrm_home = self.cfg.get('common','fbrm_path')
        log_path=os.path.join(fbrm_home,'data','FBRM_ORA_LOG')

        rman_list= self.now_rman_list()
        print rman_list
        for rman_backup in rman_list:
            u_id = rman_backup [0]
            hostname = rman_backup[1]
            db_name = rman_backup[2]
            session_key = rman_backup[3]
            session_recid = rman_backup[4]
            session_stamp = rman_backup[5]
            start_date = rman_backup[6]
            start_time = rman_backup[7]
            input_type = rman_backup[8]
            db_key = rman_backup[9]
            output_bytes = rman_backup[10]
            status = rman_backup[11]
            # print db_name,input_type,start_time
            sid = 'godb1'
            query = "select count(*) from live.live_ora_tablespace where instance_name = '{}'".format(sid)

            # print query
            db_file_count=int(self.db.get_row(query)[0][0])


            # print db_file_count
            # print input_type
            date_ch = '%Y_%m%d_%H'
            day_char=datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S').strftime(date_ch)

            print day_char
            # print day_char
            if input_type == 'ARCHIVELOG':
                log_set= os.path.join(log_path,'*{}_{}*Archivelog*{}*'.format(hostname,db_name,day_char))
            else:
                log_set = os.path.join(log_path, '*{}_{}*Level*{}*'.format(hostname,db_name,day_char))
            dict_list=[]
            update_list=[]
            print log_set
            log_files=glob.glob(log_set)
            print log_files
            progress_rate=''
            backup_label=''
            for log_file in log_files:
                if os.path.isfile(log_file):
                    level= os.path.basename(log_file).split('_')[-4]
                    if 'level1' in log_file.lower():
                        level ='Level1'
                    if 'level0' in log_file.lower():
                        level ='Level0'
                    if 'archive' in log_file.lower():
                        level ='Archivelog'
                    # print level,input_type
                    backup_cnt = 0
                    print 'level :',level
                    with open(log_file) as f:
                        tmpset = f.read()
                        lineset = tmpset.splitlines()
                    if level == 'Archivelog':
                        backup_label = 'ARCHIVE LOG'
                        for line in lineset:
                            if 'archived log file name' in line:
                                backup_cnt = backup_cnt + 1
                            progress_rate = backup_cnt
                    elif level == 'Level1':

                        if status not in ['FAILED' , 'COMPLETED WITH ERRORS'] :
                            if output_bytes == 0:
                                backup_label = 'DB INCL MERGY'
                            else:
                                backup_label = 'DB INCL LEVLE1'
                        else :
                            backup_label = status

                        for line in lineset:
                            if 'finished piece' in line:
                                print line
                                backup_cnt = backup_cnt +1
                        print 'backup_cnt :',backup_cnt
                        if backup_cnt > db_file_count:
                            backup_cnt = db_file_count
                        progress_rate = int((float(backup_cnt)/float(db_file_count))*100)

                        print 'progress_rate',progress_rate

                    elif level == 'Level0' :
                        backup_label = 'DB INCL LEVLEL0'
                        for line in lineset:
                            if 'datafile copy complete' in line:
                                backup_cnt = backup_cnt + 1
                        if backup_cnt > db_file_count:
                            backup_cnt = db_file_count
                        progress_rate = int((float(backup_cnt)/float(db_file_count))*100)
                    else:
                        level = 'unkown'
                    # print 'backup_cnt :',level,backup_cnt,progress_rate

                    dict = {}
                    dict['db_key'] = db_key
                    dict['session_key'] = session_key
                    dict['session_recid'] = session_recid
                    dict['session_stamp'] = session_stamp
                    dict['log_progress_rate'] = progress_rate
                    dict['log_backup_level'] = level
                    dict['log_backup_files'] = backup_cnt
                    dict['collect_time'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
                    dict['backup_label'] = backup_label
                    # dict['rman_log'] = tmpset
                    dict_list.append(dict)


                    query = "update ref.ref_rman_catalog set rman_log='{}' where db_key = '{}' and session_key='{}' and session_recid='{}' and session_stamp = '{}'".format(tmpset,db_key,session_key,session_recid,session_stamp)
                    update_list.append(query)
                    # if dict['status'] not in ['COMPLETED','RUNNING'] :


            db_name = 'ref.ref_rman_catalog'
            self.db.dbInsertList(dict_list,db_name)
            for query in update_list:
                self.db.queryExec(query)






if __name__=='__main__':
    rman_backupfiles().main()