import os
import socketClient
ip_list=['192.168.0.184','192.168.0.185']



for ip in ip_list:
    lineset="""curl --user root:welcome1 -k -i https://{IP}:215
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool1/projects
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool2/projects
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool1/projects/UPGR/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool1/projects/CDB2/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool1/projects/ORCL/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool1/projects/default/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool2/projects/UPGR/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool2/projects/CDB2/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool2/projects/ORCL/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/storage/v1/pools/Pool2/projects/default/filesystems
    curl --user root:welcome1 -k -i https://{IP}:215/api/system/v1/version
    curl --user root:welcome1 -k -i https://{IP}:215/api/hardware/v1/cluster""".format(IP=ip)



    fname = 'pool_{IP}.txt'.format(IP=ip)
    with open(fname,'w') as fw:
        for line in lineset.splitlines():
            print line
            ret=os.popen(line).read()
            fw.write(line+'\n')
            fw.write('-'*30+'\n')
            fw.write(ret+'\n')
            fw.write('-' * 30 + '\n')

    socketClient.SocketSender(FILENAME=fname, DIR='FBRM_ZFS_CURL', ENDCHECK='NO').main()