import datetime


utc_time = "Mon Nov 18 2020 00:01:10 GMT+0000 (UTC)"
uct=datetime.datetime.now() - datetime.timedelta(days=9)

cd_time= datetime.datetime.strptime(utc_time,"%a %b %d %Y %H:%M:%S GMT+0000 (UTC)")



print cd_time
local_time=  cd_time + datetime.timedelta(hours=9)
print local_time.strftime('%Y-%m-%d %H:%M:%S')