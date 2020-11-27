import ConfigParser
import os
import glob
import re
import datetime
import fbrm_dbms
import table_create

class srm_load():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.today = datetime.datetime.now()
        self.db = fbrm_dbms.fbrm_db()
        self.tb = table_create.table_make()
        self.rac_mode = 'FALSE'
        self.fbrm_date = self.today.strftime('%Y-%m-%d')

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('../','config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg


    def live_to_store(self,dict_list):

        for i in range(len(dict_list)):
            dict = dict_list[i]
            if 'live_date_time' in dict.keys():
                live_date_time = dict['live_date_time']
                del dict['live_date_time']
                dict['store_date_time'] = live_date_time
                dict['store_date'] = dict['fbrm_date']
                dict['write_date'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
                dict_list[i]  = dict
        return dict_list


    def get_data_file(self):
        path = self.cfg.get('common', 'fbrm_path')
        data_path = os.path.join(path, 'data')
        fs_data_path = os.path.join(path, 'data', 'FBRM_ORA_HSRM')
        print fs_data_path
        file_list = glob.glob(os.path.join(fs_data_path, '*.tmp'))
        return file_list

    def check_table(self,tb_name):
        # tb_name = 'posix_filesystem_realtime'
        if not self.tb.is_table(tb_name):
            self.tb.crate_daily_table(tb_name)
            trigger_query = self.tb.make_query(tb_name)
            self.db.dbQeuryIns(trigger_query)


    def del_tablespace(self,dict_list,oracle_sid):
        live_list =[]
        tb_list = []
        query = "select file_name from live.live_ora_tablespace where instance_name = '{}'".format(oracle_sid)
        filelist=self.db.get_row(query)
        ora_file_list=[]
        for set in filelist:
            live_list.append(set[0])

        for dict in dict_list:
            tb_list.append(dict['file_name'])



    def set_table_space(self,tbs_list):
        """
        fbrm_date date NOT NULL,
        live_date_time character varying(20) COLLATE pg_catalog."default",
        hostname character varying(50) COLLATE pg_catalog."default",
        agent_ip character varying(16) COLLATE pg_catalog."default",
        instance_name character varying(50) COLLATE pg_catalog."default",



        file_name character varying(512) COLLATE pg_catalog."default",
        file_usage numeric,
        tablespace_name character varying(50) COLLATE pg_catalog."default",
        tablespace_size numeric,
        tablespace_usage numeric
        """
        ins_dict_list=[]
        for tbs in tbs_list:

            ins_dict = {}
            ins_dict['fbrm_date'] = self.tb.today_str
            ins_dict['live_date_time'] = self.date_time
            ins_dict['hostname'] = self.hostname
            ins_dict['agent_ip'] = self.agent_ip
            ins_dict['instance_name'] = tbs[1].strip()
            ins_dict['file_name'] = tbs[2].strip()
            ins_dict['file_size'] = tbs[3].strip()
            ins_dict['file_usage'] = tbs[4].strip()
            ins_dict['tablespace_name'] = tbs[5].strip()
            ins_dict['tablespace_size'] = tbs[6].strip()
            ins_dict['tablespace_usage'] = tbs[7].strip()
            ins_dict_list.append(ins_dict)



        tb = 'live.live_ora_tablespace'
        # query = "delete from {} where instance_name = '{}' and fbrm_date <> '{}'".format(tb, self.oracle_sid,self.fbrm_date)
        # print query
        # self.db.queryExec(query)
        self.db.dbInsertList(ins_dict_list,tb)

        store_dict_list = self.live_to_store(ins_dict_list)
        tb = 'store.store_day_ora_tablespace'
        self.db.dbInsertList(store_dict_list, tb)


    def set_redolog(self,redolog_list):
        """
        fbrm_date date NOT NULL,
        live_date_time character varying(20) COLLATE pg_catalog."default",
        hostname character varying(50) COLLATE pg_catalog."default",
        agent_ip character varying(16) COLLATE pg_catalog."default",
        instance_name character varying(50) COLLATE pg_catalog."default",
        log_member character varying(76) COLLATE pg_catalog."default",
        log_size numeric,
        log_group character varying(50) COLLATE pg_catalog."default"
        """
        ins_dict_list = []
        for redolog in redolog_list:
            print redolog
            ins_dict = {}
            ins_dict['fbrm_date'] = self.tb.today_str
            ins_dict['live_date_time'] = self.date_time
            ins_dict['hostname'] = self.hostname
            ins_dict['agent_ip'] = self.agent_ip
            ins_dict['instance_name'] = self.oracle_sid
            ins_dict['log_member'] = redolog[3]
            ins_dict['log_size'] = redolog[4]
            ins_dict['log_group'] = redolog[5]
            ins_dict_list.append(ins_dict)
        tb_name = 'live.live_ora_redolog'
        query = "delete from {} where instance_name = '{}' and fbrm_date <> '{}'".format(tb_name, self.oracle_sid,self.fbrm_date)
        self.db.queryExec(query)
        self.db.dbInsertList(ins_dict_list,tb_name)
        store_dict_list = self.live_to_store(ins_dict_list)
        tb_name = 'store.store_day_ora_redolog'
        self.db.dbInsertList(store_dict_list, tb_name)

    def set_parameter(self,param_list):
        """
        fbrm_date date NOT NULL,
        live_date_time character varying(20) COLLATE pg_catalog."default",
        hostname character varying(50) COLLATE pg_catalog."default",
        agent_ip character varying(16) COLLATE pg_catalog."default",
        dbms character varying(50) COLLATE pg_catalog."default",
        instance_name character varying(50) COLLATE pg_catalog."default",
        name character varying(50) COLLATE pg_catalog."default",
        value numeric,
        description character varying(2048) COLLATE pg_catalog."default"
        :return:
        """
        ins_dict_list = []
        for param in param_list:
            print param
            ins_dict = {}
            ins_dict['fbrm_date'] = self.tb.today_str
            ins_dict['live_date_time'] = self.date_time
            ins_dict['hostname'] = self.hostname
            ins_dict['agent_ip'] = self.agent_ip
            ins_dict['instance_name'] = self.oracle_sid
            ins_dict['name'] = param[3].strip()
            ins_dict['value'] = param[4].strip()
            print 'param :',param[4]
            ins_dict['description'] = param[5].strip()
            ins_dict_list.append(ins_dict)
        tb_name = 'live.live_ora_parameter'
        query = "delete from {} where instance_name = '{}' and fbrm_date <> '{}'".format(tb_name, self.oracle_sid,self.fbrm_date)
        print query
        self.db.queryExec(query)
        self.db.dbInsertList(ins_dict_list, tb_name)

        store_dict_list=self.live_to_store(ins_dict_list)
        tb_name = 'store.store_day_ora_parameter'
        self.db.dbInsertList(store_dict_list, tb_name)
    def set_arch(self,arch_list):
        """
        fbrm_date date NOT NULL,
        live_date_time character varying(20) COLLATE pg_catalog."default",
        hostname character varying(50) COLLATE pg_catalog."default",
        agent_ip character varying(16) COLLATE pg_catalog."default",
        instance_name character varying(50) COLLATE pg_catalog."default",
        arch_date character varying(80) COLLATE pg_catalog."default",
        arch_size numeric,
        arch_cnt numeric

        """
        ins_dict_list = []
        for arch in arch_list:
            print arch
            ins_dict = {}
            ins_dict['fbrm_date'] = self.tb.today_str
            ins_dict['live_date_time'] = self.date_time
            ins_dict['instance_name'] = self.oracle_sid
            ins_dict['hostname'] = self.hostname
            ins_dict['agent_ip'] = self.agent_ip
            ins_dict['arch_date'] = arch[3].strip()
            ins_dict['arch_size'] = arch[4].strip()
            ins_dict['arch_cnt'] = arch[5].strip()

            ins_dict_list.append(ins_dict)

        tb_name = 'live.live_ora_archived_log'
        query = "delete from {} where instance_name = '{}' and fbrm_date <> '{}'".format(tb_name, self.oracle_sid,self.fbrm_date)
        print query

        self.db.queryExec(query)
        self.db.dbInsertList(ins_dict_list, tb_name)
        store_dict_list = self.live_to_store(ins_dict_list)
        tb_name = 'store.store_day_ora_archived_log'
        self.db.dbInsertList(store_dict_list, tb_name)

    def set_tempdb(self,tempdb_list):
        """
         fbrm_date date NOT NULL,
        live_date_time character varying(20) COLLATE pg_catalog."default",
        hostname character varying(50) COLLATE pg_catalog."default",
        agent_ip character varying(16) COLLATE pg_catalog."default",
        dbms character varying(50) COLLATE pg_catalog."default",
        instance_name character varying(50) COLLATE pg_catalog."default",
        size numeric,
        status character varying(16) COLLATE pg_catalog."default",
        name character varying(80) COLLATE pg_catalog."default"

        """
        ins_dict_list = []
        for tempdb in tempdb_list:
            # print tempdb
            ins_dict = {}
            ins_dict['fbrm_date'] = self.tb.today_str
            ins_dict['live_date_time'] = self.date_time
            ins_dict['hostname'] = self.hostname
            ins_dict['agent_ip'] = self.agent_ip
            ins_dict['instance_name'] = self.oracle_sid
            ins_dict['size'] = tempdb[2]
            ins_dict['status'] = tempdb[3]
            ins_dict['name'] = tempdb[4]
            ins_dict_list.append(ins_dict)


        tb_name = 'live.live_ora_tempdb'
        query = "delete from {} where instance_name = '{}' and fbrm_date <> '{}'".format(tb_name,self.oracle_sid,self.fbrm_date)
        print query
        self.db.queryExec(query)

        self.db.dbInsertList(ins_dict_list, tb_name)
        tb_name = 'store.store_day_ora_tempdb'
        store_dict_list = self.live_to_store(ins_dict_list)
        self.db.dbInsertList(ins_dict_list, tb_name)

    def filesystem(self,data):
        print 'hostname :',self.hostname
        lineset=data.splitlines()
        tb_space_list=[]
        parameter_list=[]
        redolog_list=[]
        tempdb_list=[]
        arch_list = []

        for i in range(len(lineset)):
            line = lineset[i]
            arg_set = line.split(',')
            # print arg_set
            if arg_set[0] == 'Oracle':
                tb_space_list.append(arg_set)
            if arg_set[0] == 'FPARM':
                parameter_list.append(arg_set)
            if arg_set[0] == 'FREDU':
                redolog_list.append(arg_set)
            if arg_set[0] == 'FTEMP':
                tempdb_list.append(arg_set)
            if arg_set[0] == 'FARCH':
                arch_list.append(arg_set)
            if arg_set[0] == 'FNPSPARM':
                arch_list.append(arg_set)

            if 'Real Application Clusters ' in line:
                if ',' in line:
                    self.rac_mode = line.split(',')[-1]


        self.set_table_space(tb_space_list)
        # self.set_parameter(parameter_list)
        # self.set_redolog(redolog_list)
        # self.set_tempdb(tempdb_list)
        # self.set_arch(arch_list)

    def get_env(self,data):
        for line in data.splitlines():
            if re.search('^ORACLE_HOME=',line):
                ora_home=line.split('=')[-1]

        return ora_home


    def fread(self,f):
        with open(f) as f:
            fead=f.read()
        # print fead


        dataset=fead.split('###***')
        for data in dataset:
            print data[:10]
            # print data
            if data[:10] == 'HOSTNAME**':
                self.hostname = data.split('***###')[-1].strip()
            if data[:10] == 'AGENT_IP**':
                self.agent_ip = data.split('***###')[-1].strip()
            if data[:10] == 'date_time*':
                self.date_time = data.split('***###')[-1].strip()
            if data[:10] == 'ORACLE_SID':
                self.oracle_sid = data.split('***###')[-1].strip()
            if data[:10] == 'ORACLE_HOM':
                ora_home=self.get_env(data.split('***###')[-1].strip())
            if data[:10] == 'ORACLE_SPO':
                self.filesystem(data.split('***###')[-1])


        master_ora_info_list =[]
        master_ora_info_dic = {}
        """
        SELECT ora_id, ora_sid, ora_home, ora_alias, ser_id, svr_hostname, svr_ip_v4, ora_biz_dep_a, ora_biz_dep_b, ora_biz_dep_c, ora_is_rac, tmp
FROM master.master_ora_info;
        """

        master_ora_info_dic['ora_sid'] = self.oracle_sid
        query = "select svr_id from master.master_svr_info where svr_hostname = '{hostname}' and svr_ip_v4 = '{agent_ip}'".format(
            hostname=self.hostname, agent_ip=self.agent_ip)
        print query
        ret = self.db.get_row(query)
        svr_serial = ret[0][0]
        master_ora_info_dic['svr_id'] = svr_serial
        master_ora_info_dic['svr_hostname'] = self.hostname
        master_ora_info_dic['svr_ip_v4'] = self.agent_ip
        master_ora_info_dic['ora_is_rac'] = self.rac_mode
        master_ora_info_dic['ora_home'] = ora_home
        master_ora_info_dic['inst_datetime'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
        master_ora_info_dic['fbrm_datetime'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
        master_ora_info_list.append(master_ora_info_dic)
        tb_name = 'master.master_ora_info'
        self.db.dbInsertList(master_ora_info_list, tb_name)

        """
               u_id, svr_id, svr_hostname, svr_ip, ora_id, ora_sid, inst_datetime, fbrm_datetime
                """

        live_svr_ora_list=[]
        live_svr_ora_dict = {}
        live_svr_ora_dict['svr_id']  = svr_serial
        live_svr_ora_dict['svr_hostname'] = self.hostname

        live_svr_ora_dict['svr_ip'] = self.agent_ip
        query = "select svr_id from master.master_ora_info where ora_sid = '{ora_sid}'".format(ora_sid=self.oracle_sid)

        ora_id = self.db.get_row(query)[0][0]

        live_svr_ora_dict['ora_id'] = ora_id
        live_svr_ora_dict['ora_sid'] =self.oracle_sid

        live_svr_ora_dict['inst_datetime'] =self.today.strftime('%Y-%m-%d %H:%M:%S')
        live_svr_ora_dict['fbrm_datetime'] =self.today.strftime('%Y-%m-%d %H:%M:%S')
        live_svr_ora_list.append(live_svr_ora_dict)
        tb_name = 'live.live_svr_ora'
        self.db.dbInsertList(live_svr_ora_list, tb_name)
        tb_name = 'store.store_svr_ora'
        self.db.dbInsertList(live_svr_ora_list, tb_name)



    def get_sid(self):
        query  = 'select * from master.master_svr_info where '

    def main(self):
        flist =self.get_data_file()
        for f in flist:
            print 'file name :',f
            self.fread(f)
            # os.remove(f)



if __name__=='__main__':
    srm_load().main()
