import os
import glob
import sys
import fbrm_dbms
import datetime
import ConfigParser
import re
import zipfile
import table_create
import time


class rman_backupfiles():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.db = fbrm_dbms.fbrm_db()
        self.today = datetime.datetime.now()
    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def now_rman_list(self):
        t_day = self.today.strftime('%Y-%m-%d')
        y_datetime=self.today - datetime.timedelta(days=1)


        y_day = y_datetime.strftime('%Y-%m-%d')

        query = "select  u_id,hostname,db_name,session_key,session_recid,session_stamp,start_date,start_time,input_type,db_key,output_bytes,status from live.live_rman_catalog where start_date in ('{}','{}') order by start_time desc".format(t_day,y_day)
        query = "select  u_id,hostname,db_name,session_key,session_recid,session_stamp,start_date,start_time,input_type,db_key,output_bytes,status from live.live_rman_catalog  order by start_time desc"
        rman_list = self.db.get_row(query)
        return rman_list


    def get_zfs_cluster(self,lineset,char_str):
        zfs_path_list=[]
        zfs_path_bit = False
        for line in lineset:
            #datafile
            if re.match('^%s'%char_str, line):
                # print line
                path = line[line.index('=') + 1:].strip()
                zfs_path = '/'.join(path.split('/')[:4])
                if not zfs_path_bit:
                    query = "select zfs_name,zfs_ip from live.live_svr_nfs_mounted_on where mounted='{}'".format(zfs_path)

                    retset=self.db.get_row(query)
                    if len(retset) >0 :
                        if retset not in zfs_path_list:
                            zfs_path_list.append(retset[0])
                            zfs_path_bit = True
                
        return zfs_path_list


    def get_log_file(self,log_files,start_time):
        start_time_h_m = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
        log_start_time = None
        log_file = None
        for lf in log_files:
            with open(lf) as f:
                lineset = f.readlines()[:20]

            for line in lineset:
                if 'Production on' in line:
                    log_start_time = line.split('Production on')[-1].strip()
            if not log_start_time == None:
                log_start_time = datetime.datetime.strptime(log_start_time, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M')
                # print 'log time :',start_time_h_m,log_start_time
                if start_time_h_m == log_start_time:
                    log_file = lf

                    break
        return log_file



    def main(self):
        fbrm_home = self.cfg.get('common','fbrm_path')
        log_path=os.path.join(fbrm_home,'data','FBRM_ORA_LOG')

        rman_list= self.now_rman_list()

        for rman_backup in rman_list:
            # print rman_backup
            u_id = rman_backup [0]
            hostname = rman_backup[1]
            db_name = rman_backup[2]
            # print db_name
            session_key = rman_backup[3]
            session_recid = rman_backup[4]
            session_stamp = rman_backup[5]
            start_date = rman_backup[6]
            start_time = rman_backup[7]
            input_type = rman_backup[8]
            db_key = rman_backup[9]
            output_bytes = rman_backup[10]
            status = rman_backup[11]
            # print db_name,input_type,start_time

            query = "select count(*) from live.live_ora_tablespace where instance_name = '{}'".format(db_name)
            query = "select count(*) from live.live_ora_tablespace where db_name = '{}'".format(db_name)
            # print query
            db_file_count=int(self.db.get_row(query)[0][0])

            # [rman]
            # log_date_format = '%Y_%m%d_%H'
            date_char = self.cfg.get('rman','log_date_format')

            day_char=datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S').strftime('%Y_%m%d_%H')
            # print day_char
            # print 'input_type :',input_type
            if db_name == 'GODB':
                day_char=datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S').strftime('%Y_%m%d_%H')

            if input_type == 'ARCHIVELOG':
                """
                godb01.ugenssnc.com_GODB_Archive_log_2020_0716_14.log
                """
                log_set= os.path.join(log_path,'*{}_{}*Archive*{}*'.format(hostname,db_name,day_char))

            else:
                log_set = os.path.join(log_path, '*{}_{}*Level*{}*'.format(hostname,db_name,day_char))
            dict_list=[]
            update_list=[]
            log_files=glob.glob(log_set)


            if len(log_files) == 1:

                log_file = log_files[0]
            elif len(log_files) > 1:
                log_file = self.get_log_file(log_files,start_time)

            else:
                dict = {}

                dict['db_key'] = db_key
                dict['db_name'] = db_name
                dict['session_key'] = session_key
                dict['session_recid'] = session_recid
                dict['session_stamp'] = session_stamp
                dict['log_progress_rate'] = 'unkown'
                dict['log_backup_level'] = 'unkown'
                dict['log_backup_files'] = ''
                dict['collect_time'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
                dict['backup_label'] = 'unkown'
                dict['rman_log'] = 'log file now found'
                if not db_name =='':
                    dict_list.append(dict)
                print 'log file not found ',rman_backup


            if os.path.isfile(log_file):
                level= os.path.basename(log_file).split('_')[-3]
                # print level,input_type
                if 'level1' in log_file.lower():
                    level ='Level1'
                if 'level0' in log_file.lower():
                    level ='Level0'
                if 'archive' in log_file.lower():
                    level ='Archivelog'
                print 'level :',level
                backup_cnt = 0
                with open(log_file) as f:
                    tmpset = f.read()
                    lineset = tmpset.splitlines()
                if level == 'Archivelog':
                    backup_label = 'ARCHIVE LOG'
                    for line in lineset:
                        if 'archived log file name' in line:
                            backup_cnt = backup_cnt + 1
                        progress_rate = backup_cnt
                    #target zfs update
                    target_zfs = self.get_zfs_cluster(lineset, 'datafile')
                    # print target_zfs
                    node_name, zfs_ip = '', ''
                    if not target_zfs == []:
                        if len(target_zfs[0]) > 0:
                            (node_name, zfs_ip) = target_zfs[0]
                        table_list=['live.live_rman_catalog','store.store_day_rman_catalog']

                        for table_name in table_list:
                            query = "select zfs_name from master.master_zfs_info where zfs_serial in (select zfs_serial from master.master_zfs_cluster where node_name = '{}')".format(node_name)
                            cluster_name = self.db.get_row(query)[0][0]
                            # print query
                            # print zfs_name
                            query = "select asn from master.master_zfs_cluster where  node_name = '{}'".format(node_name)
                            asn = self.db.get_row(query)[0][0]

                            query = """
                            UPDATE {table_name}
                            SET zfs_name='{cluster_name}',cluster_name='{cluster_name}',node_name='{node_name}', zfs_ip='{zfs_ip}', asn='{asn}'
                            WHERE db_key='{db_key}' and  session_key='{session_key}' and session_stamp='{session_stamp}'
                            """.format(table_name=table_name, zfs_name=node_name,zfs_ip=zfs_ip, db_key=db_key,
                                       session_key=session_key, session_stamp=session_stamp,cluster_name=cluster_name,asn=asn,node_name=node_name)
                            # print query
                            self.db.queryExec(query)



                    # print zfs_name

                    query = "update ref.ref_rman_catalog set rman_log='{}' where db_key = '{}' and session_key='{}' and session_recid='{}' and session_stamp = '{}'".format(
                        tmpset, db_key, session_key, session_recid, session_stamp)
                    update_list.append(query)


                elif level == 'Level1':

                    if status not in ['FAILED' , 'COMPLETED WITH ERRORS'] :
                        if output_bytes == 0:
                            backup_label = 'DB INCR MERGY'
                        else:
                            backup_label = 'DB INCR LEVLE1'
                    else :
                        backup_label = status

                    for line in lineset:
                        if 'finished piece' in line:
                            backup_cnt = backup_cnt +1
                    if backup_cnt > db_file_count:
                        backup_cnt = db_file_count
                    progress_rate = (backup_cnt/db_file_count)*100

                    target_zfs = self.get_zfs_cluster(lineset, 'piece handle')
                    # print lineset

                    cluster_name, zfs_ip = '', ''

                    # print node_name,zfs_ip



                    if not target_zfs == []:
                        if len(target_zfs[0]) > 0:
                            (node_name, zfs_ip) = target_zfs[0]
                        table_list = ['live.live_rman_catalog', 'store.store_day_rman_catalog']

                        for table_name in table_list:
                            query = "select zfs_name from master.master_zfs_info where zfs_serial in (select zfs_serial from master.master_zfs_cluster where node_name = '{}')".format(node_name)
                            cluster_name=self.db.get_row(query)[0][0]
                            print query
                            # print node_name

                            query = """
                            UPDATE {table_name}
                            SET zfs_name='{zfs_name}',cluster_name='{cluster_name}',node_name='{node_name}', zfs_ip='{zfs_ip}', asn='{asn}'
                            WHERE db_name='{db_name}' and  session_key='{session_key}' and session_stamp='{session_stamp}'
                            """.format(table_name=table_name, zfs_name=node_name,
                                       zfs_ip=zfs_ip, db_name=db_name,
                                       session_key=session_key, session_stamp=session_stamp,cluster_name=cluster_name,asn=asn,node_name=node_name)

                            print query
                            self.db.queryExec(query)

                        query = "update ref.ref_rman_catalog set rman_log='{}' where db_key = '{}' and session_key='{}' and session_recid='{}' and session_stamp = '{}'".format(
                            tmpset, db_key, session_key, session_recid, session_stamp)
                        # print query
                        update_list.append(query)


                elif level == 'Level0' :
                    backup_label = 'DB INCR LEVLEL0'
                    for line in lineset:
                        if 'datafile copy complete' in line:
                            backup_cnt = backup_cnt + 1
                    if backup_cnt > db_file_count:
                        backup_cnt = db_file_count
                    progress_rate = (backup_cnt / db_file_count) * 100
                    query = "update ref.ref_rman_catalog set rman_log='{}' where db_key = '{}' and session_key='{}' and session_recid='{}' and session_stamp = '{}'".format(
                        tmpset, db_key, session_key, session_recid, session_stamp)
                    update_list.append(query)


                else:
                    level = 'unkown'
                # print 'backup_cnt :',level,backup_cnt,progress_rate

                dict = {}
                dict['db_key'] = db_key
                dict['session_key'] = session_key
                dict['session_recid'] = session_recid
                dict['session_stamp'] = session_stamp
                dict['log_progress_rate'] = progress_rate
                dict['log_backup_level'] = level
                dict['log_backup_files'] = backup_cnt
                dict['collect_time'] = self.today.strftime('%Y-%m-%d %H:%M:%S')
                dict['backup_label'] = backup_label
                # dict['rman_log'] = tmpset
                dict_list.append(dict)

                # query = "select zfs_name from master.master_zfs_info where zfs_serial in (select zfs_serial from master.master_zfs_cluster where cluster_name = '{}')".format(zfs_name)
                # zfs_name=self.db.get_row(query)[0][0]
                # query = "update live.live_rman_catalog set zfs_name='{}',cluster_name,zfs_ip='{}' where db_key = '{}' and session_key='{}' and session_recid='{}' and session_stamp = '{}'".format(
                #     zfs_name, zfs_ip, tmpset, db_key, session_key, session_recid, session_stamp)
                # print query
                # update_list.append(query)
                # if dict['status'] not in ['COMPLETED','RUNNING'] :


            table_name = 'ref.ref_rman_catalog'
            self.db.dbInsertList(dict_list,table_name)
            for query in update_list:
                self.db.queryExec(query)






if __name__=='__main__':
    rman_backupfiles().main()