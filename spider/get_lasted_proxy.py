import urllib.parse
import random

def get_iplist():
    url = 'http://cn-proxy.com'
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

    data = {}
    data = urllib.parse.urlencode(data).encode('utf-8')
    getiplist = []

    req = urllib.request.Request(url,data,header)
    response = urllib.request.urlopen(req)

    html = response.read().decode('utf-8')

    iplist = re.findall(r'<tr>(.+?)</tr>',html,re.S)
    #print(iplist)

    for each in iplist:
        li = re.findall(r'<td>(.+?)</td>',each,re.S)

        if(len(li)):
            ip = re.search(r'(([0-9]{1,3}\.){3}([0-9]{1,3}))',li[0])
            #print(ip)
            if(ip):
                port = re.search(r'[0-9]{1,5}',li[1])
                #print(ip.group(0)+":"+port.group(0))
                getiplist.append(ip.group(0)+":"+port.group(0))

    return random.choice(getiplist)

if __name__ == '__main__':
    x = get_iplist()
    print(x)
