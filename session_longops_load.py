'''
Created on 2020. 4. 6.

@author: user
'''
import os
import glob
import sys
import ConfigParser
import fbrm_dbms
import datetime
import time

"""sid
serial#
opname
target
target_desc
sofar
totalwork
units
start_time
last_update_time
timestamp
time_remaining
elapsed_seconds
context
message
username
sql_address
sql_hash_value
sql_id
sql_plan_hash_value
sql_exec_
sql_exec_id
sql_plan_line_id
sql_plan_operation
sql_plan_options
qcsid"""

class fbrm_rman():
    def __init__(self):
        self.cfg=self.get_cfg()
        self.db= fbrm_dbms.fbrm_db()
        self.today = datetime.datetime.now()
        self.to_day=datetime.datetime.now().strftime('%Y-%m-%d')
        self.table_check()
        self.sid = ''
    
    def get_cfg(self):
        cfg=ConfigParser.RawConfigParser()
        cfg_file = os.path.join('config','config.cfg')
        cfg.read(cfg_file)
        return cfg

    def table_create(self):
        date_d = self.today.strftime('%Y-%m-%d')
        date_y = self.today.strftime('y%Ym%md%d')
        query="""
CREATE TABLE fbrm.mon_ora_session_longops_{date_y}
(
    
    CONSTRAINT {date_y} CHECK (fbrm_date >= '{date_d}'::date)
)
    INHERITS (fbrm.mon_ora_session_longops)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.mon_ora_session_longops_{date_y}
    OWNER to fbrmuser;
        """

        query = query.format(date_d=date_d,date_y=date_y)
        print query
        self.db.queryExec(query)


        date_1 = self.today + datetime.timedelta(days=1)
        date_2 = self.today + datetime.timedelta(days=2)
        date_1_d = date_1.strftime('%Y-%m-%d')
        date_1_y = date_1.strftime('y%ym%md%d')
        date_2_d = date_2.strftime('%Y-%m-%d')
        date_2_y = date_2.strftime('y%ym%md%d')
        trigger_query="""
        CREATE OR REPLACE FUNCTION fbrm.mon_ora_session_longops_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF ( NEW.fbrm_date = DATE '{date_d}') THEN
    INSERT INTO fbrm.mon_ora_session_longops_{date_y} VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{date_1_d}') THEN
    INSERT INTO fbrm.mon_ora_session_longops_{date_1_y} VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{date_2_d}') THEN
    INSERT INTO fbrm.mon_ora_session_longops_{date_2_y} VALUES (NEW.*);
ELSE
RAISE EXCEPTION 'Date out of range.  Fix the mon_ora_session_longops_trigger() function!';
END IF;
RETURN NULL;
END;
$BODY$;

ALTER FUNCTION fbrm.mon_ora_session_longops_trigger()
    OWNER TO fbrmuser;

        """
        trigger_query = trigger_query.format(date_d=date_d,date_y=date_y,date_1_d=date_1_d,date_1_y=date_1_y,date_2_d=date_2_d,date_2_y=date_2_y)
        print trigger_query
        self.db.queryExec(trigger_query)


    def table_check(self):
        date_y=self.today.strftime('y%Ym%md%d')
        tb_name = "mon_ora_session_longops_{date_str_y}"
        tb_name = tb_name.format(date_str_y=date_y)
        self.tb_name = "fbrm."+tb_name
        query = "select count(*) from pg_tables where tablename ='{table}'"
        query = query.format(table=tb_name)
        print query
        ret_cnt = self.db.get_row(query)[0][0]
        print 'ret_cnt : ', ret_cnt
        if ret_cnt == 0:
            self.table_create()

    def get_file_list(self):
        print self.cfg.sections()
        fbrm_path=self.cfg.get('common','fbrm_path')
        fbrm_ora_dir=os.path.join(fbrm_path,'data','FBRM_ORA_MON')
        file_list=glob.glob(os.path.join(fbrm_ora_dir,'*'))
        return file_list


    def get_col(self):
        col_str="""sid
serial
opname
target
target_desc
sofar
totalwork
units
start_time
last_update_time
timestamp
time_remaining
elapsed_seconds
context
message
username
sql_address
sql_hash_value
sql_id
sql_plan_hash_value
sql_exec_
sql_exec_id
sql_plan_line_id
sql_plan_operation
sql_plan_options
db_name
complete
live_date_time
db_name
qcsid"""
        return col_str.split()
    def fead(self,fname):
        col_set=self.get_col()
        with open(fname) as f:
            lineset = f.readlines()
        print '-'*50
        line_list=[]
        fbrm_date = self.to_day
        hostname,agent_ip = '',''
        for i in range(len(lineset)):
            line=lineset[i]
            if 'DATA TIME :' in line:
                date_str = line.split('DATA TIME :')[-1]
                date_str = date_str.replace('#','')
                live_date_time  = date_str.strip()
                print live_date_time



            if '###***HOSTNAME***###' in line:
                hostname=lineset[i+1].strip()
            if '###***AGENT_IP***###' in line:
                agent_ip=lineset[i+1].strip()
            if '###***ORACLE_SID***###' in line:
                self.sid=lineset[i+1].strip()

            if ',' in line and '--------------' not in line and 'SQL_ADDRESS' not in line:
                argset=line.split(',')

                dict_info = {}
                for j in range(len(argset)):
                    arg=argset[j].strip()

                    dict_info[col_set[j]] = arg
                if len(dict_info.keys()) > 10:
                    dict_info['hostname'] = hostname
                    dict_info['agent_ip'] = agent_ip
                    dict_info['fbrm_date'] = fbrm_date
                    dict_info['live_date_time'] = live_date_time

                    dict_info['db_name'] = self.sid

                    line_list.append(dict_info)
        return line_list
    def get_date_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    def main(self):
        file_list=self.get_file_list()
        cnt=1
        tot=len(file_list)
        for f_name in file_list:
            print f_name
            dict_list=self.fead(f_name)

            # tb_name='fbrm.mon_ora_session_longops'
            for dict  in dict_list:
                ins_datetime = self.get_date_time()
                print dict.keys()
                dict['sql_id'] = 0
                print dict['serial'],dict['fbrm_date'],dict['sid'],dict['sql_id']
                sofar= dict['sofar']
                totalwork = dict['totalwork']
                try:
                    complete = round((int(sofar)/int(totalwork))*100)
                except:
                    complete = 0

                dict['complete'] = complete

                dict['ins_date_time'] = ins_datetime



            # self.db.dbInsertList(dict_list, self.tb_name)



            tb_name = 'live.live_ora_session_longops'
            query = "delete from {} where db_name = '{}' " .format(tb_name,self.sid)
            self.db.queryExec(query)
            self.db.dbInsertList(dict_list, tb_name)
            for i in range(len(dict_list)):
                dict = dict_list[i]
                if 'live_date_time' in dict.keys():
                    store_date_time = dict['live_date_time']
                    del dict['live_date_time']
                    dict['store_date_time'] = store_date_time
                    dict_list[i]  = dict



            tb_name = 'store.store_day_ora_session_longops'
            self.db.dbInsertList(dict_list, tb_name)


            print 'session longops load'
            print '{}/{}'.format(cnt,tot)
            cnt = cnt +1

            os.remove(f_name)
            print 'sleep 0.2sec'
            time.sleep(0.2)


        

if __name__=='__main__':
    fbrm_rman().main()
    # while True:
    #     fbrm_rman().main()
    #     print 'wati 60'
    #     time.sleep(60)