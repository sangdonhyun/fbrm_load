import ConfigParser
import os
import sys
import glob
import datetime
import fbrm_dbms
import table_create
class fs_load():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.today = datetime.datetime.now()
        self.db = fbrm_dbms.fbrm_db()
        self.tb = table_create.table_make()
        self.check_table()



    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def get_data_file(self):
        path = self.cfg.get('common', 'fbrm_path')
        data_path = os.path.join(path, 'data')
        fs_data_path = os.path.join(path, 'data', 'FBRM_FS')
        print fs_data_path
        file_list = glob.glob(os.path.join(fs_data_path, '*.tmp'))
        return file_list

    def check_table(self):
        tb_name = 'posix_filesystem_realtime'
        if not self.tb.is_table(tb_name):
            self.tb.crate_daily_table(tb_name)
            trigger_query = self.tb.make_query(tb_name)
            self.db.dbQeuryIns(trigger_query)


    def filesystem(self,data):
        lineset=data.splitlines()
        arg_list=[]
        print data
        title = ['Filesystem','1K-blocks','Used','Available','Used_rate',' Mounted_on']
        for i in range(len(lineset)):
            line = lineset[i]
            arg_set = line.split()
            if len(arg_set) == 1:
                arg_list.append(arg_set + lineset[i+1].split())
            if len(arg_set) == 6:
                arg_list.append(arg_set)

        return arg_list


    def zfs_hosts(self,data):
        """
         check_date_time character varying(20) COLLATE pg_catalog."default",
        server_hostname character varying(50) COLLATE pg_catalog."default",
        server_ip character varying(16) COLLATE pg_catalog."default",
        zfs_hostname character varying(50) COLLATE pg_catalog."default",
        zfs_ip character varying(16) COLLATE pg_catalog."default",
        :param data:
        :return:
        """
        print data
        zfs_host_list=[]
        zfs_sever_hosts=[]
        for arg in self.arg_list:
            fs=arg[0]
            if ':' in fs:
                zfs_fs=fs.split(':')[0]
                zfs_host_list.append(zfs_fs)
        print '#'*59
        print zfs_host_list
        for line in data.splitlines():
            if '#' not in line:
                lineset= line.split()
                print line
                if len(lineset) > 1:
                    ip=lineset[0]
                    hostname=lineset[1]
                    for zfs in zfs_host_list:
                        if zfs in hostname:
                            zfs_server_hosts_info={}
                            zfs_server_hosts_info['check_date_time'] = self.date_time
                            zfs_server_hosts_info['server_hostname'] = self.hostname
                            zfs_server_hosts_info['server_ip'] = self.agent_ip
                            zfs_server_hosts_info['zfs_hostname'] = zfs
                            zfs_server_hosts_info['zfs_service_ip'] = ip
                            zfs_server_hosts_info['zfs_alias'] = ip
                            zfs_sever_hosts.append(zfs_server_hosts_info)
        tb_name = 'live.live_zfs_server_hosts'
        print zfs_sever_hosts

        self.db.dbInsertList(zfs_sever_hosts,tb_name)



    def get_nfs_capacity(self,fs):
        ret = '','','',''
        for arg in self.arg_list:
            if fs== arg[0]:
                ret= arg[1],arg[2],arg[3],arg[4]
        return ret
    def nfs_mounted(self,data):
        """check_date_time character varying(20) COLLATE pg_catalog."default",
        server_hostname character varying(50) COLLATE pg_catalog."default",
        server_ip character varying(16) COLLATE pg_catalog."default",
        filesystem character varying(50) COLLATE pg_catalog."default",
        mounted  character varying(50) COLLATE pg_catalog."default",
        mounted_bit  bool default False ,
        check_bit bool default False ,
        """
        nfs_list=[]
        zfs_name = ''
        zfs_ip = ''
        blocks, Used, Available, Used_rate = '','','',''
        print '-'*40
        print self.arg_list

        for line in data.splitlines():
            if ',' in line:
                nfs={}
                lineset=line.split(',')
                # print lineset
                nfs['check_date_time'] =lineset[0]
                nfs['server_hostname'] =lineset[1]
                nfs['server_ip'] = lineset[2]
                nfs['filesystem'] = lineset[3].strip()


                blocks, Used, Available, Used_rate = self.get_nfs_capacity(nfs['filesystem'])

                # print nfs['filesystem']
                print 'available:',blocks, Used, Available, Used_rate
                # nfs['ussage_blocks'] = blocks
                nfs['ussage_used'] = Used
                nfs['ussage_available'] = Available
                nfs['ussage_used_capacity'] = Used_rate



                nfs['mounted'] = lineset[4]
                nfs['zfs_hostname'] = lineset[5]
                nfs['mounted_bit'] = lineset[6]
                nfs['check_bit'] = 'True'
                nfs['fbrm_date'] = self.today.strftime('%Y-%m-%d')


                fs= nfs['filesystem']
                if ':' in fs:
                    net_zfs=fs.split(':')[0]
                    if '.' in net_zfs:
                        zfs_name = zfs_name
                        zfs_ip = zfs_ip
                    else:
                        zfs_name  = net_zfs
                        query ="select zfs_service_ip from live.live_zfs_server_hosts where zfs_hostname = '{zfs_name}'".format(zfs_name=zfs_name)
                        print query
                        try:
                            zfs_ip =self.db.get_row(query)[0][0]
                        except:
                            zfs_ip = ''

                        query = "select zfs_name,zfs_cluster from live.live_zfs_network_interfaces where  zfs_service_ip = '{service_ip}'".format(service_ip=zfs_ip)
                        print query
                        try:
                            zfs_name = self.db.get_row(query)[0][0]
                            asn = self.db.get_row(query)[0][1]
                            nfs['zfs_name'] = zfs_name
                            nfs['node_name'] = zfs_name
                            nfs['zfs_ip'] = zfs_ip

                            nfs['zfs_cluster'] = asn

                            nfs_list.append(nfs)
                        except:
                            pass

        print nfs_list
        for arg in  self.arg_list:
            print arg


        tb_name='live.live_svr_nfs_mounted_on'
        query = "delete from {} where server_hostname = '{}'".format(tb_name, self.hostname)
        print query
        self.db.queryExec(query)
        self.db.dbInsertList(nfs_list,tb_name)
        tb_name = 'store.store_day_svr_nfs_mounted_on'

        self.db.dbInsertList(nfs_list, tb_name)

        return nfs_list




    def get_uname(self,data):
        os_type = ''
        dataset= data.split()
        os_type = dataset[0]
        return os_type

    def get_release(self,data):
        print data
        """
        VERSION="6.8"
ID="ol"
VERSION_ID="6.8"
PRETTY_NAME="Oracle Linux Server 6.8"
        :param data:
        :return:
        """
        self.os_ver = ''
        self.os_ver_rel = ''

        for line in data.splitlines():
            print line
            if 'VERSION=' in line:
                self.os_ver = line.split('=')[-1]
            if 'PRETTY_NAME=' in line:
                self.os_ver_rel = line.split('=')[-1]

    def is_dbms(self,data):
        is_db=''
        if 'ora_pmon' in data:
            is_db='ORACLE'
        if 'catdb' in data:
            is_db='RMAN'
        return is_db

    def fread(self,f):
        with open(f) as f:
            fead=f.read()
        # print fead
        dataset=fead.split('###***')
        for data in dataset:
            print data[:10]
        os_type,get_is_vm,user_id,is_db = '','','',''
        for data in dataset:
            print data[:10]
            print data
            if data[:10] == 'hostname**':
                self.hostname = data.split('***###')[-1].strip()
            if data[:10] == 'agent_ip**':
                self.agent_ip = data.split('***###')[-1].strip()
            if data[:10] == 'date_time*':
                self.date_time = data.split('***###')[-1].strip()
            if data[:10] == 'df -k***##':
                self.arg_list=self.filesystem(data.split('***###')[-1])
            if data[:10] == 'cat /etc/h':
                self.zfs_hosts(data.split('***###')[-1])
            if data[:10] == 'nsf_mounte':
                nfs_list=self.nfs_mounted(data.split('***###')[-1])
            if data[:10] == 'uname***##':
                os_type = self.get_uname(data.split('***###')[-1])
            if data[:10] == 'release***':
                self.get_release(data.split('***###')[-1])
            if data[:10] == 'virt-what*':
                get_is_vm = data.split('***###')[-1].strip()
            if data[:10] == 'is_dbms***':
                is_db = self.is_dbms(data.split('***###')[-1])
            if data[:10] == 'whoami***#':
                user_id = data.split('***###')[-1].strip()

        ins_dict_list=[]
        for arg in self.arg_list:
            ins_dict={}
            ins_dict['hostname'] = self.hostname
            ins_dict['agent_ip'] = self.agent_ip
            ins_dict['live_date_time'] = self.date_time
            ins_dict['fbrm_date'] = self.today.strftime('%Y-%m-%d')
            ins_dict['filesystem']    = arg[0]
            ins_dict['blocks']        = arg[1]
            ins_dict['used']          = arg[2]
            ins_dict['available']     = arg[3]
            ins_dict['used_capacity'] = arg[4]
            ins_dict['mounted']       = arg[5]

            ins_dict_list.append(ins_dict)
        # self.check_table()
        # self.db.dbInsertList(ins_dict_list,'fbrm.posix_filesystem_realtime_{date_y}'.format(date_y=self.tb.today_y))
        """
        INSERT INTO master.master_svr_info(
	svr_serial, svr_hostname, os_type, os_ver, os_ver_rel, svr_ip_v4, svr_is_vm, svr_op_type, user_id, dbms_info, svr_biz_dep_a, svr_biz_dep_b, svr_biz_dep_c, svr_center, svr_position, tmp)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        master_svr_list=[]
        master_dic = {}
        master_dic['svr_hostname'] = self.hostname
        master_dic['os_type'] = os_type
        master_dic['os_ver'] = self.os_ver
        master_dic['os_ver_rel'] = self.os_ver_rel
        master_dic['svr_ip_v4'] = self.agent_ip
        master_dic['svr_is_vm'] =get_is_vm
        master_dic['svr_op_type'] =''
        master_dic['user_id'] = user_id
        master_dic['dbms_info'] =is_db
        master_dic['inst_datetime'] = self.today.strftime('%Y-%m-%d')
        master_dic['fbrm_datetime'] = self.today.strftime('%Y-%m-%d')
        master_svr_list.append(master_dic)
        tb_name = 'master.master_svr_info'
        self.db.dbInsertList(master_svr_list, tb_name)

        print nfs_list
        for nfs in nfs_list:
            print nfs


    def main(self):
        flist =self.get_data_file()
        for f in flist:
            print f
            self.fread(f)



if __name__=='__main__':
    fs_load().main()
