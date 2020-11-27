str="""
C:\Python27\python.exe C:/Users/Administrator/PycharmProjects/FBRM/fbrm_lib/zfs_sysver.py
curl --user root:welcome1 -k -i https://192.168.56.105:215/api/system/v1/version
<type 'dict'>
{'fbrm_date': '2020-07-13 09:19:35', 'update_time': 'Thu Nov 15 2018 23:10:39 GMT+0000 (UTC)', 'href': '/api/system/v1/version', 'install_time': 'Thu Nov 15 2018 23:10:39 GMT+0000 (UTC)', 'csn': 'unknown', 'ak_version': 'ak/SUNW,ankimo@2013.06.05.8.0,1-1.34', 'os_version': 'SunOS 5.11 11.4.0.34.0 64-bit', 'version': '2013.06.05.8.0,1-1.34', 'bios_version': 'innotek GmbH (BIOS)VirtualBox (BIOS)12.01.2006', 'navagent': 'aksh', 'ak_release': 'OS8.8.0', 'product': 'Sun Storage 7000', 'http': 'Apache/2.4.34 (Unix)', 'nodename': 'ZFS-88', 'mkt_product': 'Oracle ZFS Storage VirtualBox', 'ssl': 'OpenSSL 1.0.2o-fips  27 Mar 2018', 'zfs_name': 'ZFS-88', 'boot_time': 'Tue Jun 30 2020 01:58:30 GMT+0000 (UTC)', 'sp_version': '-', 'asn': 'df0c6049-dfae-4022-8320-edc1b00b8d8c', 'navname': 'aksh 1.0', 'urn': 'urn:uuid:11da4018-a79e-11dd-a2a2-080020a9ed93', 'zfs_ip': '192.168.56.105', 'part': 'Oracle 000-0000'}
update_time : Thu Nov 15 2018 23:10:39 GMT+0000 (UTC)
update_time : 2018-11-16 08:10:39
('2020-07-13 09:19:35', '2018-11-16 08:10:39', '/api/system/v1/version', '2018-11-16 08:10:39', 'unknown', 'ak/SUNW,ankimo@2013.06.05.8.0,1-1.34', 'SunOS 5.11 11.4.0.34.0 64-bit', '2013.06.05.8.0,1-1.34', 'innotek GmbH (BIOS)VirtualBox (BIOS)12.01.2006', 'aksh', 'OS8.8.0', 'Sun Storage 7000', 'Apache/2.4.34 (Unix)', 'ZFS-88', 'Oracle ZFS Storage VirtualBox', 'OpenSSL 1.0.2o-fips  27 Mar 2018', 'ZFS-88', '2020-06-30 10:58:30', '-', 'df0c6049-dfae-4022-8320-edc1b00b8d8c', 'aksh 1.0', '11da4018-a79e-11dd-a2a2-080020a9ed93', '192.168.56.105', 'Oracle 000-0000')
insert into master.master_zfs_info ("fbrm_date","update_time","href","install_time","csn","ak_version","os_version","version","bios_version","navagent","ak_release","product","http","nodename","mkt_product","ssl","zfs_name","boot_time","sp_version","asn","navname","urn","zfs_ip","part") values ('2020-07-13 09:19:35', '2018-11-16 08:10:39', '/api/system/v1/version', '2018-11-16 08:10:39', 'unknown', 'ak/SUNW,ankimo@2013.06.05.8.0,1-1.34', 'SunOS 5.11 11.4.0.34.0 64-bit', '2013.06.05.8.0,1-1.34', 'innotek GmbH (BIOS)VirtualBox (BIOS)12.01.2006', 'aksh', 'OS8.8.0', 'Sun Storage 7000', 'Apache/2.4.34 (Unix)', 'ZFS-88', 'Oracle ZFS Storage VirtualBox', 'OpenSSL 1.0.2o-fips  27 Mar 2018', 'ZFS-88', '2020-06-30 10:58:30', '-', 'df0c6049-dfae-4022-8320-edc1b00b8d8c', 'aksh 1.0', '11da4018-a79e-11dd-a2a2-080020a9ed93', '192.168.56.105', 'Oracle 000-0000');
------------------------------
insert into master.master_zfs_info ("fbrm_date","update_time","href","install_time","csn","ak_version","os_version","version","bios_version","navagent","ak_release","product","http","nodename","mkt_product","ssl","zfs_name","boot_time","sp_version","asn","navname","urn","zfs_ip","part") values ('2020-07-13 09:19:35', '2018-11-16 08:10:39', '/api/system/v1/version', '2018-11-16 08:10:39', 'unknown', 'ak/SUNW,ankimo@2013.06.05.8.0,1-1.34', 'SunOS 5.11 11.4.0.34.0 64-bit', '2013.06.05.8.0,1-1.34', 'innotek GmbH (BIOS)VirtualBox (BIOS)12.01.2006', 'aksh', 'OS8.8.0', 'Sun Storage 7000', 'Apache/2.4.34 (Unix)', 'ZFS-88', 'Oracle ZFS Storage VirtualBox', 'OpenSSL 1.0.2o-fips  27 Mar 2018', 'ZFS-88', '2020-06-30 10:58:30', '-', 'df0c6049-dfae-4022-8320-edc1b00b8d8c', 'aksh 1.0', '11da4018-a79e-11dd-a2a2-080020a9ed93', '192.168.56.105', 'Oracle 000-0000');
##################################################
system asn
##################################################
asn : df0c6049-dfae-4022-8320-edc1b00b8d8c
curl --user root:welcome1 -k -i https://192.168.56.105:215/api/hardware/v1/cluster
HTTP/1.1 200 OK
Date: Mon, 13 Jul 2020 00:19:17 GMT
Server: TwistedWeb/10.1.0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: frame-ancestors 'self'
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Content-Length: 626
X-Zfssa-Version: ak/SUNW,ankimo@2013.06.05.8.0,1-1.34
X-Zfssa-Hardware-Api: 2.0
X-Zfssa-Api-Version: 2.0
Content-Type: application/json; charset=utf-8

{"cluster":
{
"state": "AKCS_UNCONFIGURED",
"description": "Clustering is not configured",
"peer_asn": "",
"peer_hostname": "",
"peer_state": "",
"peer_description": "",
"resources": [{"owner": "ZFS-88",
"type": "singleton",
"user_label": "Backup_LAN",
"details": ["192.168.56.105"],
"href": "/api/hardware/v1/cluster/resources/net/e1000g0"
},
{"owner": "ZFS-88",
"type": "singleton",
"user_label": "",
"details": ["29.3G"],
"href": "/api/hardware/v1/cluster/resources/zfs/Pool1"
},
{"owner": "ZFS-88",
"type": "singleton",
"user_label": "",
"details": ["29.3G"],
"href": "/api/hardware/v1/cluster/resources/zfs/Pool2"
}]}

}

{'cluster': {'description': 'Clustering is not configured', 'peer_state': '', 'state': 'AKCS_UNCONFIGURED', 'peer_description': '', 'peer_hostname': '', 'resources': [{'owner': 'ZFS-88', 'user_label': 'Backup_LAN', 'href': '/api/hardware/v1/cluster/resources/net/e1000g0', 'type': 'singleton', 'details': ['192.168.56.105']}, {'owner': 'ZFS-88', 'user_label': '', 'href': '/api/hardware/v1/cluster/resources/zfs/Pool1', 'type': 'singleton', 'details': ['29.3G']}, {'owner': 'ZFS-88', 'user_label': '', 'href': '/api/hardware/v1/cluster/resources/zfs/Pool2', 'type': 'singleton', 'details': ['29.3G']}], 'peer_asn': ''}}
--------------------------------------------------
description
Clustering is not configured
val : Clustering is not configured <type 'str'>
--------------------------------------------------
peer_state

val :  <type 'str'>
--------------------------------------------------
state
AKCS_UNCONFIGURED
val : AKCS_UNCONFIGURED <type 'str'>
--------------------------------------------------
peer_description

val :  <type 'str'>
--------------------------------------------------
peer_hostname

val :  <type 'str'>
--------------------------------------------------
resources
[{'owner': 'ZFS-88', 'user_label': 'Backup_LAN', 'href': '/api/hardware/v1/cluster/resources/net/e1000g0', 'type': 'singleton', 'details': ['192.168.56.105']}, {'owner': 'ZFS-88', 'user_label': '', 'href': '/api/hardware/v1/cluster/resources/zfs/Pool1', 'type': 'singleton', 'details': ['29.3G']}, {'owner': 'ZFS-88', 'user_label': '', 'href': '/api/hardware/v1/cluster/resources/zfs/Pool2', 'type': 'singleton', 'details': ['29.3G']}]
['owner', 'user_label', 'href', 'type', 'details']
['ZFS-88', 'Backup_LAN', '/api/hardware/v1/cluster/resources/net/e1000g0', 'singleton', ['192.168.56.105']]
['owner', 'user_label', 'href', 'type', 'details']
['ZFS-88', '', '/api/hardware/v1/cluster/resources/zfs/Pool1', 'singleton', ['29.3G']]
['owner', 'user_label', 'href', 'type', 'details']
['ZFS-88', '', '/api/hardware/v1/cluster/resources/zfs/Pool2', 'singleton', ['29.3G']]
--------------------------------------------------
peer_asn

val :  <type 'str'>
[{'fbrm_date': '2020-07-13 09:19:35', 'description': 'Clustering is not configured', 'peer_state': '', 'peer_hostname': '', 'state': 'AKCS_UNCONFIGURED', 'peer_description': '', 'asn': 'df0c6049-dfae-4022-8320-edc1b00b8d8c', 'peer_asn': ''}]
[{'fbrm_date': '2020-07-13 09:19:35', 'user_label': 'Backup_LAN', 'href': '/api/hardware/v1/cluster/resources/net/e1000g0', 'details': '192.168.56.105', 'owner': 'ZFS-88', 'type': 'singleton', 'asn': 'df0c6049-dfae-4022-8320-edc1b00b8d8c'}, {'fbrm_date': '2020-07-13 09:19:35', 'user_label': '', 'href': '/api/hardware/v1/cluster/resources/zfs/Pool1', 'details': '29.3G', 'owner': 'ZFS-88', 'type': 'singleton', 'asn': 'df0c6049-dfae-4022-8320-edc1b00b8d8c'}, {'fbrm_date': '2020-07-13 09:19:35', 'user_label': '', 'href': '/api/hardware/v1/cluster/resources/zfs/Pool2', 'details': '29.3G', 'owner': 'ZFS-88', 'type': 'singleton', 'asn': 'df0c6049-dfae-4022-8320-edc1b00b8d8c'}]
('2020-07-13 09:19:35', 'Clustering is not configured', '', '', 'AKCS_UNCONFIGURED', '', 'df0c6049-dfae-4022-8320-edc1b00b8d8c', '')
insert into master.master_zfs_cluster ("fbrm_date","description","peer_state","peer_hostname","state","peer_description","asn","peer_asn") values ('2020-07-13 09:19:35', 'Clustering is not configured', '', '', 'AKCS_UNCONFIGURED', '', 'df0c6049-dfae-4022-8320-edc1b00b8d8c', '');
------------------------------
insert into master.master_zfs_cluster ("fbrm_date","description","peer_state","peer_hostname","state","peer_description","asn","peer_asn") values ('2020-07-13 09:19:35', 'Clustering is not configured', '', '', 'AKCS_UNCONFIGURED', '', 'df0c6049-dfae-4022-8320-edc1b00b8d8c', '');
('2020-07-13 09:19:35', 'Backup_LAN', '/api/hardware/v1/cluster/resources/net/e1000g0', '192.168.56.105', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c')
insert into master.master_zfs_cluster_resouces ("fbrm_date","user_label","href","details","owner","type","asn") values ('2020-07-13 09:19:35', 'Backup_LAN', '/api/hardware/v1/cluster/resources/net/e1000g0', '192.168.56.105', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c');
('2020-07-13 09:19:35', '', '/api/hardware/v1/cluster/resources/zfs/Pool1', '29.3G', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c')
insert into master.master_zfs_cluster_resouces ("fbrm_date","user_label","href","details","owner","type","asn") values ('2020-07-13 09:19:35', '', '/api/hardware/v1/cluster/resources/zfs/Pool1', '29.3G', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c');
('2020-07-13 09:19:35', '', '/api/hardware/v1/cluster/resources/zfs/Pool2', '29.3G', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c')
insert into master.master_zfs_cluster_resouces ("fbrm_date","user_label","href","details","owner","type","asn") values ('2020-07-13 09:19:35', '', '/api/hardware/v1/cluster/resources/zfs/Pool2', '29.3G', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c');
------------------------------
insert into master.master_zfs_cluster_resouces ("fbrm_date","user_label","href","details","owner","type","asn") values ('2020-07-13 09:19:35', 'Backup_LAN', '/api/hardware/v1/cluster/resources/net/e1000g0', '192.168.56.105', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c');
------------------------------
insert into master.master_zfs_cluster_resouces ("fbrm_date","user_label","href","details","owner","type","asn") values ('2020-07-13 09:19:35', '', '/api/hardware/v1/cluster/resources/zfs/Pool1', '29.3G', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c');
------------------------------
insert into master.master_zfs_cluster_resouces ("fbrm_date","user_label","href","details","owner","type","asn") values ('2020-07-13 09:19:35', '', '/api/hardware/v1/cluster/resources/zfs/Pool2', '29.3G', 'ZFS-88', 'singleton', 'df0c6049-dfae-4022-8320-edc1b00b8d8c');

Process finished with exit code 0
"""

for line in str.splitlines():
    if 'curl' in line:
        print line