#-*- coding:utf-8 -*-

import os
import ConfigParser
import glob
import datetime

class job_sched():
    def __init__(self):
        self.cfg = self.get_cfg()
        self.tot_cnt = 0

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfg_file = os.path.join('config','config.cfg')
        cfg.read(cfg_file)
        return cfg

    def data_files(self):
        fbrm_path=self.cfg.get('common','fbrm_path')
        clist=glob.glob(os.path.join(fbrm_path,'data','FBRM_ORA_CLONTAB','*.tmp'))
        return clist

    def get_hostname(self,lineset):
        hostname = lineset.strip()
        return hostname



    def get_cnt(self,cron_sched):
        cnt = 0
        min, hour, day, mon, week = cron_sched
        to_week=datetime.datetime.now().weekday() + 1
        if datetime.datetime.now().weekday() == 6:
            to_week = 0


        to_mon = 0
        to_mon = 0

        print min, hour, day, mon, week
        if ',' in min :
            min_cnt = len(min.split(','))
        elif '/' in min:
            aa = min.split('/')[1]
            min_cnt = 60/int(aa)
        else:
            min_cnt = 1

        if ',' in hour :
            hour_cnt = len(hour.split(','))
            # print 'hour_cnt' ,hour_cnt,hour,',' in hour
        elif '/' in min:
            aa = hour.split('/')[1]
            hour_cnt = 60/int(aa)
        else:
            hour_cnt = 1
        if week == '*':
            cnt = min_cnt * hour_cnt
            self.tot_cnt = self.tot_cnt + cnt
        else:
            if '-' in week:
                start=week[0]
                end = week[-1]
                range_week= range(int(start),int(end)+1)
                if to_week in range_week:
                    cnt = min_cnt * hour_cnt
                    self.tot_cnt = self.tot_cnt + cnt
            else:
                if to_week == int(week):
                    cnt = min_cnt * hour_cnt
                    self.tot_cnt = self.tot_cnt + cnt



        print 'min_cnt :',min_cnt
        print 'hour_cnt :', hour_cnt
        print 'cnt :', cnt

        print '-'*50

    def get_clon_sched(self,ret):
        lineset=ret.splitlines()
        sched_list=[]
        for i in range(len(lineset)):
            line=lineset[i]
            if len(line) > 0:
                if not line[0] == '#':
                    if 'ZFS' in line:
                        sched_list.append(line)
        # print sched_list
        for sched in sched_list:
            self.get_cnt(sched.split()[:5])





    def fead(self,filename):
        with open(filename) as f:
            fead=f.read()
        lineset=fead.split('###***')
        print lineset
        for ret in lineset:
            if ret[:10] == 'hostname**':
                hostname=self.get_hostname(ret)
            if ret[:10] == 'crontab -l':
                self.get_clon_sched(ret)



    def main(self):

        """
            python datetime.datetime.now().weekday()
            요일
            반환(0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일)

        clontab
        * * * * *  수행할 명령어
        ┬ ┬ ┬ ┬ ┬
        │ │ │ │ │
        │ │ │ │ │
        │ │ │ │ └───────── 요일 (0 - 6) (0:일요일, 1:월요일, 2:화요일, …, 6:토요일)
        │ │ │ └───────── 월 (1 - 12)
        │ │ └───────── 일 (1 - 31)
        │ └───────── 시 (0 - 23)
        └───────── 분 (0 - 59)


        * * * * * 1440
        15,45 * * * *  48
        */10 * * * *    144
        0 2 * * * 1
        30 */6 * * * 4
        30 1-23/6 * * * 4  (01:30, 07:30, 13:30, 19:30)
        0 8 * * 1-5    평일(월요일~금요일) 08:00
        0 8 * * 0,6 주말(일요일, 토요일) 08:00
        """

        print datetime.datetime.now().weekday()
        clist=self.data_files()
        for c in clist:
            self.fead(c)
        print 'tot_cnt :',self.tot_cnt

if __name__=='__main__':
    job_sched().main()