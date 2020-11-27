with open('rman.txt') as f:
    tmpset = f.read().strip()


lineset = tmpset.splitlines()
linecnt = 0
for i in range(len(lineset)):
    line = lineset[i]
    if ',' in line:
        print line
        linecnt = linecnt +1




print linecnt

