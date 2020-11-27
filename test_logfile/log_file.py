import re
import os
with open('log.log') as f:

    lineset = f.readlines()


for line in lineset:
    if re.match('^datafile',line):
        # print line
        path= line[line.index('=')+1:].strip()
        print '/'.join(path.split('/')[:4])