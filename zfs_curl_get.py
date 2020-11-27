import sys
import os
import ConfigParser
import json
import socketClient
import common

class curl_get():
    def __init__(self):
        self.com = common.Common()


    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'config.cfg')
        cfg.read(cfgFile)
        return cfg

    def get_list(self):
        zfs_list=[]
        cfg = ConfigParser.RawConfigParser()
        cfgFile = os.path.join('config', 'zfs_list.cfg')
        cfg.read(cfgFile)
        for sec in cfg.sections():
            zfs={}
            zfs['name'] = sec
            for opt in cfg.options(sec):
                zfs[opt] = cfg.get(sec,opt)
            zfs_list.append(zfs)
        return zfs_list


    def get_project_url(self,zfs):
        ip = zfs['ip']
        user = zfs['user']
        passwd = zfs['passwd']
        port = zfs['port']
        cmd_list="""curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool1/projects
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool2/projects
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool1/projects/UPGR/filesystems
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool1/projects/CDB2/filesystems
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool1/projects/ORCL/filesystems
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool1/projects/default/filesystems
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool2/projects/UPGR/filesystems
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool2/projects/CDB2/filesystems
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool2/projects/ORCL/filesystems
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools/Pool2/projects/default/filesystems
""".format(IP=ip,user=user,passwd=passwd,port=port)

    def get_curl_list(self,zfs):
        ip = zfs['ip']
        user = zfs['user']
        passwd = zfs['passwd']
        port = zfs['port']
        lineset = """curl --user {user}:{passwd} -k -i https://{IP}:{port}
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/system/v1/version
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/hardware/v1/cluster
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/network/v1/interfaces
curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/storage/v1/pools""".format(IP=ip,user=user,passwd=passwd,port=port)
        return lineset.splitlines()


    def get_chassis(self,zfs):
        """
        curl --user root:welcome1 -k -i https://192.168.0.185:215/api/hardware/v1/chassis
        :param zfs:
        :return:
        """
        ip = zfs['ip']
        user = zfs['user']
        passwd = zfs['passwd']
        port = zfs['port']
        cmd = "curl --user {user}:{passwd} -k -i https://{IP}:{port}/api/hardware/v1/chassis".format(IP=ip,user=user,passwd=passwd,port=port)
        ret=os.popen(cmd).read()
        print cmd
        print ret
        if '{' in ret:
            curl_lineset = ret[ret.index('{') - 1:]
            root = json.loads(curl_lineset)
            self.fwrite(cmd)
            self.fwrite(ret)
            for chassi in root['chassis']:
                url= chassi['href']
                print url
                cmd = "curl --user {user}:{passwd} -k -i https://{IP}:{port}{url}".format(IP=ip,user=user,passwd=passwd,port=port,url=url)
                print cmd
                self.fwrite(cmd)
                ret = os.popen(cmd).read()
                print ret
                self.fwrite(ret)

    def fwrite(self,msg,wbit='a'):
        with open(self.fname,wbit) as fw:
            fw.write('-'*50+'\n')
            fw.write(msg+'\n')

    def get_head_msg(self):
        msg='#'*50 +'\n'
        msg ='# ibrm zfs connnect () #'
        msg = msg + '#' * 50 + '\n'
        return msg


    def get_pools(self,ret):
        zfs_list=[]
        curl_lineset = ret[ret.index('{') - 1:]
        root = json.loads(curl_lineset)
        if 'pools' in root.keys():
            print root

            if 'fault' not in root.keys():
                zfs_info = root['pools']
                for zfs in zfs_info:
                    print zfs
                    if zfs['status'] == 'online':
                        zfs_list.append(zfs['href'])
        return zfs_list

    def get_projects(self,ret):
        prj_list=[]
        curl_lineset = ret[ret.index('{') - 1:]
        root = json.loads(curl_lineset)
        for project in root['projects']:
            if 'href' in project.keys():
                prj_list.append(project['href'])
        return prj_list



    def main(self):
        for zfs in self.get_list():
            self.fname = os.path.join('data','%s_%s.tmp'%(zfs['name'],zfs['ip']))
            self.fwrite(self.com.get_module_head_msg(s_hostname=zfs['name'],s_ip=zfs['ip']),'w')

            self.fwrite("###***zfsname***###\n"+zfs['name'])
            self.fwrite("###***zfs_ip***###\n" + zfs['ip'])
            print zfs
            cmd_list=self.get_curl_list(zfs)
            for cmd in cmd_list:

                print cmd
                ret=os.popen(cmd).read()
                self.fwrite(cmd)
                self.fwrite(ret)

                if '{' in ret:
                    p_list=self.get_pools(ret)
                    for p in p_list:
                        cmd ='curl --user {user}:{passwd} -k -i https://{IP}:{port}{URL}/projects'.format(user=zfs['user'],passwd=zfs['passwd'],IP=zfs['ip'],port=zfs['port'],URL=p)
                        print cmd
                        ret=os.popen(cmd).read()
                        print ret
                        self.fwrite(cmd)
                        self.fwrite(ret)
                        prj_list=self.get_projects(ret)
                        print prj_list
                        for prj in prj_list:
                            cmd = 'curl --user {user}:{passwd} -k -i https://{IP}:{port}{URL}/filesystems'.format(
                                user=zfs['user'], passwd=zfs['passwd'], IP=zfs['ip'], port=zfs['port'], URL=prj)
                            print cmd
                            ret = os.popen(cmd).read()
                            print ret
                            self.fwrite(cmd)
                            self.fwrite(ret)
                            cmd = 'curl --user {user}:{passwd} -k -i https://{IP}:{port}{URL}/filesystems/snapshots'.format(
                                user=zfs['user'], passwd=zfs['passwd'], IP=zfs['ip'], port=zfs['port'], URL=prj)
                            ret = os.popen(cmd).read()
                            print ret
                            self.fwrite(cmd)
                            self.fwrite(ret)

            self.get_chassis(zfs)
            self.fwrite(self.com.get_module_tail_msg())
            socketClient.SocketSender(FILENAME=self.fname,DIR='FBRM_ZFS_CURL',ENDCHECK='YES').main()



if __name__=='__main__':
    curl_get().main()