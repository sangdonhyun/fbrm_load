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
import re

class fbrm_rman():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.db = fbrm_dbms.fbrm_db()
        self.col_name_list = self.col_set_list()
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')


        # table_create.table_creat().rman_table()


    def check_table(self):

        td = datetime.datetime.now()
        yd = td - datetime.timedelta(days=1)
        tm = td + datetime.timedelta(days=1)
        tb_char_d = td.strftime('%Y-%m-%d')
        tb_char_y = td.strftime('y%Ym%md%d')
        tb_org = "mon_ora_backup_files"
        tb_name = "mon_ora_backup_files_%s" % td.strftime('y%Ym%md%d')
        print tb_name
        sql = "select count(*) from pg_tables where tablename='%s'" % tb_name
        print sql
        ret_cnt = self.db.get_row(sql)[0][0]
        print 'table count :', ret_cnt
        if ret_cnt == 0:
            query = """

CREATE TABLE fbrm.mon_ora_backup_files_{date_y}
(
    
    CONSTRAINT {date_y} CHECK (fbrm_date >= '{date_d}'::date)
)
    INHERITS (fbrm.{ta_name_org})
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.{tb_name}
    OWNER to fbrmuser;    
            """.format(date_y=tb_char_y,date_d=tb_char_d,ta_name_org = tb_org,tb_name = tb_name)
            print query
            self.db.evtInsert(query)



            td_1 = td + datetime.timedelta(days=1)
            td_2 = td + datetime.timedelta(days=2)
            td_1_d = td_1.strftime('%Y-%m-%d')
            td_1_y = td_1.strftime('y%Ym%md%d')
            td_2_d = td_2.strftime('%Y-%m-%d')
            td_2_y = td_2.strftime('y%Ym%md%d')
            query = """


 CREATE OR REPLACE FUNCTION fbrm.mon_ora_backup_files_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF ( NEW.fbrm_date = DATE '{date_d}') THEN
    INSERT INTO fbrm.mon_ora_backup_files_{date_y} VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{date_1_d}') THEN
    INSERT INTO fbrm.mon_ora_backup_files_{date_1_y} VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{date_2_d}') THEN
    INSERT INTO fbrm.mon_ora_backup_files_{date_2_y} VALUES (NEW.*);
ELSE
RAISE EXCEPTION 'Date out of range.  Fix the mon_ora_session_longops_trigger() function!';
END IF;
RETURN NULL;
END;
$BODY$;

ALTER FUNCTION fbrm.mon_ora_backup_files_trigger()
    OWNER TO fbrmuser;

            """
            query = query.format(date_d=tb_char_d, date_y=tb_char_y, date_1_d=td_1_d, date_1_y=td_1_y, date_2_d=td_2_y,
                                 date_2_y=td_2_y)
            print query

            # query = """
            #
            # CREATE TRIGGER merge_mon_rman_backup_list_trigger
            #     BEFORE INSERT
            #     ON fbrm.mon_rman_backup_list_{date_y}
            #     FOR EACH ROW
            #     EXECUTE PROCEDURE fbrm.merge_mon_rman_backup_list_trigger();
            #             """
            # query = query.format(date_y=tb_char_y)
            # print query
            # self.db.evtInsert(trigger_query)

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def get_data_file(self):
        path = self.cfg.get('common', 'fbrm_path')
        data_path = os.path.join(path, 'data')
        rman_data_path = os.path.join(path, 'data', 'FBRM_ORA_BAKUP')
        file_list = glob.glob(os.path.join(rman_data_path, '*.tmp'))
        return file_list

    def set_line_cols(self, line):
        cols_list = line.split(',')
        return cols_list

    def col_set_list(self):
        str = """pkey numeric,backup_type,file_type,status,fname,completion_time,"""
        col_name_list = []
        for col in str.split(','):
            col_name_list.append(col)
        return col_name_list

    def to_byte(self, num):
        bnum = 0
        if 'K' in num.upper():
            num = num.replace('K', '')
            bnum = float(num) * 1024
        elif 'M' in num.upper():
            num = num.replace('M', '')
            bnum = float(num) * 1024 * 1024
        elif 'G' in num.upper():
            num = num.replace('G', '')
            bnum = float(num) * 1024 * 1024 * 1024

        else:
            try:
                bnum = int(num)
            except:
                bnum = 0

        return bnum

    def to_num(self, chr):
        if chr == '':
            return 0
        else:
            return chr

    def data_fead(self, hostanme, agent_ip, data_set):
        rman_cat_list = []

        for i in range(len(data_set)):

            line = data_set[i]
            cnt = i % 6
            if cnt == 0:
                col_dict = {}
                col_set = self.set_line_cols(line)
                for i in range(len(col_set)):
                    col = col_set[i]
                    col_dict[self.col_name_list[i]] = col.strip()

            elif cnt == 1:
                # print cnt, 21, self.col_name_list[21], line.strip()
                col_dict[self.col_name_list[21]] = self.to_byte(line.split(',')[0])
            elif cnt == 2:
                # print cnt, 22, self.col_name_list[22], line.strip()
                col_dict[self.col_name_list[22]] = self.to_byte(line.split(',')[0])
            elif cnt == 3:
                # print cnt, 23, self.col_name_list[23], line.strip()
                col_dict[self.col_name_list[23]] = self.to_byte(line.split(',')[0])
            elif cnt == 4:
                # print cnt, 24, self.col_name_list[24], line.strip()
                col_dict[self.col_name_list[24]] = self.to_byte(line.split(',')[0])
            else:
                # print 'line : ', line
                col_dict['hostname'] = hostanme
                col_dict['agent_ip'] = agent_ip
                col_dict['fbrm_date'] = self.today
                col_dict['db_name'] = self.oracle_sid

                if len(col_dict.keys()) == 28:
                    col_dict['input_bytes_per_sec'] = self.to_num(col_dict['input_bytes_per_sec'])
                    rman_cat_list.append(col_dict)
        return rman_cat_list
    def get_col(self):
        return ["pkey","backup_type","file_type","status","fname","tag","completion_time"]



    def fead(self, fname):
        col_set = self.get_col()
        with open(fname) as f:
            lineset = f.readlines()
        print '-' * 50
        line_list = []
        fbrm_date = self.today
        hostname, agent_ip = '', ''
        oracle_sid=''

        for i in range(len(lineset)):
            line = lineset[i]
            if 'DATA TIME :' in line:
                date_str = line.split('DATA TIME :')[-1]
                date_str = date_str.replace('#', '')
                live_date_time = date_str.strip()
                print live_date_time

            if '###***HOSTNAME***###' in line:
                hostname = lineset[i + 1].strip()
            if '###***AGENT_IP***###' in line:
                agent_ip = lineset[i + 1].strip()
            if '###***ORACLE_SID***###' in line:
                self.oracle_sid = lineset[i + 1].strip()
                self.db_name = self.oracle_sid
            if '###***ZFS_NAME***###' in line:
                zfs_name = lineset[i + 1].strip()

            if ',' in line and '--------------' not in line and 'SQL_ADDRESS' not in line:
                argset = line.split(',')

                if re.search('^DBNAME',line):
                    self.db_name = line.split(',')[-1].strip()


                if len(argset) == 7:
                    dict_info = {}
                    # print argset,len(argset)
                    # print col_set
                    # print len(argset)
                    # print len(col_set)
                    # print argset
                    # print col_set
                    if '      PKEY' not in argset:

                        for j in range(len(argset)):
                            arg = argset[j].strip()
                            # print len(col_set)
                            # print len(argset)
                            dict_info[col_set[j]] = arg
                        # print dict_info.keys()


                        dict_info['hostname'] = hostname
                        dict_info['db_name'] = self.db_name
                        dict_info['agent_ip'] = agent_ip
                        dict_info['fbrm_date'] = fbrm_date
                        dict_info['zfs_name'] = zfs_name
                        dict_info['node_name'] = zfs_name
                        dict_info['live_date_time'] = live_date_time
                        #2020/06/21 10:30
                        print dict_info['completion_time']
                        c_time = str(dict_info['completion_time']).strip()
                        print 'ctime :',c_time,len(c_time),c_time[:4]
                        print ''

                        #2020/06/21 10:30
                        completion_datetime = datetime.datetime.strptime('2020/06/21 10:30', '%Y/%m/%d %H:%M')
                        print completion_datetime
                        
                        print '-'*40

                        completion_datetime = datetime.datetime.strptime(dict_info['completion_time'], '%Y/%m/%d %H:%M').strftime('%Y-%m-%d %H:%M:00')
                        completion_date = datetime.datetime.strptime(dict_info['completion_time'], '%Y/%m/%d %H:%M').strftime('%Y-%m-%d')
                        dict_info['completion_time'] = completion_datetime
                        dict_info['completion_date'] = completion_date

                        line_list.append(dict_info)
        return line_list


    def live_to_store(self,dict_list):

        for i in range(len(dict_list)):
            dict = dict_list[i]
            if 'live_date_time' in dict.keys():
                live_date_time = dict['live_date_time']
                del dict['live_date_time']
                dict['store_date_time'] = live_date_time
                dict['store_date'] = self.today
                dict['write_date'] = live_date_time
                dict_list[i]  = dict
        return dict_list


    def main(self):
        # self.check_table()
        today = datetime.datetime.now()
        file_list = self.get_data_file()

        # tb_name = "fbrm.mon_ora_backup_files"
        tcnt = len(file_list)
        print 'file count :', len(file_list)
        cnt = 1
        file_lsit = file_list[:1]
        for file in file_list:
            print file


            dict_list=self.fead(file)

            # for dict in dict_list:
            #     print dict
            #     print len(dict.keys()), dict.keys()
            query = "delete from live.live_ora_backupfiles where db_name = '{}'".format(self.oracle_sid)
            self.db.queryExec(query)
            tb_name = "live.live_ora_backupfiles"
            self.db.dbInsertList(dict_list, tb_name)
            store_dict_list = self.live_to_store(dict_list)

            tb_name = 'store.store_day_ora_backupfiles'
            self.db.dbInsertList(store_dict_list, tb_name)
            print 'sleep 2 sec'
            print "%s/%s"%(str(cnt),tcnt)
            cnt = cnt +1
            print 'ORACLE BACKUP FILE LOAD'
            time.sleep(2)
            try:
                os.remove(file)
            except:
                pass


if __name__ == '__main__':
    fbrm_rman().main()
    # while True:
    #     try:
    #         fbrm_rman().main()
    #     except:
    #         pass
    #     time.sleep(60)
