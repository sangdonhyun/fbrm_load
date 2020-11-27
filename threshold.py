import os
import sys
import fbrm_dbms
import datetime

class threshold():
    def __init__(self):
        self.db=fbrm_dbms.fbrm_db()
        self.now = datetime.datetime.now()


    def get_common_threshold(self):
        query = "select * from ref.ref_threshold where device_type = 'common'"
        ret = self.db.getRaw(query)

        return ret


    def get_cluster(self,asn):
        cluster_name,cluster_ip = '',''
        query = "select cluster_name from master.master_zfs_cluster where asn = '{}'".format(asn)
        ret =self.db.getRaw(query)[0][0]
        if not ret == '' :
            cluster_name= self.db.getRaw(query)[0][0]

        query = "select zfs_default_ip from live.live_zfs_network_interfaces where zfs_cluster = '{}' limit 1".format(asn)
        ret = self.db.getRaw(query)[0][0]
        if not ret == '':
            cluster_ip = self.db.getRaw(query)[0][0]

        return cluster_name,cluster_ip

    def set_pool(self,threshold):
        print threshold
        query = "select asn,u_total,u_usage_total,name from live.live_zfs_pools where status = 'online'"
        ret = self.db.getRaw(query)

        event_list=[]

        for pools in ret:

            rate= round(pools[2]/pools[1] * 100,2)

            if rate > threshold[3]:
                cluster_name, cluster_ip = self.get_cluster(pools[0])
                # print threshold
                # print pools
                # print rate
                # print cluster_name,cluster_ip

                total = round(pools[1]/1024/1024/1024,2)
                used = round(pools[2]/1024/1024/1024,2)

                msg='[pool threshold alram] cluster : {cluster_name}({cluster_ip}), Pool name :{pool_name}, total:{total}GB, used : {used}GB , usage rage : {usage_rate}%, threshold : {threshold}%'.format(cluster_name=cluster_name,cluster_ip=cluster_ip,pool_name=pools[3],total=total,used=used,usage_rate=rate,threshold=threshold[3])
                print msg
                event={}
                event['log_date']= self.now.strftime('%Y-%m-%d')
                event['check_date'] = self.now.strftime('%Y-%m-%d %H:%M:%S')
                event['check_category']='threshold pool'
                event['event_date']=self.now.strftime('%Y-%m-%d %H:%M:%S')
                event['serial_number'] = pools[0]
                event['event_code'] = 'th_pool'
                event['event_level'] = threshold[4]
                event['desc_detail'] = msg
                event['device_type'] = 'ZFS POOL'
                event['vendor_name'] = 'Oracle'
                query = "select count(*) from event.noti_info_log where log_date ='{}' and desc_detail = '{}'".format(self.now.strftime('%Y-%m-%d'),msg)
                ret=self.db.getRaw(query)[0][0]
                if ret == 0:
                    event_list.append(event)


        db_name = 'event.noti_info_log'
        self.db.dbInsertList(event_list,db_name)

    def set_nfs(self,threshold):
        print threshold
        query = "select check_date_time,server_hostname,server_ip,filesystem,zfs_name,mounted_bit,ussage_used_capacity,zfs_cluster  FROM live.live_svr_nfs_mounted_on;"
        ret=self.db.getRaw(query)
        event_list=[]
        for nfs in ret:

            event_date = nfs[0]
            server_name = nfs[1]
            server_ip  = nfs[0]
            fs_name = nfs[3]
            zfs_name = nfs[4]
            mounted_bit = nfs[5]

            if not  bool(mounted_bit) == True:
                print mounted_bit
                mounted_info={}
                mounted_info['event_date']=event_date

                mounted_info['server_ip'] = nfs[0]
                mounted_info['fs_name'] = nfs[3]
                mounted_info['server_name'] =  server_name
                self.set_nfs_mount(mounted_info)
            usage_rate = nfs[6]
            if '%' in usage_rate :
                usage_rate = usage_rate.replace('%','')
            usage_rate = round(float(usage_rate),2)
            if usage_rate > threshold[3]:
                serial = nfs[7]
                msg="[nfs threshold alram] {} {} usage_rate {}% (threshold:{}%) ".format(server_name,fs_name,usage_rate,threshold[3])
                event = {}
                event['log_date'] = self.now.strftime('%Y-%m-%d')
                event['check_date'] = self.now.strftime('%Y-%m-%d %H:%M:%S')
                event['check_category'] = 'threshold pool'
                event['event_date'] = event_date
                event['serial_number'] = serial
                event['event_code'] = 'th_nfs'
                event['event_level'] = threshold[4]
                event['desc_detail'] = msg
                event['device_type'] = 'NFS'
                event['vendor_name'] = 'Oracle'
                query = "select count(*) from event.noti_info_log where log_date ='{}' and desc_detail = '{}'".format(
                    self.now.strftime('%Y-%m-%d'), msg)
                ret = self.db.getRaw(query)[0][0]
                if ret == 0:
                    event_list.append(event)

        db_name = 'event.noti_info_log'
        self.db.dbInsertList(event_list, db_name)


    def set_nfs_mount(self,mounted_info):
        msg='[nfs mount alarm] {}({}) {} NFS file system mount fail '.format(mounted_info['server_name'],mounted_info['server_ip'],mounted_info['fs_name'])
        event={}
        event['log_date'] = self.now.strftime('%Y-%m-%d')
        event['check_date'] = self.now.strftime('%Y-%m-%d %H:%M:%S')
        event['check_category'] = 'nfs mount'
        event['event_date'] = mounted_info['event_date']
        event['serial_number'] = mounted_info['server_ip']
        event['event_code'] = 'nfs_mount'
        event['event_level'] = 'warnning'
        event['desc_detail'] = msg
        event['device_type'] = 'NFS MOUNT'
        event['vendor_name'] = 'iBRM'
        event_list=[event]
        query = "select count(*) from event.noti_info_log where log_date ='{}' and desc_detail = '{}'".format(
        self.now.strftime('%Y-%m-%d'), msg)
        ret = self.db.getRaw(query)[0][0]
        if ret == 0:
            event_list.append(event)
            db_name = 'event.noti_info_log'
            self.db.dbInsertList(event_list, db_name)

    def main(self):
        threshold_list=self.get_common_threshold()

        if not  threshold_list == []:
            for threshold in threshold_list:
                print threshold
                type=  threshold[1]
                if type == 'pool':
                    self.set_pool(threshold)
                if type == 'nfs' :
                    self.set_nfs(threshold)

if __name__=='__main__':
    threshold().main()
