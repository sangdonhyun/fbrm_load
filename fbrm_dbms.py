'''
Created on 2020. 4. 9.

@author: user
'''
# -*- encoding:utf-8*-
'''
Created on 2013. 2. 11.

@author: Administrator
'''

import sys
import os
import psycopg2
import ConfigParser
import codecs
import locale
#import common



class fbrm_db():
    def __init__(self):
#         self.com = common.Common()
#         self.dec = common.Decode()
#         self.logger = self.com.flog()
                
#         self.conn_string = "host='localhost' dbname='fleta' user='fletaAdmin' password='kes2719!'"
        self.conn_string = self.getConnStr()
#         print self.conn_string
        self.cfg = self.getCfg()
        
        
    
    def getCfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config','config.cfg')
        cfg.read(cfgFile)
        return cfg
    
    def getConnStr(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config','config.cfg')
        cfg.read(cfgFile)
        try:
            ip = cfg.get('database','ip')
        except:
            ip = 'localhost'
        try:
            user = cfg.get('database','user')
        except:
            user = 'fbrmuser'
        try:
            dbname = cfg.get('database','dbname')
        except:
            dbname = 'fbrm'
        try: 
            passwd = cfg.get('database','passwd')
        except:
            passwd = 'fbrmpass'
        
        
        if len(passwd)>20:
            try:
                passwd= self.dec.fdec(passwd)
            except:
                pass
        
        return "host='%s' dbname='%s' user='%s' password='%s'"%(ip,dbname,user,passwd)
        
    
    def getConnectInfo(self):
        dbinfo = {}
        for info in self.cfg.options('database'):
            val = self.cfg.get('database',info)
            if (info == 'passwd' or info == 'user') and len(val) >20:
                val - self.dec.fdec(val)
            dbinfo[info] = val
        return dbinfo
    
    def getNow(self):
        return self.com.getNow('%Y%m%d%H%M%S')
    
    
    def getHistMonth(self):
        return self.com.getNow('%Y%m%d')
    
    def queryExec(self,query):
        con = None
        try:
            con = psycopg2.connect(self.conn_string)
            cur = con.cursor()
            
            cur.execute(query)
            con.commit()
#             print "Number of rows updated: %d" % cur.rowcount
        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print 'Error %s' % e    
            sys.exit(1)
        finally:
            if con:
                con.close()


    def del_rman_category(self,del_list):
        db = psycopg2.connect(self.conn_string)
        cursor = db.cursor()

        for del_value  in del_list:
            db_key, session_key, session_recid, session_stamp = del_value
            query = "DELETE FROM live.live_rman_catalog where db_key ='{}' and session_key ='{}' and  session_recid= '{}' and  session_stamp ='{}' ".format(db_key, session_key, session_recid, session_stamp)
            # print query
            cursor.execute(query)

        cursor.close()
        db.close()

    def isEvnt(self,query):
    
        db=psycopg2.connect(self.conn_string)
        cursor = db.cursor()
        print 'query 2:',query
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if rows == None:
            self.com.sysOut('Empty result set from query')
        
                
        cursor.close()
        db.close()
        return rows[0]
    
    def evtInsert(self,insquery):
        con = None
        try:
             
            con = psycopg2.connect(self.conn_string)
            cur = con.cursor()
            
            cur.execute(insquery)
            con.commit()
            
#             print "Number of rows updated: %d" % cur.rowcount
               
        
        except psycopg2.DatabaseError, e:
            
            if con:
                con.rollback()
            
            print 'Error %s' % e    
            sys.exit(1)
            
            
        finally:
            
            if con:
                con.close()

    def qwrite(self,msg,wbit='a'):
        with open('query.txt',wbit) as f:
            f.write(msg+'\r\n')
    
    def isilonQuery(self,dicList,table='live_live_rman_catalog'):
        for dic in dicList:
            colList= dic.keys()
            valList= dic.values()
            colStr = '('
            for i in colList:
                colStr += "%s"%i +','
            if colStr[-1]==',':
                colStr = colStr[:-1]+')'
            val = ()
            for i in valList:
                
                val+=(i,)
            valStr = str(val)
            query = 'insert into %s %s values %s;'%(table,colStr,valStr)
    #         print query
            return query
        
    
    
    def getQList(self,dicList,table='monotir.pm_auto_isilon_info'):
        qList=[]
        for dic in dicList:
            colList= dic.keys()
            valList= dic.values()
            colStr = '('
            for i in colList:
                colStr += "%s"%i +','
            if colStr[-1]==',':
                colStr = colStr[:-1]+')'
            val = ()
            for i in valList:
                
                val+=(i,)
            valStr = str(val)
            query = 'insert into %s %s values %s;'%(table,colStr,valStr)
            qList.append(query)
        return qList
#         print query
    
    
    def dbInsertDicList(self,dicList,table='monotir.pm_auto_isilon_info'):
        qList=self.getQList(dicList, table)
        con = None
        
        
        
        try:
              
            con = psycopg2.connect(self.conn_string)
            cur = con.cursor()
            for q in qList:
                
                cur.execute(q)
            con.commit()
             
#             print "Number of rows updated: %d" % cur.rowcount
                
         
        except psycopg2.DatabaseError, e:
             
            if con:
                con.rollback()
             
            print 'Error %s' % e    
            sys.exit(1)
             
             
        finally:
             
            if con:
                con.close()
        

    def get_zfs_name_from_cluster_name(self,cluster_name):

        query = "select zfs_name from master.master_zfs_info where zfs_serial in (select zfs_serial from master.master_zfs_cluster where cluster_name = '{}')".format(
            cluster_name)
        zfs_name = self.get_row(query)[0][0]

        return zfs_name

    def get_zfs_name_from_asn(self,asn):

        query = "select zfs_name from master.master_zfs_info where zfs_serial in (select zfs_serial from master.master_zfs_cluster where asn = '{}')".format(
            asn)
        print query
        zfs_name = self.get_row(query)[0][0]

        query = "select cluster_name from master.master_zfs_cluster where asn = '{}'".format(asn)

        cluster_name = self.get_row(query)[0][0]
        return zfs_name,cluster_name

    def get_cluster_name_from_node(self,node_name):

        query = "select zfs_name from master.master_zfs_cluster where node_name  = '{}'".format(node_name)
        print query
        zfs_name = self.get_row(query)[0][0]
        return zfs_name
    
    def null_check(self,col):
        check_key=['SESSION_KEY','SESSION_RECID','SESSION_STAMP','INPUT_BYTES','OUTPUT_BYTES','STATUS_WEIGHT', 'OPTIMIZED_WEIGHT', 'INPUT_TYPE_WEIGHT', 'ELAPSED_SECONDS', 'COMPRESSION_RATIO','INPUT_BYTES_PER_SEC','OUTPUT_BYTES_PER_SEC']
        null_bit=False
        if col in check_key:
            null_bit=True
        return null_bit


    def db_master_insert(self,master_dict,table='master.master_ora_info'):
        colList = master_dict.keys()
        valList = master_dict.values()
        colStr = '('
        for i in colList:
            colStr += "\"%s\"" % i + ','
        if colStr[-1] == ',':
            colStr = colStr[:-1] + ')'
        val = ()
        val_list = []
        for val in valList:
            if type(val) == type('aa'):
                if "'" in val:
                    val = val.replace("'", "`")
            # print str(val)
            val_list.append(str(val))
        valStr = "','".join(val_list)
        # print valStr
        query = 'insert into %s %s values (\'%s\');' % (table, colStr, valStr)
        print query
        self.dbQeuryIns(query)

    def dbInsertList(self,dicList,table='fbrm.mon_rman_backup_list'):

        query_set=[]
        for dic in dicList:
            colList= dic.keys()
            valList= dic.values()
            colStr = '('
            for i in colList:
                colStr += "\"%s\""%i +','
            if colStr[-1]==',':
                colStr = colStr[:-1]+')'
            val = ()
            val_list=[]
            for val in valList:
                if type(val) == type('aa'):
                    if  "'" in val:
                        val = val.replace("'","`")
                # print str(val)
                val_list.append(str(val))
            valStr= "','".join(val_list)
            # print valStr
            query = 'insert into %s %s values (\'%s\');'%(table,colStr,valStr)

            # sys.exit()
            query_set.append(query)
        
        con = None
             
        try:

            con = psycopg2.connect(self.conn_string)
            cur = con.cursor()
            for query in query_set:
                # print '-'*30
                # print query
                cur.execute(query)
            con.commit()
             
#             print "Number of rows updated: %d" % cur.rowcount
                

        except psycopg2.DatabaseError, e:

            if con:
                con.rollback()

            print 'Error %s' % e
            sys.exit(1)
             
             
        finally:

            if con:
                con.close()
    
    def dbQeuryIns(self,query):
        con = None
        try:
             
            con = psycopg2.connect(self.conn_string)
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except psycopg2.DatabaseError, e:
            
            if con:
                con.rollback()
            
            print 'Error %s' % e    
#             sys.exit(1)
        finally:
            
            if con:
                con.close()

    def get_row(self,query_string):
        db = psycopg2.connect(self.conn_string)
        cursor = db.cursor()


        cursor.execute(query_string)
        rows = cursor.fetchall()

        if rows == None:
            self.com.sysOut('Empty result set from query')

        cursor.close()
        db.close()
        return rows

    def eventList(self):
        db=psycopg2.connect(self.conn_string)
        cursor = db.cursor()
        
        query_string = self.getQuery()
        cursor.execute(query_string)
        rows = cursor.fetchall()
        
        if rows == None:
            self.com.sysOut('Empty result set from query')
        
                
        cursor.close()
        db.close()
        return rows
    
    def getRaw(self,query_string):
        db=psycopg2.connect(self.conn_string)
        
        try:
            cursor = db.cursor()
            cursor.execute(query_string)
            rows = cursor.fetchall()
        
            
            cursor.close()
            db.close()
            
            return rows
        except:
            return []
    
    def insMany(self,insList,table):
        
        insdics = tuple(insList)
        db=psycopg2.connect(self.conn_string)
        
        try:
            cursor = db.cursor()
            query="""INSERT INTO monitor.%s (check_date, ctrl_unum, flag_nm, cols_nm, cols_value) VALUES (%s, %s, %s, %s, %s);"""%table
            cursor.executemany(query, insdics)
            
            db.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if db is not None:
                db.close()
    
    def isEvtByQeury(self,query):
       
       
        conn = None
        try:
             
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            
            
        except:
            print "I am unable to connect to the database."
        
        # If we are accessing the rows via column name instead of position we 
        # need to add the arguments to conn.cursor.
        
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute(query)
        except:
            pass
        #
        # Note that below we are accessing the row via the column name.
        try:
            rows = cur.fetchall()
    
            if rows[0][0] == 0:
                return True
            else:
                return False
        except:
            pass
    def store_pool(self):
        query = "select u_id,zfs_name,cluster_name from store.store_day_zfs_pools"
        rows = self.get_row(query)
        for row in rows:
            uid=row[0]
            cluster_name = row[2]
            print uid,cluster_name

if __name__ == '__main__':
    dic_list=[{'ora_is_rac': 'FALSE', 'inst_datetime': '2020-10-21 13:21:28', 'svr_hostname': 'ibrmsv01', 'svr_id': 8004, 'fbrm_datetime': '2020-10-21 13:21:28', 'db_name': 'ibrm', 'ora_sid': 'ibrm', 'svr_ip_v4': '121.170.193.200', 'ora_home': '/u01/app/oracle/product/18.0.0/dbhome_1'}]
    fbrm_db().dbInsertList(dic_list,'master.master_ora_info')
    #print fbrm_db().store_pool()
    
    
        