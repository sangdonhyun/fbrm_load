import os
import sys
import ConfigParser
import fbrm_dbms

class evt_threshold():
    def __init__(self):
        self.db=fbrm_dbms.fbrm_db()
        self.cfg = self.get_cfg()
        self.threscfg = self.get_threshold_cfg()

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfg_file = os.path.join('config', 'config.cfg')
        cfg.read(cfg_file)
        return cfg

    def get_threshold_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfg_file = os.path.join('config', 'threshold.cfg')
        cfg.read(cfg_file)
        return cfg


    def get_threshold(self,key):
        threshold = {}
        for opt in self.threscfg.options(key):
            threshold[opt] = self.threscfg.get(key,opt)
        return threshold


    def pool_threshold(self):
        query = "select * from live.live_zfs_pools "
        print self.db.get_row(query)
    def main(self):
        for key in self.threscfg.sections():
            print key
            if key=='pool':
                self.pool_threshold()
            print self.get_threshold(key)



if __name__ == '__main__':
    evt_threshold().main()