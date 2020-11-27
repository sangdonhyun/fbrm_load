import ConfigParser
import datetime
import glob
import json
import os
import re
import sys
import fbrm_dbms

event_files=glob.glob(os.path.join('data','event*.txt'))

class zfs_curl_pool():
    def __init__(self):
        self.cfg= self.get_cfg()
        self.today = datetime.datetime.now()
        self.check_date = self.today.strftime('%Y-%m-%d %H:%M:%S')
        self.db= fbrm_dbms.fbrm_db()

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg



    def to_local_time(self, utc):
        """
        Thu Nov 15 2018 23:10:39 GMT+0000 (UTC)
        :param utc:
        :return:
        Thu Nov 15 2018 23:10:39 GMT+0000 (UTC)
        """
        utc_time = datetime.datetime.strptime(utc, "%a %b %d %Y %H:%M:%S GMT+0000 (UTC)")
        local_time = utc_time + datetime.timedelta(hours=9)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def set_sysver(self, arg):
        lines = arg.split('-' * 30)[1]
        curl_lineset = lines[lines.index('{') - 1:]
        root = json.loads(curl_lineset)


        zfs_list=[]
        zfs_info = root['version']
        zfs_info['zfs_name'] = self.zfs['name']
        zfs_info['zfs_ip'] = self.zfs['ip']
        zfs_info['fbrm_date'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
        zfs_list.append(zfs_info)

        print zfs_info
        urn = zfs_info['urn']
        urn = urn.split(':')[-1]
        zfs_info['urn'] = urn

        install_time = zfs_info['install_time']
        zfs_info['install_time'] = self.to_local_time(install_time)
        boot_time = zfs_info['boot_time']
        zfs_info['boot_time'] = self.to_local_time(boot_time)
        update_time = zfs_info['update_time']
        zfs_info['update_time'] = self.to_local_time(update_time)
        print 'update_time :', update_time
        print 'update_time :', self.to_local_time(update_time)
        self.db.dbInsertList(zfs_list, 'master.master_zfs_info')

    def set_pools(self,arg):
        lines = arg.split('-' * 30)[1]
        curl_lineset = lines[lines.index('{') - 1:]
        root = json.loads(curl_lineset)

        zfs_list = []
        
        if 'fault' not in root.keys():
            zfs_info = root['pools']
            for zfs in zfs_info:
                print zfs
                if zfs['status'] == 'online':
                    zfs_list.append(zfs['href'])

        print zfs_list

    def set_projects(self,arg):
        lines = arg.split('-' * 30)[1]
        curl_lineset = lines[lines.index('{') - 1:]
        root = json.loads(curl_lineset)
        if 'fault' not in root.keys():
            zfs_info = root['projects']
            print zfs_info

    def get_data_file(self):
        path = self.cfg.get('common', 'fbrm_path')
        data_path = os.path.join(path, 'data')
        evt_data_path = os.path.join(path, 'data', 'FBRM_ZFS_CURL')
        file_list = glob.glob(os.path.join(evt_data_path, '*'))
        return file_list


    def set_mster_serial(self):
        query ="""
        select asn,peer_asn from master.master_zfs_cluster
        """

        ret=self.db.queryExec(query)
        for row in ret:
            print row[0],row[1]


    def main(self):
        self.zfs={}
        pool_linkes=[]
        pool_files  = self.get_data_file()
        print pool_files
        for file in pool_files:
            print file
            ip = file.split('_')[-1]
            ip = ip.replace('.txt','')
            self.zfs['name'] = 'UZFS01'
            self.zfs['ip'] = ip

            with open(file) as f:
                readset = f.read()
            # print readset
            for arg in readset.split('curl --'):




                # if 'v1/version' in  arg[:100]:
                #     self.set_sysver(arg)
                linesp = arg.split()
                if len(linesp) > 4:


                    if '/v1/pools' == linesp[4][-9:]:
                        pool_linkes=self.set_pools(arg)


                    print pool_linkes
                    # print linesp[4][-9:]
                    # if '/projects' == linesp[4][-9:]:
                    #     self.set_projects(arg)

                if 'logs/fault' in  arg[:100]:
                    self.set_fault(arg)
                if 'logs/system' in  arg[:100]:
                    self.set_system(arg)
                if 'logs/alert' in  arg[:100]:
                    self.set_alert(arg)





if __name__=='__main__':
    zfs_curl_pool().main()

