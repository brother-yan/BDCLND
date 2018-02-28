#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['dload', 'download']

import requests
import time
import numpy as np
import base64
import json

session = requests.Session()
User_Agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36'}
host = 'https://pan.baidu.com'

def verify(surl, pwd):
    surl = surl[1:]
    Referer = {'Referer' : host + '/share/init' + '?surl=' + surl}
    
    t = int(time.time() * 1000)
    logid = str(int(time.time() * 1000)) + str(np.round(np.random.rand(), 16))
    logid = base64.b64encode(logid.encode()).decode()
    
    params = {'surl' : surl, 't' : t, 'bdstoken' : 'null', 'channel' : 'chunlei', 'clienttype' : 0, 'web' : 1, 'app_id' : 250528, 'logid' : logid}
    data = {'pwd' : pwd, 'vcode' : '', 'vcode_str' : ''}
    r = session.post(host + '/share/verify', params = params, data = data, headers = {**Referer, **User_Agent})
    return r.json()

def dlink(surl, vcode_input = None, vcode_str = None):
    r = session.get(host + '/s/' + surl, headers = User_Agent)
    r = r.text
    r = r[r.find('yunData.setData') : r.rfind('yunData.setData')]
    r = r[len('yunData.setData(') : r.rfind(');')]
    r = json.loads(r)
    
    logid = str(int(time.time() * 1000)) + str(np.round(np.random.rand(), 16))
    logid = base64.b64encode(logid.encode()).decode()
    
    if 'BDCLND' in session.cookies.keys():
        sekey = session.cookies['BDCLND']
        sekey = requests.utils.unquote(sekey)
        extra = '{"sekey"' + ':"' + sekey + '"}' # extra = {"sekey" : sekey}
    else: # for public share link
        extra = None
    fid_list = '[' + str(r['file_list']['list'][0]['fs_id']) + ']'
    
    Referer = {'Referer' : host + '/s/' + surl}
    params = {'sign' : r['sign'], 'timestamp' : r['timestamp'], 'bdstoken' : 'null', 'channel' : 'chunlei', 'clienttype' : 0, 'web' : 1, 'app_id' : 250528, 'logid' : logid}
    data = {'encrypt' : 0, 'extra' : extra, 'product' : 'share', 'vcode_input' : vcode_input, 'vcode_str' : vcode_str, 'uk' : r['uk'], 'primaryid' : r['shareid'], 'fid_list' : fid_list, 'path_list' : ''}
    r = session.post(host + '/api/sharedownload', params = params, data = data, headers = {**Referer, **User_Agent})
    return r.json()

def capcha(surl):
    Referer = {'Referer' : host + '/s/' + surl}
    
    t = str(np.round(np.random.rand(), 16))
    logid = str(int(time.time() * 1000)) + str(np.round(np.random.rand(), 16))
    logid = base64.b64encode(logid.encode()).decode()
    
    params = {'prod' : 'pan', 't' : t, 'bdstoken' : 'null', 'channel' : 'chunlei', 'clienttype' : 0, 'web' : 1, 'app_id' : 250528, 'logid' : logid}
    r = session.get(host + '/api/getvcode', params = params, headers = {**Referer, **User_Agent})
    return r.json()


from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def dload(surl, pwd, path = ''):
    session = requests.Session() # create a new session
    if pwd != None: # private share link
        r = verify(surl, pwd)
        if r['errno'] != 0:
            print(r)
            return 'url or password incorrect'
    
    r = dlink(surl)
    for i in range(20):
        if r['errno'] == 0:
            break
        r = capcha(surl)
        vcode_str = r['vcode']
        r = session.get(r['img'])
        img = Image.open(BytesIO(r.content))
        print('Please input capcha：')
        plt.imshow(img)
        plt.show()
        vcode_input = input()
        r = dlink(surl, vcode_input, vcode_str)
    if r['errno'] != 0:
        print(r)
        return 'can\'t fetch download link'
    
    name = r['list'][0]['server_filename']
    link = r['list'][0]['dlink']
    r = session.get(link)
    if r.status_code != 200:
        return 'download error'
    with open(path + name, 'wb') as f:
        f.write(r.content)
    return 'OK'

def download(s, path = ''):
    if s.find('密码') != -1:
        surl = s[s.find(host) + len(host) + 3 : s.find('密码')].strip()
        p = s[s.find('密码') + 3 :].strip()[:4]
    else:
        surl = s[s.find(host) + len(host) + 3 :].strip()
        p = None
    r = dload(surl, p, path)
    return r




if __name__ == '__main__':
    s = input('请输入资源：')
    r = download(s)
    print(r)
