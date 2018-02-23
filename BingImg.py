# !usr/bin/python3.4
# -*- coding:utf-8 -*-

import json
import grequests
import requests
import re
import time
import os

def geturl(urls):

    sn = requests.Session()
    rs = [grequests.get(url, session=sn) for url in urls]

    return grequests.map(rs)

def get(url):

    header = {'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
                'Referer':'http://cn.bing.com',
                'Host': 'cn.bing.com'}

    # 解析网页
    html_bytes = requests.get(url, headers=header)
    return html_bytes

# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    # '/\:*?"<>|'
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "", title)
    return new_title

if __name__ == '__main__':
    i = 0
    img = []
    imgname = []
    while True:
        url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=' + str(i) + '&n=1'
        urlPre = "http://cn.bing.com/"
        contents =get(url)
        data = contents.content.decode('utf-8', 'ignore')
        data = json.loads(data)
        try:
            onefile = data['images']
            for item in onefile:
                if len(img) > 0 and img[-1] == urlPre + item['url']:
                    raise RuntimeError('testError')
                else:
                    img.append(urlPre + item['url'])
                    imgname.append(item['copyright'].replace(' ', ''))
                print(img[i])
            i = i + 1
        except Exception as err:
            print(err)
            break

    print('已经搜集好网址...')
    print('暂停3秒后开始批量下载图片，请保持网络畅通...')
    time.sleep(3)
    print('正在下载...')
    pics = geturl(img)

    j = 0
    for pic in pics:
        filenamep = os.path.abspath('.') + '/jpg/' + validateTitle(imgname[j] + '.jpg')
        filess = open(filenamep, 'wb')
        filess.write(pic.content)
        filess.close()
        print('已经写入第' + str(j + 1) + '张图片')
        j = j + 1