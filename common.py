import os
import sys
import datetime

class Common()
    def __init__(self):
        pass

    def get_now_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def get_version(self):
        return '0.01'

    def get_module_head_msg(self, s_title='ZFS hardwre info', s_hostname='', s_ip=''):
        s_execute_date = self.get_now_time()
        s_version = self.get_version()
        s_module_head = ''

        s_module_head = s_module_head + '#' * 79 + '\n'
        s_module_head = s_module_head + '#   ' + ' ' * 74 + '#\n'
        s_module_head = s_module_head + '#   ' + 'Description  : ' + s_title.ljust(59) + '#\n'
        s_module_head = s_module_head + '#   ' + 'HOSTNAME     : ' + s_hostname.ljust(59) + '#\n'
        s_module_head = s_module_head + '#   ' + 'CONNECT IP   : ' + s_ip.ljust(59) + '#\n'
        s_module_head = s_module_head + '#   ' + 'EXECUTE DATE : ' + s_execute_date.ljust(59) + '#\n'
        s_module_head = s_module_head + '#   ' + 'VERSION      : ' + s_version.ljust(59) + '#\n'
        s_module_head = s_module_head + '#   ' + ' ' * 74 + '#\n'
        s_module_head = s_module_head + '#' * 79 + '\n'
        return s_module_head

    def get_module_tail_msg(self, b_default_msg=True):
        s_module_tail = '\n'

        if b_default_msg:
            s_module_tail = s_module_tail + '\n'
            s_module_tail = s_module_tail + '#' * 79 + '\n'
            s_module_tail = s_module_tail + '#' * 79 + '\n'
            s_module_tail = s_module_tail + '#' * 11 + '  END : %s\n' % (self.get_now_time())
            s_module_tail = s_module_tail + '#' * 79 + '\n'
            s_module_tail = s_module_tail + '#' * 79 + '\n'
        return s_module_tail