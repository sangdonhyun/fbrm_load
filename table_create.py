import os
import datetime
import fbrm_dbms

class table_make():
    def __init__(self):
        self.db=fbrm_dbms.fbrm_db()
        self.today = datetime.datetime.now()
        self.today_str = self.today.strftime('%Y-%m-%d')
        self.today_y = self.today.strftime('y%Ym%md%d')
        self.date_1 = (self.today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.date_2 = (self.today - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        self.date_y_1 =(self.today - datetime.timedelta(days=1)).strftime('y%Ym%md%d')
        self.date_y_2 =(self.today - datetime.timedelta(days=2)).strftime('y%Ym%md%d')


    def make_query(self,tb_name):

        query ="""
        
CREATE OR REPLACE FUNCTION fbrm.{table_name}_realtime_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF ( NEW.fbrm_date = DATE '{date_2}') THEN
    INSERT INTO fbrm.{table_name}_realtime_{date_y_2} VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{date_1}') THEN
    INSERT INTO fbrm.mon_{table_name}_realtime_{date_y_1} VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '{to_day}') THEN
    INSERT INTO fbrm.mon_{table_name}_realtime_{today_y} VALUES (NEW.*);
ELSE
RAISE EXCEPTION 'Date out of range.  Fix the {table_name}_realtime_trigger() function!';
END IF;
RETURN NULL;
END;
$BODY$;

ALTER FUNCTION fbrm.{table_name}_realtime_trigger()
    OWNER TO fbrmuser;

        """.format(table_name=tb_name,date_1=self.date_1,date_2=self.date_2,to_day=self.today_str,today_y=self.today_y,date_y_1=self.date_y_1,date_y_2=self.date_y_2)
        return  query

    def get_tb_list(self):
        tb_list=['mon_ora_backup_file','mon_ora_session_longops','mon_rman_backup_list',
                 'mon_zfs_filesystem','zfs_pools','zfs_projects',
                 'zfs_snapshots']
        return tb_list

    def is_table(self,tb_name):
        query="select count(*) from pg_tables where tablename = '{tb_name}_{date_y}'".format(tb_name=tb_name,date_y=self.today_y)
        print query
        ret=self.db.get_row(query)
        ret_cnt = ret[0][0]
        if ret_cnt == 0:
            return False
        else:
            return True



    def crate_daily_table(self,tb_name):
        query = """
CREATE TABLE fbrm.{tb_name}_{date_y}
(
   
    CONSTRAINT {date_y} CHECK (fbrm_date >= '{today}'::date)
)
    INHERITS (fbrm.{tb_name})
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.{tb_name}_{date_y}
    OWNER to fbrmuser;
        """.format(tb_name=tb_name,date_y=self.today_y,today=self.today_str)
        print query
        self.db.dbQeuryIns(query)

    def main(self):
        tb='mon_zfs_filesystem'
        for tb in self.get_tb_list():
            query = self.make_query(tb)
            print query
            self.db.dbQeuryIns(query)


if __name__=='__main__':
    table_make().main()