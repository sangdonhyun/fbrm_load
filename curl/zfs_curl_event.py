import json
import os
import glob
import datetime

event_files=glob.glob(os.path.join('data','event*.txt'))

class zfs_curl_event():
    def __init__(self):
        self.today = datetime.datetime.now()
        self.check_date = self.today.strftime('%Y-%m-%d %H:%M:%S')


    def set_audit(self,arg):
        lines = arg.split('-' * 30)[1]
        audit_event = lines[lines.index('{') - 1:]
        audit_json = json.loads(audit_event)
        audit_event_list=[]
        for audit in audit_json['logs']:
            # print audit
            # print audit['timestamp']

            event_time = datetime.datetime.strptime(audit['timestamp'], '%Y%m%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

            if 'address' in audit.keys():
                addr = str(audit['address'])
            else:
                addr = ''
            if 'user' in audit.keys():
                user = str(audit['user'])
            else:
                addr = ''
            if 'summary' in audit.keys():
                summary = str(audit['summary'])
            else:
                summary = ''

            # print user,addr,summary
            # for key in  audit.keys():
            #     print key,audit[key]
            event_dict = {}
            event_dict['log_date'] = self.check_date
            event_dict['check_date'] = self.check_date
            event_dict['check_category'] = 'ZFS_CURL'
            event_dict['event_date'] = event_time
            event_dict['event_code'] = 'zfs_audit_001'
            event_dict['serial_number'] = self.ip
            event_dict['event_level'] = 'info'
            event_dict['device_type'] = "zfs_cluster"
            event_dict['desc_detail'] = 'user(%s) address(%s) %s' % (user, addr, summary)
            event_dict['vendor_name'] = 'Oracle'
            audit_event_list.append(event_dict)
            # print event_dict

    def set_fault(self, arg):
        lines = arg.split('-' * 30)[1]
        fault_event = lines[lines.index('{') - 1:]
        fault_json = json.loads(fault_event)
        fault_event_list=[]
        for fault in fault_json['logs']:
            event_time = datetime.datetime.strptime(fault['timestamp'], '%Y%m%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            serial = fault['uuid']
            type  = fault['type']
            event_dict = {}
            event_dict['log_date'] = self.check_date
            event_dict['check_date'] = self.check_date
            event_dict['check_category'] = 'ZFS_CURL'
            event_dict['event_date'] = event_time
            event_dict['event_code'] = 'zfs_fault_001'
            event_dict['serial_number'] = serial
            event_dict['event_level'] = fault['severity']
            event_dict['device_type'] = "zfs_cluster"
            event_dict['desc_detail'] = '[%s] %s'%(type,fault['description'])
            event_dict['vendor_name'] = 'Oracle'
            fault_event_list.append(event_dict)

    def set_system(self, arg):
        lines = arg.split('-' * 30)[1]
        system_event = lines[lines.index('{') - 1:]
        system_json = json.loads(system_event)
        system_event_list=[]
        for system in system_json['logs']:
            # print system
            event_time = datetime.datetime.strptime(system['timestamp'], '%Y%m%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

            event_dict = {}
            event_dict['log_date'] = self.check_date
            event_dict['check_date'] = self.check_date
            event_dict['check_category'] = 'ZFS_CURL'
            event_dict['event_date'] = event_time
            event_dict['event_code'] = 'zfs_system_001'
            event_dict['serial_number'] = self.ip
            event_dict['event_level'] = system['priority']
            event_dict['device_type'] = "zfs_cluster"
            event_dict['desc_detail'] = '[%s] %s'%(system['module'],system['text'])
            event_dict['vendor_name'] = 'Oracle'
            # print event_dict
            system_event_list.append(event_dict)
    def set_alert(self, arg):
        lines = arg.split('-' * 30)[1]
        alert_event = lines[lines.index('{') - 1:]
        alert_json = json.loads(alert_event)
        alert_event_list=[]
        for alert in alert_json['logs']:
            print alert
            event_time = datetime.datetime.strptime(alert['timestamp'], '%Y%m%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

            event_dict = {}
            event_dict['log_date'] = self.check_date
            event_dict['check_date'] = self.check_date
            event_dict['check_category'] = 'ZFS_CURL'
            event_dict['event_date'] = event_time
            event_dict['event_code'] = 'zfs_alert_001'
            event_dict['serial_number'] = alert['uuid']
            event_dict['event_level'] = alert['severity']
            event_dict['device_type'] = "zfs_cluster"
            event_dict['desc_detail'] = '[%s] %s'%(alert['alert'],alert['description'])
            event_dict['category_a'] = 'Oracle'
            print event_dict
            alert_event_list.append(event_dict)
        tb='event.event_log'
        


    def main(self):

        for file in event_files:
            print file
            ip = file.split('_')[-1]
            ip = ip.replace('.txt','')
            self.ip = ip
            with open(file) as f:
                readset = f.read()

            for arg in readset.split('curl --'):
                print arg[:100]
                if 'logs/audit' in  arg[:100]:
                    self.set_audit(arg)
                if 'logs/fault' in  arg[:100]:
                    self.set_fault(arg)
                if 'logs/system' in  arg[:100]:
                    self.set_system(arg)
                if 'logs/alert' in  arg[:100]:
                    self.set_alert(arg)



if __name__=='__main__':
    zfs_curl_event().main()

