import datetime



today = datetime.datetime.now()
day_list = []
for i in range(3):
    oday = today - datetime.timedelta(days=i)
    print oday.strftime('%Y-%m-%d')
    day_list.append(oday.strftime('%Y-%m-%d'))


print "','".join(day_list)
