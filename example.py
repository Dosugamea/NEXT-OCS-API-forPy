import NextCloud
import json

url = "INPUT_YOUR_CLOUD"
userid = "INPUT_YOUR_USERNAME"
passwd = "INPUT_YOUR_PASSWORD"

#True if you want to get response as JSON
#False if you want to get response as XML
tojs = True

nxc = NextCloud.NextCloud(url,userid,passwd,tojs)
print(nxc.getUsers())