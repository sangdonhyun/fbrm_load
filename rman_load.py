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
        self.col_name_list = self.col_set_list()
        self.now = datetime.datetime.now()
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')

        # table_create.table_creat().rman_table()
        # self.check_table()

    def check_table(self):

        td = datetime.datetime.now()
        yd = td - datetime.timedelta(days=1)
        tm = td + datetime.timedelta(days=1)
        tb_char_d = td.strftime('%Y-%m-%d')
        tb_char_y = td.strftime('y%Ym%md%d')
        tb_name = "mon_rman_backup_list_%s" % td.strftime('y%Ym%md%d')
        print tb_name
        sql = "select count(*) from pg_tables where tablename='%s'" % tb_name
        print sql
        ret_cnt = self.db.get_row(sql)[0][0]
        print 'table count :', ret_cnt
        if ret_cnt == 0:
            query = """
CREATE TABLE fbrm.%s
(

    CONSTRAINT %s CHECK (fbrm_date >= '%s'::date)
)
    INHERITS (fbrm.mon_rman_backup_list)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.%s
    OWNER to fbrmuser;
            """ % (tb_name, tb_char_y, tb_char_d, tb_name)
            print query
            self.db.evtInsert(query)
            trigger_query = """
            CREATE OR REPLACE FUNCTION fbrm.backup_list_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF ( NEW.fbrm_date = DATE '%s') THEN
    INSERT INTO fbrm.mon_rman_backup_list_y2020m05d06 VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '%s') THEN
    INSERT INTO fbrm.mon_rman_backup_list_y2020m05d07 VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '%s') THEN
    INSERT INTO fbrm.mon_rman_backup_list_y2020m05d08 VALUES (NEW.*);
ELSE
RAISE EXCEPTION 'Date out of range.  Fix the insert_mon_rman_backup_list_trigger() function!';
END IF;
RETURN NULL;
END;
$BODY$;

ALTER FUNCTION fbrm.backup_list_trigger()
    OWNER TO fbrmuser;

            """ % (yd.strftime('%Y-%m-%d'), td.strftime('%Y-%m-%d'), tm.strftime('%Y-%m-%d'))
            print trigger_query
            # self.db.evtInsert(trigger_query)
            query = """
CREATE OR REPLACE FUNCTION fbrm.merge_mon_rman_backup_list_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$ begin
  if exists ( select 1 from fbrm.mon_rman_backup_list_{date_y} where session_key = new.session_key ) then
    update fbrm.mon_rman_backup_list_{date_y} set 

        session_stamp = new.session_stamp,
        command_id =new.command_id ,
        start_time = new.start_time ,
        end_time = new.end_time, 
        input_bytes = new.input_bytes ,
        output_bytes = new.output_bytes ,
        status_weight = new.status_weight ,
        optimized_weight  = new.optimized_weight,
        input_type_weight = new.input_type_weight ,
        output_device_type  = new.output_device_type,
        autobackup_count = new.autobackup_count,
        backed_by_osb = new.backed_by_osb,
        autobackup_done = new.autobackup_done,
        status = new.status,
        input_type = new.input_type,
        optimized = new.optimized,
        elapsed_seconds = new.elapsed_seconds,
        compression_ratio = new.compression_ratio,
        input_bytes_per_sec = new.input_bytes_per_sec,
        output_bytes_per_sec = new.output_bytes_per_sec,
        input_bytes_display = new.input_bytes_display,
        output_bytes_display =new.output_bytes_display,
        input_bytes_per_sec_display = new.input_bytes_per_sec_display ,
        output_bytes_per_sec_display =new.output_bytes_per_sec_display,
        time_taken_display = new.time_taken_display,
        collect_time =collect_time 

      where session_key = new.session_key  ;
    return null;
    end if;
  return new;
  end; $BODY$;

ALTER FUNCTION fbrm.merge_mon_rman_backup_list_trigger()
    OWNER TO fbrmuser;

            """
            query = query.format(date_y=tb_char_y, date_d=tb_char_d)
            self.db.evtInsert(trigger_query)

            td_1 = td + datetime.timedelta(days=1)
            td_2 = td + datetime.timedelta(days=2)
            td_1_d = td_1.strftime('%Y-%m-%d')
            td_1_y = td_1.strftime('y%Ym%md%d')
            td_2_d = td_2.strftime('%Y-%m-%d')
            td_2_y = td_2.strftime('y%Ym%md%d')
            query = """
CREATE OR REPLACE FUNCTION fbrm.backup_list_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF ( NEW.fbrm_date = DATE '{date_d}') THEN
    INSERT INTO fbrm.mon_rman_backup_list_{date_y}VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{date_1_d}') THEN
    INSERT INTO fbrm.mon_rman_backup_list_{date_1_y} VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{date_2_d}') THEN
    INSERT INTO fbrm.mon_rman_backup_list_{date_2_y} VALUES (NEW.*);
ELSE
RAISE EXCEPTION 'Date out of range.  Fix the insert_mon_rman_backup_list_trigger() function!';
END IF;
RETURN NULL;
END;
$BODY$;

ALTER FUNCTION fbrm.backup_list_trigger()
    OWNER TO fbrmuser;

            """
            query = query.format(date_d=tb_char_d, date_y=tb_char_y, date_1_d=td_1_d, date_1_y=td_1_y, date_2_d=td_2_y,
                                 date_2_y=td_2_y)
            print query

            query = """

            CREATE TRIGGER merge_mon_rman_backup_list_trigger
                BEFORE INSERT
                ON fbrm.mon_rman_backup_list_{date_y}
                FOR EACH ROW
                EXECUTE PROCEDURE fbrm.merge_mon_rman_backup_list_trigger();
                        """
            query = query.format(date_y=tb_char_y)
            print query
            self.db.evtInsert(trigger_query)

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def get_data_file(self):
        path = self.cfg.get('common', 'fbrm_path')
        data_path = os.path.join(path, 'data')
        rman_data_path = os.path.join(path, 'data', 'FBRM_RMAN')
        file_list = glob.glob(os.path.join(rman_data_path, '*.tmp'))
        return file_list

    def set_line_cols(self, line):
        cols_list = line.split(',')
        return cols_list

    def col_set_list(self):
        str = """db_key                                                                          
db_name                                                                         
session_key                                                                     
session_recid                                                                   
session_stamp                                                                   
start_time                                                                      
end_time                                                                        
input_bytes                                                                     
output_bytes                                                                    
status_weight                                                                   
optimized_weight                                                                
input_type_weight                                                               
output_device_type                                                              
autobackup_count                                                                
backed_by_osb                                                                   
autobackup_done                                                                 
status
input_type                                                                          
optimized                                                                       
elapsed_seconds                                                                 
compression_ratio                                                               
input_bytes_per_sec                                                             
output_bytes_per_sec                                                            
input_bytes_display                                                             
output_bytes_display                                                            
input_bytes_per_sec_display                                                     
output_bytes_per_sec_display"""
        col_name_list = []
        for col in str.split():
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


    def data_confirm(self,dict):
        for key in dict.keys():
            if key in ['output_bytes']:
                if dict[key] == '' :
                    dict[key] == '0'
        return dict

    def data_fead(self, hostanme, agent_ip, data_set):
        rman_cat_list = []
        print data_set

        for i in range(len(data_set)):



            line = data_set[i]
            print line

            if ',' in line:
                col_dict = {}
                col_set = self.set_line_cols(line)
                print 'COL SET :',col_set

                for i in range(len(col_set)):
                    col = col_set[i]

                    col_dict[self.col_name_list[i]] = col.strip()
                    col_dict[self.col_name_list[21]] = self.to_byte(data_set[i + 1].split(',')[0])
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
                col_dict = self.data_confirm(col_dict)
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
                    col_dict = self.data_confirm(col_dict)
                    print 'output bytes :',col_dict['output_bytes']
                    rman_cat_list.append(col_dict)



        return rman_cat_list


    def get_show_all(self,cat_data):
        rman_data,show_all_data= '',''
        cnum=len(cat_data)
        for i in range(len(cat_data)):
            line = cat_data[i]
            if 'rows selected.' in line:
                cnum = i
        rman_data = cat_data[:cnum]
        show_all_data = cat_data[cnum:]

        return rman_data,show_all_data



    def fead(self, f):

        hostname, agent_ip = '', ''
        with open(f) as f:
            lineset = f.readlines()
        # print lineset
        for i in range(len(lineset)):
            line = lineset[i]
            if '***###hostname###***' in line:
                hostname = lineset[i + 1].strip()
            if '***###agent_ip###***' in line:
                agent_ip = lineset[i + 1].strip()
            if '***###rman_catalog###***' in line:
                cat_data = lineset[i + 2:]



        print hostname
        print agent_ip

        return hostname, agent_ip, cat_data

    def get_2day(self):
        today=datetime.datetime.now()
        day_list=[]
        for i in range(2):
            oday=today-datetime.timedelta(days=i)
            day_list.append(oday.strftime('%Y-%m-%d'))
        return day_list



    def set_show_all(self,show_all_data):
        for i in range(len(show_all_data)):
            line = show_all_data[i]
            # print line
            if 'CONFIGURE' in line:
                print line

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


    def set_del(self,dict_list,hostname):
        query = "select db_key, session_key, session_recid, session_stamp from live.live_rman_catalog where hostname= '{}'".format(hostname)
        ref=self.db.get_row(query)
        diff_list = []
        del_list=[]
        for dict in dict_list:
            diff1=[dict['db_key'],dict['session_key'],dict['session_recid'],dict['session_stamp']]
            diff_list.append(diff1)
        for ref_val in ref:
            diff_2=[str(ref_val[0]),str(ref_val[1]),str(ref_val[2]),str(ref_val[3])]
            if diff_2 not in diff_list:
                del_list.append(diff_2)

        self.db.del_rman_category(del_list)
        print del_list


    def live_to_store(self,dict_list):

        for i in range(len(dict_list)):
            dict = dict_list[i]
            dict['store_date'] = dict['fbrm_date']
            dict['write_date'] = self.now.strftime('%Y-%m-%d %H:%M:%S')
            dict_list[i]  = dict
        return dict_list


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

            hostname, agent_ip, cat_data = self.fead(file)
            rman_data , show_all_data = self.get_show_all(cat_data)
            dict_list = self.data_fead(hostname, agent_ip, rman_data)
            to_cnt = 0
            live_list=[]


            self.set_show_all(show_all_data)

            day_list = self.get_2day()
            for dict in dict_list:
                start_time = dict['start_time']
                dict['start_date'] = start_time[:10]
                if dict['start_date'] in day_list:
                    live_list.append(dict)
                print 'dict :',dict.keys()
                print dict['output_bytes']
                if dict['output_bytes'] == '':

                    if dict['output_bytes'] == '':
                        dict['output_bytes'] = '0'


                dict = self.data_confirm(dict)

                if 'status' in dict.keys():
                    if dict['status'] not in ['COMPLETED','RUNNING']:
                        self.set_event(dict)

            #     print len(dict.keys()), dict.keys()
            # self.db.dbInsertList(dict_list, tb_name)



            tb_name='live.live_rman_catalog'

            # query = "delete from  {} where start_date not in  ('{}','{}') ".format(tb_name,day_list[0],day_list[1])

            # query = "delete from live.live_rman_catalog where hostname = '{}'".format(hostname)
            # print query
            # self.db.queryExec(query)
            self.set_del(dict_list,hostname)
            self.db.dbInsertList(dict_list, tb_name)




            tb_name = 'store.store_day_rman_catalog'
            store_list = self.live_to_store(dict_list)
            self.db.dbInsertList(store_list, tb_name)
            print 'rman catalog count :',len(store_list)
            print 'sleep 2 sec'
            print "%s/%s"%(str(cnt),tcnt)
            cnt = cnt +1
            print 'RMAN LOAD '
            time.sleep(0.2)


            try:
                os.remove(file)
            except:
                pass

        rman_backup_files.rman_backupfiles().main()


if __name__ == '__main__':
   fbrm_rman().main()

   #  while True:
   #      fbrm_rman().main()
   #      time.sleep(60)
