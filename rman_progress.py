'''
Created on 2020. 4. 6.

@author: user
'''
import os
import glob
import sys
import fbrm_dbms
import datetime
import ConfigParser
import zipfile
import table_create
import time
import rman_backup_files

class fbrm_rman():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.db = fbrm_dbms.fbrm_db()
        self.now = datetime.datetime.now()
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')

        # table_create.table_creat().rman_table()
        # self.check_table()


    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def get_data_file(self):
        path = self.cfg.get('common', 'fbrm_path')
        data_path = os.path.join(path, 'data')
        rman_data_path = os.path.join(path, 'data', 'FBRM_RMAN_PROGRESS')
        file_list = glob.glob(os.path.join(rman_data_path, '*'))
        return file_list

    def set_line_cols(self, line):
        cols_list = line.split(',')
        return cols_list


    def data_fead(self, hostanme, agent_ip, data_set):
        rman_cat_list = []
        print data_set

        for i in range(len(data_set)):



            line = data_set[i]
            # print line

            if ',' in line:
                col_dict = {}
                col_set = self.set_line_cols(line)
                for i in range(len(col_set)):
                    col = col_set[i]
                    col_dict[self.col_name_list[i]] = col.strip()
                    col_dict[self.col_name_list[21]] = self.to_byte(data_set[i+1].split(',')[0])
                    col_dict[self.col_name_list[22]] = self.to_byte(data_set[i + 2].split(',')[0])
                    col_dict[self.col_name_list[23]] = self.to_byte(data_set[i + 3].split(',')[0])
                    col_dict[self.col_name_list[24]] = self.to_byte(data_set[i + 4].split(',')[0])
                    col_dict['hostname'] = hostanme
                    col_dict['agent_ip'] = agent_ip
                    col_dict['fbrm_date'] = self.today
                    # col_dict['db_name'] = 'catdb'

                    if len(col_dict.keys()) == 28:
                        col_dict['input_bytes_per_sec'] = self.to_num(col_dict['input_bytes_per_sec'])
                        col_dict['collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                rman_cat_list.append(col_dict)
            #
            #
            #
            # cnt = i % 6
            # if cnt == 0:
            #     col_dict = {}
            #     col_set = self.set_line_cols(line)
            #     for i in range(len(col_set)):
            #         col = col_set[i]
            #         col_dict[self.col_name_list[i]] = col.strip()
            #
            # elif cnt == 1:
            #
            #     col_dict[self.col_name_list[21]] = self.to_byte(line.split(',')[0])
            #
            # elif cnt == 2:
            #
            #     col_dict[self.col_name_list[22]] = self.to_byte(line.split(',')[0])
            # elif cnt == 3:
            #
            #     col_dict[self.col_name_list[23]] = self.to_byte(line.split(',')[0])
            # elif cnt == 4:
            #
            #     col_dict[self.col_name_list[24]] = self.to_byte(line.split(',')[0])
            # else:
                # print 'line : ', line
                col_dict['hostname'] = hostanme
                col_dict['agent_ip'] = agent_ip
                col_dict['fbrm_date'] = self.today
                # col_dict['db_name'] = 'catdb'

                if len(col_dict.keys()) == 28:
                    col_dict['input_bytes_per_sec'] = self.to_num(col_dict['input_bytes_per_sec'])
                    col_dict['collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # print col_dict
                    # sys.exit()
                    rman_cat_list.append(col_dict)
        return rman_cat_list





    def fead(self, f):

        hostname, agent_ip = '', ''
        with open(f) as f:
            lineset = f.readlines()
        # print lineset
        db_name,start_time,end_time,session_key,session_recid,session_staamp = '','','','','',''
        for i in range(len(lineset)):
            line = lineset[i]

            if '###***DB_NAME***###' in line:
                db_name = lineset[i + 1].strip()
            if '###***START_TIME***###' in line:
                start_time = lineset[i + 1].strip()
            if '###***END_TIME***###' in line:
                end_time = lineset[i + 1].strip()
            if '###***END_TIME***###' in line:
                end_time = lineset[i + 1].strip()
            if '###***SESSION_KEY***###' in line:
                session_key = lineset[i + 1].strip()
            if '###***SESSION_STAMP***###' in line:
                session_stamp = lineset[i + 1].strip()
            if '###***RMAN_PROGRESS***###' in line:
                progress_date = lineset[i+2:]

        return db_name,start_time,end_time,session_key,session_recid,session_stamp,progress_date






    def set_event(self,ora_dict):
        """
        log_date date NOT NULL,
        check_date character varying(30) COLLATE pg_catalog."default" NOT NULL,
        check_category character varying(30) COLLATE pg_catalog."default" NOT NULL,
        event_date character varying(30) COLLATE pg_catalog."default" NOT NULL,
        serial_number character varying(200) COLLATE pg_catalog."default" NOT NULL,
        event_code character varying(50) COLLATE pg_catalog."default" NOT NULL,
        event_level character(50) COLLATE pg_catalog."default",
        q_event_level character(50) COLLATE pg_catalog."default",
        desc_summary character(1000) COLLATE pg_catalog."default",
        desc_detail character(1000) COLLATE pg_catalog."default",
        device_type character varying(10) COLLATE pg_catalog."default",
        vendor_name character varying(50) COLLATE pg_catalog."default",
        event_method character varying(30) COLLATE pg_catalog."default",
        :param ora_dict:
        :return:
        """
        event_list=[]
        event_dict ={}
        event_date = self.now.strftime('%Y-%m-%d %H:%M:%S')
        event_msg = "Oracle DB {db_name} BACKUP {status} ".format(db_name=ora_dict['db_name'],
                                                                        status=ora_dict['status'])
        event_dict['log_date'] = event_date
        event_dict['check_date'] = event_date
        event_dict['check_category'] = 'RMAN BACKUP'
        event_dict['event_date']   = ora_dict['start_time']
        event_dict['event_code'] = 'b001'
        event_dict['serial_number'] = ora_dict['db_key']
        event_dict['event_level'] = ora_dict['status']
        event_dict['device_type'] = "RMAN"
        event_dict['desc_detail'] = event_msg
        event_dict['vendor_name'] = 'Oracle'
        event_list.append(event_dict)

        query = "select count(*) from event.event_log where log_date='{}' and desc_detail ='{}'".format(event_date,event_msg)
        ret=self.db.get_row(query)[0][0]

        if ret == 0:
            db_name = 'event.event_log'
            self.db.dbInsertList(event_list, db_name)

        query = "select count(*) from event.noti_info_log where log_date='{}' and desc_detail ='{}'".format(event_date,event_msg)
        ret = self.db.get_row(query)[0][0]
        if ret == 0:
            db_name = 'event.noti_info_log'
            self.db.dbInsertList(event_list, db_name)


    def get_backup_file_cnt(self,db_name):
        query = "SELECT COUNT(*) FROM live.live_ora_tablespace where instance_name='{DB_NAME}' ".format(DB_NAME=db_name)
        try:
            cnt=self.db.getRaw(query)[0][0]
        except:
            cnt = 0

        return cnt





    def main(self):
        # self.check_table()
        today = datetime.datetime.now()
        file_list = self.get_data_file()
        # tb_name = "fbrm.mon_rman_backup_list_%s" % today.strftime('y%Ym%md%d')
        # tb_name = "fbrm.mon_rman_backup_list"
        tcnt = len(file_list)
        print 'file count :', len(file_list)
        cnt = 1
        for file in file_list:
            print file

            self.fead(file)
            db_name, start_time, end_time,session_key, session_recid, session_stamp, progress_date  = self.fead(file)
            backup_file_cnt = 0
            for line in progress_date:
                if 'Name:' in line:
                    # print line
                    backup_file_cnt=backup_file_cnt +1
            target_backup_file_cnt=self.get_backup_file_cnt(db_name)
            print 'target_backup_file_cnt :',target_backup_file_cnt
            progress=float(backup_file_cnt) / float(target_backup_file_cnt) * 100
            print '-'*50

            print
            print 'progress :',target_backup_file_cnt,backup_file_cnt,round(progress,2)

            query = """UPDATE ref.ref_rman_catalog
	SET log_progress_rate='{PROGRESS}'
	WHERE db_name='{DB_NAME}' and session_key='{SESSION_KEY}' and session_recid='{SESSION_RECID}' and session_stamp='{SESSION_STAMP}';""".format(PROGRESS=progress,DB_NAME=db_name,SESSION_KEY=session_key,SESSION_RECID=session_recid,SESSION_STAMP=session_stamp)
            print query
            self.db.queryExec(query)
            #
            #
            # try:
            #     os.remove(file)
            # except:
            #     pass




if __name__ == '__main__':
   fbrm_rman().main()

   #  while True:
   #      fbrm_rman().main()
   #      time.sleep(60)
