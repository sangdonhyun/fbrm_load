import fbrm_dbms



class ora_nsf():
    def __init__(self):
        self.db=fbrm_dbms.fbrm_db()


    def main(self):
        query = "select * from live.live_zfs_network_interfaces"
        retset = self.db.get_row(query)
        print retset



        query = "select * from live.live_zfs_server_hosts"
        retset = self.db.get_row(query)
        print retset

        query = "select * from live.live_svr_nfs_mounted_on where server_hostname='fora_01'"
        retset=self.db.get_row(query)

        for ret in retset:
            mf= ret[5]
            fs= ret[6]

            if ':' in mf:
                zfs=mf.split(':')[0]
                dir=mf.split(':')[1]
            print zfs,dir,fs


        query = "select * from live.live_zfs"

    def get_zfs(self,dir):
        dir='/ZFS/BACKUP/DATA_UPGR_01'
        query ="select zfs_name,zfs_ip from live.live_svr_nfs_mounted_on where mounted='{dir}'".format(dir=dir)
        print query
        retset = self.db.get_row(query)
        print retset

if __name__=='__main__':
    dir = '/ZFS/BACKUP/DATA_UPGR_01'
    ora_nsf().get_zfs(dir)