import ConfigParser
import datetime
import glob
import json
import os
import sys

import fbrm_dbms

event_files=glob.glob(os.path.join('data','event*.txt'))

class zfs_curl_pool():
    def __init__(self):
        self.cfg= self.get_cfg()
        self.today = datetime.datetime.now()
        self.check_date = self.today.strftime('%Y-%m-%d %H:%M:%S')
        self.db= fbrm_dbms.fbrm_db()
        self.fbrm_datetime = self.today.strftime('%Y-%m-%d %H:%M:%S')

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
        # zfs_info['cluster_ip'] = self.zfs['ip']
        zfs_info['fbrm_date'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
        zfs_list.append(zfs_info)


        urn = zfs_info['urn']
        urn = urn.split(':')[-1]
        zfs_info['urn'] = urn

        install_time = zfs_info['install_time']
        zfs_info['install_time'] = self.to_local_time(install_time)
        boot_time = zfs_info['boot_time']
        zfs_info['boot_time'] = self.to_local_time(boot_time)
        update_time = zfs_info['update_time']
        zfs_info['update_time'] = self.to_local_time(update_time)
        self.db.dbInsertList(zfs_list, 'master.master_zfs_info')

    # def set_pools(self,arg):
    #     lines = arg.split('-' * 30)[1]
    #     curl_lineset = lines[lines.index('{') - 1:]
    #     root = json.loads(curl_lineset)
    #
    #     zfs_list = []
    #
    #     if 'fault' not in root.keys():
    #         zfs_info = root['pools']
    #         for zfs in zfs_info:
    #
    #             if zfs['status'] == 'online':
    #                 zfs_list.append(zfs['href'])



    def set_projects(self,root):
        prj_dict_list = []
        for prj in root['projects']:
            print prj
            prj_dict = {}

            prj['zfs_name'] = self.zfs['name']
            prj['node_name'] = self.zfs['name']
            prj['cluster_name'] = self.i_cluster_name
            prj['zfs_ip'] = self.zfs['ip']
            prj['asn'] = self.asn
            prj['cluster_ip'] = self.zfs['ip']
            prj['space_data'] = str(int(prj['space_data']))
            prj['space_total'] = str(int(prj['space_total']))
            prj['space_available'] = str(int(prj['space_available']))
            prj['space_snapshots'] = str(int(prj['space_snapshots']))
            prj['fbrm_date'] = self.today.strftime('%Y-%m-%d')
            prj['ins_date_time'] = self.today.strftime('%Y-%m-%d %H-%M-%S')
            create_str = prj['creation']
            "20200319T06:47:06"
            create_date = datetime.datetime.strptime(create_str, "%Y%m%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            prj['creation'] = create_date
            prj['source'] = str(prj['source'])
            prj_dict_list.append(prj)
            print prj.keys()
        tb = 'live.live_zfs_projects'
        self.db.dbInsertList(prj_dict_list, tb)
        store_prj_dict_list = self.set_store_list(prj_dict_list)
        tb = 'store.store_day_zfs_projects'
        self.db.dbInsertList(store_prj_dict_list, tb)

    def get_data_file(self):
        path = self.cfg.get('common', 'fbrm_path')
        data_path = os.path.join(path, 'data')
        evt_data_path = os.path.join(path, 'data', 'FBRM_ZFS_CURL')
        file_list = glob.glob(os.path.join(evt_data_path, '*'))
        return file_list

    def to_local_time(self,utc):
        """
        Thu Nov 15 2018 23:10:39 GMT+0000 (UTC)
        :param utc:
        :return:
        Thu Nov 15 2018 23:10:39 GMT+0000 (UTC)
        """
        utc_time = datetime.datetime.strptime(utc,"%a %b %d %Y %H:%M:%S GMT+0000 (UTC)")
        local_time = utc_time + datetime.timedelta(hours=9)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def set_system(self,root):

        zfs_list=[]
        zfs_info = root['version']

        zfs_info['zfs_name'] = self.zfs['name']
        zfs_info['zfs_ip'] = self.zfs['ip']
        zfs_info['fbrm_date'] = self.today.strftime('%Y-%m-%d %H:%M:%S')


        urn = zfs_info['urn']
        urn = urn.split(':')[-1]
        zfs_info['urn'] = urn

        install_time = zfs_info['install_time']
        zfs_info['install_time'] = self.to_local_time(install_time)
        boot_time = zfs_info['boot_time']
        zfs_info['boot_time'] = self.to_local_time(boot_time)
        update_time = zfs_info['update_time']
        zfs_info['update_time'] = self.to_local_time(update_time)
        zfs_list.append(zfs_info)
        self.db.dbInsertList(zfs_list, 'master.master_zfs_info')
        self.asn = zfs_info['asn']
        self.i_cluster_name,self.cluster_name = self.db.get_zfs_name_from_asn(self.asn)
        self.cluster_name = zfs_info['nodename']


    def get_zfsname(self,readset):
        zfsname,zfs_ip = '',''
        for i in range(len(readset)):
            line = readset[i]
            if '###***zfsname***###' in line:
                zfsname = readset[i+1].strip()
            if '###***zfs_ip***###' in line:
                zfs_ip = readset[i+1].strip()
                break

        return zfsname,zfs_ip

    def set_cluster(self,root):
        cluster_list=[]
        resource_list=[]
        print 'root :',root
        cluster_dict = {}
        cluster_dict['asn'] = self.asn
        cluster_dict['cluster_name'] = self.i_cluster_name

        cluster_dict['node_name'] = self.cluster_name
        cluster_dict['fbrm_date'] = self.fbrm_datetime



        for cluster in root['cluster']:

            print 'cluster ::::',cluster

            
            if not cluster == 'resources':
                val = root['cluster'][cluster]
            
                if "'" in val :
                    val=val.replace("'","`")
                if "[" in val:
                    val=','.join(list(val))
                print 'key val :'  ,cluster,  val

                # query = "select zfs_name from master.master_zfs_info where asn in ('{}','{}') """.format (self.asn,cluster['peer_asn'])
                cluster_dict[cluster] = str(val)
                print cluster_dict
            else:

                resource_dict = {}
                resouces  = root['cluster'][cluster]

                for resource in resouces:
                    print resource.keys()
                    print resource.values()

                    res_dict = {}
                    res_dict['asn'] = self.asn
                    for key in resource.keys():
                        val = resource[key]
                        if "'" in val:
                            val=val.replace("'","`")
                        if type(val) == type([]):
                            val = ','.join(val)

                        res_dict[key] = val
                        res_dict['fbrm_date'] = self.fbrm_datetime
                    resource_list.append(res_dict)
        print cluster_dict
        cluster_list.append(cluster_dict)
        print cluster_list
        print resource_list
        db_name = 'master.master_zfs_cluster'
        self.db.dbInsertList(cluster_list, db_name)
        db_name = 'master.master_zfs_cluster_resouces'
        self.db.dbInsertList(resource_list, db_name)


    def set_interfaces(self,root):
        zfs_network_interfaces=[]
        for val in root['interfaces']:
            print val['v4addrs']
            service_ip = {}
            for v4addr in val['v4addrs']:
                service_ip['zfs_name'] = self.zfs['name']
                service_ip['node_name'] = self.cluster_name
                service_ip['zfs_default_ip'] = self.zfs['ip']

                print v4addr

                if '/' in v4addr:
                    zfs_service_ip = v4addr.split('/')[0]
                else:
                    zfs_service_ip = v4addr
                service_ip['zfs_service_ip'] = zfs_service_ip
                service_ip['fbrm_date'] = self.today.strftime('%Y-%m-%d')
                # service_ip['cluster_serial'] = self.asn

                service_ip['zfs_cluster'] = self.asn
                zfs_network_interfaces.append(service_ip)


        tb_name = 'live.live_zfs_network_interfaces'
        self.db.dbInsertList(zfs_network_interfaces, tb_name)


    def set_store_list(self,live_list):
        store_list = []
        for item in live_list:
            item['store_date'] = item['fbrm_date']
            item['write_date'] = item['ins_date_time']
            store_list.append(item)
        return store_list



    def set_pools(self,root):
        pool_dict_list = []
        print root
        for pool in root['pools']:
            pool_dict = {}
            keys = pool.keys()
            vals = pool.values()
            u_keys, u_vals = [], []
            for i in range(len(keys)):
                key = keys[i]
                val = vals[i]
                if key == 'usage':
                    # print pool['usage']
                    u_keys = pool['usage'].keys()
                    u_vals = pool['usage'].values()
                else:
                    pool_dict[key] = val

            for i in range(len(u_keys)):
                u_key = u_keys[i]
                u_val = u_vals[i]
                key = 'u_{}'.format(u_key)
                pool_dict[key] = str(int(u_val))


            pool_dict['cluster_ip'] = self.zfs['ip']
            pool_dict['zfs_ip'] = self.zfs['ip']
            pool_dict['fbrm_date'] = self.today.strftime('%Y-%m-%d')
            pool_dict['ins_date_time'] = self.today.strftime('%Y-%m-%d %H-%M-%S')


            pool_dict['zfs_name'] = self.cluster_name
            pool_dict['cluster_name'] = self.i_cluster_name
            pool_dict['node_name'] = self.zfs['name']
            print pool_dict
            pool_dict_list.append(pool_dict)

        tb = 'live.live_zfs_pools'
        self.db.dbInsertList(pool_dict_list, tb)
        store_pool_dict_list = self.set_store_list(pool_dict_list)
        tb = 'store.store_day_zfs_pools'
        self.db.dbInsertList(store_pool_dict_list, tb)

    def set_filesystems(self,root):
        print '#' * 50
        print 'FILESYSTEMS SET '
        print '#' * 50

        pool_fs_list = []
        for fs in root['filesystems']:
            print fs
            del fs['source']
            fs['zfs_name']= self.zfs['name']
            fs['node_name'] = self.zfs['name']
            fs['cluster_name'] = self.i_cluster_name
            fs['zfs_ip'] = self.zfs['ip']
            fs['cluster_ip'] = self.zfs['ip']
            fs['asn'] = self.asn
            fs['cluster_ip'] = self.zfs['ip']
            fs['space_total'] = str(int(fs['space_total']))
            fs['space_available'] = str(int(fs['space_available']))
            fs['space_data'] = str(int(fs['space_data']))
            fs['space_snapshots'] = str(int(fs['space_snapshots']))
            fs['fbrm_date'] =self.today.strftime('%Y-%m-%d')
            fs['ins_date_time'] = self.today.strftime('%Y-%m-%d %H-%M-%S')
            fs=self.set_str(fs)
            fs['root_acl'] = str(fs['root_acl'])

            del fs['root_acl']
            create_str = fs['creation']
            "20200319T06:47:06"
            create_date = datetime.datetime.strptime(create_str, "%Y%m%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            fs['creation'] = create_date

            # fs['root_acl'] = str("'{}'".format()['root_acl'])
            # print fs.keys()
            if 'origin' in fs.keys():
                origin = fs['origin']
                fs['origin_project'] = origin['project']
                fs['origin_share'] = origin['share']
                fs['origin_snapshot'] = origin['snapshot']
                fs['origin_pool'] = origin['pool']
                fs['origin_collection'] = origin['collection']
                del fs['origin']
            pool_fs_list.append(fs)


        tb= 'live.live_zfs_filesystems'
        self.db.dbInsertList(pool_fs_list, tb)

        store_fs_list = self.set_store_list(pool_fs_list)
        tb = 'store.store_day_zfs_filesystems'
        self.db.dbInsertList(store_fs_list, tb)

    def set_str(self,src_dict):
        keys=src_dict.keys()
        vals = src_dict.keys()
        for i in range(len(keys)):
            k=keys[i]
            v=vals[i]
            if type(v) == dict:
                src_dict[k] = str(v)
        return src_dict

    def set_chassis(self,root):
        print root
        cpu_list=[]
        disk_list=[]
        chassis = root['chassis']
        if type(chassis) == type([]):
            hardware_list=[]
            for chassis in chassis:
                keys = chassis.keys()
                print chassis.values()
                chassis['asn'] = self.asn
                url = chassis['href']
                chassis_name = os.path.basename(url)
                dict = {}
                dict['asn'] = self.asn
                dict['chassis_name'] = chassis_name
                dict['name'] = chassis['name']
                dict['model'] = chassis['model']
                dict['type'] = chassis['type']
                dict['serial'] = chassis['serial']
                dict['manufacturer'] = chassis['manufacturer']
                dict['fbrm_datetime'] = self.fbrm_datetime
                if 'rpm' in keys :
                    dict['rpm'] = chassis['rpm']
                if 'part' in keys :
                    dict['part'] = chassis['part']
                if 'path' in keys :
                    dict['path'] = chassis['path']
                if 'revision' in keys :
                    dict['revision'] = chassis['revision']
                hardware_list.append(dict)

            db_name = 'master.master_zfs_hardware'
            self.db.dbInsertList(hardware_list, db_name)

        else:
            keys= chassis.keys()
            url = chassis['href']
            chassis_name = os.path.basename(url)
            if 'cpu' in keys:
                for cpus in chassis['cpu']:
                    print cpus.keys()
                    # ['faulted', 'name', 'cpu', 'href', 'model', 'disk', 'type', 'serial', 'manufacturer']
                    print cpus.values()
                    # ['faulted', 'label', 'href', 'cores', 'model', 'speed', 'present', 'manufacturer']

                    cpus['asn'] = self.asn
                    cpus['chassis_name'] = chassis_name
                    cpus['name'] = chassis['name']
                    cpus['cpu_speed'] = str(cpus['speed'])
                    cpus['cores'] = str(cpus['cores'])
                    del (cpus['speed'])
                    cpus['fbrm_datetime'] = self.fbrm_datetime
                    cpu_list.append(cpus)
            if 'disk' in keys:
                for disk in chassis['disk']:

                    # print disk.keys()
                    # print disk.values()
                    if 'use' in disk.keys():
                        disk['disk_use'] = disk['use']
                        del (disk['use'])
                    else:
                        disk['disk_use'] = ''
                    disk['asn'] = self.asn
                    disk['chassis_name'] = chassis_name
                    disk['name'] = chassis['name']
                    if 'size' in  disk.keys():
                        disk['size'] = str(disk['size'])

                    disk['fbrm_datetime'] = self.fbrm_datetime
                    print disk
                    disk_list.append(disk)


            # query = "delete from master.master_zfs_hardware_cpus where chassis_name = '{}'".format(chassis_name)
            # print query
            # self.db.queryExec(query)

            db_name = 'master.master_zfs_hardware_cpus'
            self.db.dbInsertList(cpu_list, db_name)

            # query = "delete from master.master_zfs_hardware_disks where chassis_name = '{}'".format(chassis_name)
            # self.db.queryExec(query)

            db_name = 'master.master_zfs_hardware_disks'
            self.db.dbInsertList(disk_list, db_name)





    def main(self):
        self.zfs={}
        pool_linkes=[]
        pool_files  = self.get_data_file()

        for file in pool_files:
            # print file
            ip = file.split('_')[-1]
            ip = ip.replace('.txt','')


            with open(file) as f:
                readset = f.read()
            # print readset
            zfs_name,zfs_ip=self.get_zfsname(readset.splitlines())
            print zfs_name,zfs_ip
            self.zfs['name'] = zfs_name
            self.zfs['ip'] = zfs_ip
            for arg in readset.split('curl --'):


                if '--------------------------------------------------' in arg:
                    arg = arg.replace('--------------------------------------------------','')
                if '############' in arg:
                    arg=arg.split('############')[1]

                if '{' in arg:
                    curl_lineset = arg[arg.index('{') - 1:]
                    # print curl_lineset
                    print curl_lineset
                    root = json.loads(curl_lineset)
                    key= root.keys()[0]
                    print 'key :',key
                    if key=='version':
                        self.set_system(root)
                    if key == 'cluster':
                        self.set_cluster(root)
                    if key =='interfaces':
                        self.set_interfaces(root)
                    if key =='pools':
                        self.set_pools(root)
                    if key =='projects':
                        self.set_projects(root)
                    if key == 'filesystems':
                        self.set_filesystems(root)

                    print '-'*50
                    if key == 'chassis':
                        self.set_chassis(root)


if __name__=='__main__':
    zfs_curl_pool().main()

