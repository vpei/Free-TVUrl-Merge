#!/usr/bin/env python3

import base64
import datetime
from gettext import find
import hashlib
import json
import os
import requests
import sys
from cls import IsValid
from cls import LocalFile
from cls import ListFile
from cls import NetFile
from cls import PingIP
from cls import StrText

# 获取传递的参数
try:
    #0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        cid = sys.argv[1:][1]
except:
    menu = 'init'
print('menu: ' + menu)

# ustat = NetFile.url_stat('https://video.xuanqi.pro/api.php/provide/vod/', 60, 60)
# menu = 'update'
# menu = 'upexpire'
# menu = 'uptvbox'
# menu = 'check'
# 配置信息和同步本地需要更新的资源文件
# resurl = 'http://121.46.250.130:8080/ipns/k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax/'

# 对程序的基本信息进行下载更新，下载IPFS网关信息和过滤列表信息
# if(menu == 'init'):
#     filename = 'live.json|tvbox.json'
#     for i in filename.split('|'):
#         try:
#             File = NetFile.url_to_str(resurl + '' + i, 240, 240)
#             if(len(File) > 10240):
#                 LocalFile.write_LocalFile('./res/' + i, File.strip('\n')) 
#                 print('Get-File-is-True:' + resurl + '' + i + ' FileSize:' + str(len(File)))
#         except Exception as ex:
#             print('Get-File-is-False:' + resurl + '' + i + '\n' + str(ex))


# def write_json():
#     '''
#     写入/追加json文件
#     :param obj:
#     :return:
#     '''
#     # post=set()
#     # fp=[]
#     # for p in range(len(json)):
#     #         if json[p]['text'] not in post:#如果set中没有这个值（set特性是不能重复）
#     #                 fp.append(json[p])#fp数组将这个不重复的值存进
#     #                 post.add(json[p]['text'])#set存进这个不重复的值，为了后面判断是否重复做准备
#     #                 print(json[p])
#     #                 print(post)
#     #                 print(json[p]['text'])
#     # print(fp)

#     #首先读取已有的json文件中的内容
#     post=set()
#     item_list = []
#     alltypename = ''
#     with open('./res/tvlist.json', 'r', encoding='utf-8') as f:
#         load_dict = json.load(f)
#         num_item = len(load_dict)
#         for i in range(num_item):
#             try:
#                 if load_dict[i]['tvmd5'] not in post:#如果set中没有这个值（set特性是不能重复）
#                     post.add(str(load_dict[i]['tvmd5']))#set存进这个不重复的值，为了后面判断是否重复做准备
#                     typename = load_dict[i]['typename']
#                     if(alltypename.find(typename) == -1):
#                         alltypename = alltypename + '\r\n' + typename
#                     # tvname = load_dict[i]['tvname']
#                     # tvmd5 = load_dict[i]['tvmd5']
#                     # tvurl = load_dict[i]['tvurl']

#                     # item_dict = {'typename':typename, 'tvname':tvname,'tvmd5':tvmd5, 'tvurl':tvurl}
#                     # item_list.append(item_dict)
#                     item_list.append(load_dict[i])
#             except Exception as ex:
#                 LocalFile.write_LogFile('Main-Line-87-Exception:' + str(ex))
            
#     #读取已有内容完毕
#     #将新传入的dict对象追加至list中
#     # item_list.append(obj)
#     #将追加的内容与原有内容写回（覆盖）原文件
#     with open('./res/tvlist.json', 'w', encoding='utf-8') as f2:
#         json.dump(item_list, f2, ensure_ascii=False)
#     LocalFile.write_LocalFile('./res/typename.txt', alltypename.lstrip('\r\n'))

# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
# 本菜单暂时无效
if(menu == 'update'):
    oldexpire = LocalFile.read_LocalFile("./res/r_sites_err.txt")
    nettvexpire = LocalFile.read_LocalFile("./res/expire.txt")
    # 本地所有失效链接合并去重存储至expires.txt
    allexpire = oldexpire.strip('\n') + '\n' + nettvexpire.strip('\n')
    expires = ''
    expirecount = len(allexpire.split('\n'))
    print('Get-oldexpire.txt: \n' + str(expirecount))
    for i in allexpire.split('\n'):
        if(expires.find(i) == -1):
            expires = expires + i + '\n'
    if(len(expires) > len(oldexpire)):
        LocalFile.write_LocalFile('./res/r_sites_err.txt', expires.strip('\n')) 
    print('Get-expire.txt: \n' + str(len(expires)))

    tvlist = LocalFile.read_LocalFile("./res/tvlist.json")
    list1 = tvlist.split('\n')
    list1 = ListFile.get_list_sort(list1)
    print('Get-tvbox.json: \n' + str(len(list1)))

    boxurl = ''
    boxsites = ''
    allonesite = ''
    ii = 0
    iii = 0
    for i in list1:
        ii += 1
        print('\nNodes-List-OneNodeList:\n' + i)
        if(i == ''):
            continue
        else:
            osite = json.loads(i)
            # osite_uptime = osite['typename']
            # osite_uptime = osite['tvname']
            osite_uptime = osite['uptime']
            osite_upmd5 = osite['upmd5']
            osite_tvurl = osite['tvurl']
            osite_size = osite['size']
        if(boxurl.find(osite_tvurl) == -1):
            try:
                newboxurl = osite_tvurl.replace('<yyyy>', datetime.datetime.now().strftime('%Y'))
                newboxurl = newboxurl.replace('<mm>', datetime.datetime.now().strftime('%m'))
                newboxurl = newboxurl.replace('<dd>', datetime.datetime.now().strftime('%d'))
                print('Get node link on sub ' + newboxurl)
                requests.adapters.DEFAULT_RETRIES = 3 # 增加重连次数
                s = requests.session()
                s.keep_alive = False # 关闭多余连接
                s.verify = False
                rq = s.get(newboxurl, timeout=(240, 120)) #连接超时 和 读取超时
                # rq = s.get(newboxurl, keep_alive=False, verify=False, timeout=(240, 120)) #连接超时 和 读取超时
                # rq.encoding = 'utf-8'
                if (rq.status_code != 200 and rq.status_code != 301 and rq.status_code != 302):
                    print('[GET Code {}] Download sub error on link: '.format(rq.status_code) + osite_upurl)
                    boxurl = boxurl + '\n' + i
                    continue
                # boxsites = (rq.content).decode('utf-8', 'ignore') # 可用
                # print(str(isinstance(rq.text, basestring)))
                # print(str(chardet.detect(rq.text)))
                if(rq.encoding != None):
                    boxsites = rq.text.encode(rq.encoding).decode('utf-8')
                else:
                    boxsites = rq.text.encode('utf-8') #unicode -> str
                    boxsites = boxsites.decode('utf-8') #str -> unicode
                boxsites = boxsites.encode('utf-8').decode('utf-8', 'ignore').replace('\ufeff', '').strip('\n')
                if (boxsites != '' and osite_upmd5 != hashlib.md5(boxsites.encode('utf-8')).hexdigest()):
                    osite['upmd5'] = hashlib.md5(boxsites.encode('utf-8')).hexdigest()
                    if (osite_tvurl.find('k51qzi5uqu5dgc33fk7pd3093uw5ouejcyhwicv6gtfersoetui51qxq62zn5a') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1453)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax/index') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1097)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('out/node') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=731)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('vpei') > -1 or osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                    #elif (ii > 115):
                    #    osite['uptime'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        osite['uptime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    osite['size'] = len(boxsites)
                    i = json.dumps(osite)
                    print('UpdateTime:' + osite['uptime'] + ' boxsites-len:' + str(len(boxsites)))
                    # if(IsValid.isBase64(boxsites)):
                    #     boxsites = StrText.get_str_base64(boxsites) # Base64格式化
                    #     boxsites = base64.b64decode(boxsites).decode('utf-8')
                    #     print('Url-All-Nodes-is-Base64:' + newboxurl)
                    # else:
                    #     print('Url-All-Nodes-no-Base64:' + newboxurl)
                    allonesite = ''
                    if (osite['type'] == 'tlive'):
                        alltv = boxsites #NetFile.url_to_str(osite_tvurl, 240, 240)
                        
                        typename = ''
                        for onetv in alltv.split('\n'):
                            try:
                                onetv = onetv.rstrip('\r').replace(' ','')
                                if(onetv != ''):
                                    if(onetv.find(',#genre#') > -1):
                                        typename = onetv.split(',')[0]
                                        if(typename.find('韩') > -1 or typename.find('韩国') > -1):
                                            typename = '韩国频道'
                                        elif(typename.find('cctv') > -1 or typename.find('央视') > -1):
                                            typename = '央视频道'
                                        elif(typename.find('卫视') > -1):
                                            typename = '卫视频道'
                                    elif(onetv.find(',') > -1 and onetv.find('://') > -1):
                                        tvname = onetv.split(',')[0]
                                        tvurl = onetv.split(',')[1]
                                        #obj字典对象为新增内容
                                        # .encode('utf-8') #unicode -> str
                                        # .decode('utf-8') #str -> unicode
                                        obj = {"typename": "" + typename.encode('utf-8').decode('utf-8') + "","tvname": "" + tvname.encode('utf-8').decode('utf-8') + "","tvmd5": "" + hashlib.md5(tvurl.encode('utf-8')).hexdigest() + "","tvurl": "" + tvurl + ""}
                                        #write_json(obj)
                                        print(obj)
                                        # obj = json.dumps(obj, encoding='utf-8', ensure_ascii=False)
                                        print(str(obj))
                                        print(type(obj))
                                        # dictinfo = json.loads(obj)
                                        fjson = './res/tvlist.json'
                                        with open(fjson, 'r') as f:
                                            content = json.load(f)     
                                                                
                                        # axis = {"axis":[22, 10, 11]}
                                        content.append(obj)
                                        
                                        print(type(content))
                                        with open(fjson, 'w') as f_new:
                                            json.dump(content, f_new, indent=4, ensure_ascii=True)
                            except Exception as ex:
                                LocalFile.write_LogFile('Main-Line-205-Exception:' + str(ex) + '\nonesite:\n' + onetv)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-272-main-Exception:' + str(ex) + '\nosite_tvurl:\n' + osite_tvurl)
            boxurl = boxurl + '\n' + i
    # 去除重复项目
    # write_json()
    # 将节点更新时间等写入配置文件
    if (boxurl.find('uptime') > -1):
        LocalFile.write_LocalFile('./res/list.json', boxurl.strip('\n'))
    print('Line-238:tvbox.json已更新，共更新网址[' + str(iii) + ']。')
    #print('Url-All-Clash-To-Mixed-Nodes:\n' + allonesite)

    # 读取所有节点到allonesite新记录后面。
    alltypename = LocalFile.read_LocalFile("./res/typename.txt").replace('\r','')
    tvlists = []
    with open('./res/tvlist.json', 'r', encoding='utf-8') as f:
        tvlists = json.load(f)
    num_item = len(tvlists)
    alltv = ''
    oldtypename = ''
    for ii in alltypename.split('\n'):
        for i in range(num_item):
            try:
                typename = tvlists[i]['typename'].decode("unicode-escape")
                tvname = tvlists[i]['tvname'].decode("unicode-escape")
                tvurl = tvlists[i]['tvurl'].decode("unicode-escape")
                if(tvname.find(ii) == -1 or typename == ii):
                    if(ii == oldtypename):
                        alltv += '\r\n' + typename + ',' + tvurl
                    else:
                        alltv += '\r\n\r\n' + typename + ',#genre#'
                # tvname = load_dict[i]['tvname']
                # tvmd5 = load_dict[i]['tvmd5']
                # tvurl = load_dict[i]['tvurl']
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-264-Exception:' + str(ex) + '\nonesite:' + i)
    alltv = alltv.strip('\n').encode('utf-8')
    # allboxs.json = base64.b64encode(boxsites.strip('\n').encode('utf-8')).decode('utf-8')
    LocalFile.write_LocalFile('./out/all', alltv)
    print('Line-293-Node整理成功，共有记录' + str(iii) + '条。')


# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if(menu == 'upexpire'):
    r_sites_err = LocalFile.read_LocalFile("./res/r_sites_err.txt")
    nettvexpire = LocalFile.read_LocalFile("./res/expire.txt")
    nettvexpire = nettvexpire.strip('\n')
    # 处理临时数据和网络失效数据中vmess同一IP和端口过滤列表
    fakeip = LocalFile.read_LocalFile("./res/fakeip.txt")
    newallexpire = ''
    for i in nettvexpire.split('\n'):
        try:
            if(i.find('://')>-1):
                i = StrText.get_str_btw((i + '/'), '://', '/', 0)
                if(fakeip.find(i) == -1):
                    newallexpire = newallexpire + '\n' + i
        except Exception as ex:
            LocalFile.write_LogFile('Main-Line-324-Exception:' + str(ex) + '\nexpire:' + i)
    # LocalFile.write_LocalFile('./res/fakeip.txt', fakeip)
    
    # 本地所有失效链接合并去重存储至expires.txt
    allexpire = r_sites_err.strip('\n') + '\n' + newallexpire.strip('\n')
    expires = ''
    expirecount = len(allexpire.split('\n'))
    print('Get-oldexpire.txt: \n' + str(expirecount))
    for i in allexpire.split('\n'):
        if(expires.find(i) == -1):
            expires = expires + i + '\n'
    if(len(expires) > len(r_sites_err)):
        LocalFile.write_LocalFile('./res/r_sites_err.txt', expires.strip('\n')) 
    print('Get-expire.txt: \n' + str(len(expires)))

if(menu == 'uptvbox'):
    tvlist = LocalFile.read_LocalFile("./res/tvlist.json")
    print('Get-tvbox.json: \n' + str(len(tvlist.split('\n'))))
    #sub_link = []
    #for i in range(len(sub_url)):
    #    s_url = sub_url[i]
    boxurl = ''
    boxsites = ''
    allonesite = ''
    list1 = tvlist.split('\n')
    list1 = ListFile.get_list_sort(list1)
    ii = 0
    iii = 0
    # 获取默认值再添加后重写
    alllive = LocalFile.read_LocalFile("./res/live.txt")
    r_parses = LocalFile.read_LocalFile("./res/r_parses.txt")
    r_parses_err = LocalFile.read_LocalFile("./res/r_parses_err.txt")
    tvlist = LocalFile.read_LocalFile("./res/all")
    if(tvlist.find('"sites":[')>-1):
        tvlist = StrText.get_str_btw(tvlist, '"sites":[', '],', 0) + ','
    tvjar = ''
    for i in list1:
        ii += 1
        print('\nNodes-List-OneNodeList:\n' + i)
        if(i == ''):
            continue
        else:
            osite = json.loads(i)
            # osite_uptime = osite['typename']
            # osite_uptime = osite['tvname']
            osite_uptime = osite['uptime']
            osite_upmd5 = osite['upmd5']
            osite_tvurl = osite['tvurl']
            osite_size = osite['size']
        if(boxurl.find(osite_tvurl) == -1):
            try:
                newboxurl = osite_tvurl.replace('<yyyy>', datetime.datetime.now().strftime('%Y'))
                newboxurl = newboxurl.replace('<mm>', datetime.datetime.now().strftime('%m'))
                newboxurl = newboxurl.replace('<dd>', datetime.datetime.now().strftime('%d'))
                print('Get boxurl link on sub ' + newboxurl)
                requests.adapters.DEFAULT_RETRIES = 3 # 增加重连次数
                s = requests.session()
                s.keep_alive = False # 关闭多余连接
                s.verify = False
                rq = s.get(newboxurl, timeout=(240, 120)) #连接超时 和 读取超时
                # rq = s.get(newboxurl, keep_alive=False, verify=False, timeout=(240, 120)) #连接超时 和 读取超时
                # rq.encoding = 'utf-8'
                if (rq.status_code != 200 and rq.status_code != 301 and rq.status_code != 302):
                    print('[GET Code {}] Download sub error on link: '.format(rq.status_code) + osite_tvurl)
                    boxurl = boxurl + '\n' + i
                    continue
                # boxsites = rq.content
                # boxsites = boxsites.encode(rq.encoding).decode('utf-8')
                # print(str(isinstance(rq.text, basestring)))
                # print(str(chardet.detect(rq.text)))
                if(rq.encoding != 'utf-16le' and rq.encoding != None):
                    boxsites = rq.text.encode(rq.encoding).decode('utf-8')
                else:
                    boxsites = rq.text.encode('utf-8') #unicode -> str
                    boxsites = boxsites.decode('utf-8') #str -> unicode
                boxsites = boxsites.replace(' ','')
                boxsites = boxsites.encode('utf-8').decode('utf-8', 'ignore').replace('\ufeff', '').strip('\n')
                # if (boxsites != ''):# and osite_upmd5 != hashlib.md5(boxsites.encode('utf-8')).hexdigest()):
                if (boxsites != '' and (osite_upmd5 != hashlib.md5(boxsites.encode('utf-8')).hexdigest() or osite_tvurl.find('/vpei/')>-1 or osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax')>-1)):
                    # 写入文件
                    LocalFile.write_LocalFile('./tmp/' + hashlib.md5(newboxurl.encode('utf-8')).hexdigest() + '.txt', boxsites)
                    osite['upmd5'] = hashlib.md5(boxsites.encode('utf-8')).hexdigest()
                    if (osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1453)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax/index2') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1097)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('out/node') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=731)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('vpei') > -1 or osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                    #elif (ii > 115):
                    #    osite['uptime'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        osite['uptime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    osite['size'] = len(boxsites)
                    i = json.dumps(osite)
                    #　boxsites = boxsites.encode('utf-8').decode('utf-8', 'ignore').strip('\n')
                    print('UpdateTime:' + osite['uptime'] + ' boxsites-len:' + str(len(boxsites)))
                    # if(IsValid.isBase64(boxsites)):
                    #     boxsites = StrText.get_str_base64(boxsites) # Base64格式化
                    #     boxsites = base64.b64decode(boxsites).decode('utf-8')
                    #     print('Url-All-Nodes-is-Base64:' + newboxurl)
                    # else:
                    #     print('Url-All-Nodes-no-Base64:' + newboxurl)
                    allonesite = ''
                    if (osite['type'] == 'tlive'):
                        alltv = boxsites #NetFile.url_to_str(osite_tvurl, 240, 240)
                        typename = ''
                        for onetv in alltv.split('\n'):
                            try:
                                onetv = onetv.rstrip('\r').replace(' ','')
                                if(onetv != ''):
                                    if(onetv.find(',#genre#') > -1):
                                        typename = onetv.split(',')[0]
                                        if(typename.find('韩') > -1 or typename.find('韩国') > -1):
                                            typename = '韩国频道'
                                        elif(typename.find('cctv') > -1 or typename.find('央视') > -1):
                                            typename = '央视频道'
                                        elif(typename.find('卫视') > -1):
                                            typename = '卫视频道'
                                    elif(onetv.find(',') > -1 and onetv.find('://') > -1):
                                        tvname = onetv.split(',')[0]
                                        tvurl = onetv.split(',')[1]
                                        #obj字典对象为新增内容
                                        # .encode('utf-8') #unicode -> str
                                        # .decode('utf-8') #str -> unicode
                                        obj = {"typename": "" + typename.encode('utf-8').decode('utf-8') + "","tvname": "" + tvname.encode('utf-8').decode('utf-8') + "","tvmd5": "" + hashlib.md5(tvurl.encode('utf-8')).hexdigest() + "","tvurl": "" + tvurl + ""}
                                        #write_json(obj)
                                        print(obj)
                                        # obj = json.dumps(obj, encoding='utf-8', ensure_ascii=False)
                                        print(str(obj))
                                        print(type(obj))
                                        # dictinfo = json.loads(obj)
                                        fjson = './res/tvlist.json'
                                        with open(fjson, 'r') as f:
                                            content = json.load(f)     
                                                                
                                        # axis = {"axis":[22, 10, 11]}
                                        content.append(obj)
                                        
                                        print(type(content))
                                        with open(fjson, 'w') as f_new:
                                            json.dump(content, f_new, indent=4, ensure_ascii=True)
                            except Exception as ex:
                                LocalFile.write_LogFile('Main-Line-205-main-Exception:' + str(ex) + '\nosite_tvurl:\n' + onetv)
                    elif (osite['type'] == 'mixed'):
                        boxsites = boxsites.replace('\r','').replace('\n','').replace('\t','').replace('	','').replace(' ','')
                        tvjar = StrText.get_str_btw(boxsites, '"spider":"', '",', 0)
                        if(boxsites.find('"proxy://do=live&type=txt&ext=')>-1):
                            try:
                                onelive = base64.b64decode(StrText.get_str_btw(boxsites, 'proxy://do=live&type=txt&ext=', '"', 0)).decode('utf-8')
                                if(alllive.find(onelive) == -1):
                                    alllive = onelive + '\r\n' + alllive
                            except Exception as ex:
                                LocalFile.write_LogFile('Main-Line-488-Exception:\n' + str(ex))
                        if(boxsites.find('"parses":[') > -1 and boxsites.find('}],') > -1):
                            parses = StrText.get_str_btw(boxsites, '"parses":[', '}],', 0) + '}'
                            parses = parses.replace(' ','').replace('\r','').replace('\n','').replace('//{','{').strip('{').strip('}')
                            for oneparse in parses.split('},{'):        
                                try:
                                    if(oneparse[-3:] == '},}'):
                                        oneparse = oneparse[:-2]
                                    if(len(oneparse.split('{')) == len(oneparse.split('}'))): #指定字符数量-1
                                        oneparse = '{' + oneparse + '}'
                                        if(oneparse.find('"name":"') > -1 and oneparse.find('"url":"') > -1):
                                            onep = json.loads(oneparse)
                                            if(r_parses.find(onep['url']) == -1 and r_parses_err.find(onep['url']) == -1):
                                                if(oneparse.find('"ext":"') > -1):
                                                    r_parses = oneparse + ',' + '\r\n' + r_parses
                                                else:
                                                    r_parses += '\r\n' + oneparse + ','
                                    else:
                                        LocalFile.write_LogFile('Main-Line-457-boxurl:' + newboxurl + '\nparse:' + oneparse)
                                except Exception as ex:
                                    LocalFile.write_LogFile('Main-Line-459-Exception:\n' + str(ex) + '\n' + oneparse)
                        if(boxsites.find('"sites":[') > -1 and boxsites.find('}],') > -1):
                            boxsites = StrText.get_str_btw(boxsites, '"sites":[', '}],', 0) + '}'
                            for onetvurl in boxsites.split('},{'):
                                try:
                                    onetvurl = '{' + onetvurl + '}'
                                    onetvurl = onetvurl.replace('{{','{').replace('}}','}')
                                    osite = json.loads(onetvurl)
                                    if(osite['type'] == 1 or osite['type'] == 2):
                                        tvlist += onetvurl + ',\r\n'
                                    elif(osite['type'] == 3):
                                        if(onetvurl.find('"jar":"') == -1):
                                            tvlist += onetvurl.replace('}',',"jar":"' + tvjar + '"}') + ',\r\n'
                                        else:
                                            tvlist += onetvurl + ',\r\n'
                                    else:
                                        tvlist += onetvurl + ',\r\n'
                                except Exception as ex:
                                    LocalFile.write_LogFile('Main-Line-211-Exception:' + str(ex) + '\nonetvurl:\n' + onetvurl)
                        elif(boxsites.find('proxies:') > -1 and boxsites.find('proxy-groups:') == -1):
                            boxsites = ''
                iii += 1
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-530-Exception:' + str(ex) + '\nosite_tvurl:\n' + osite_tvurl)
            boxurl = boxurl + '\n' + i
    # tvlist = tvlist.replace(',"jar":"' + tvjar + '"','')
    tvlist = tvlist.replace(',"jar":"http://freed.yuanhsing.cf/TVBox/MaooXB2/XBiubiuLA4.jar"','')
    tvlist = tvlist.replace(',"jar":"http://121.46.250.130:8080/ipfs/QmZFDWsm15DiH3WLb2WwgPb136tKPibvMoGKDT41aEpwfa?filename=XBiubiuLA4.jar"','')
    tvlist = tvlist.replace(',"jar":"https://raw.iqiq.io/vpei/Free-TVUrl-Merge/main/res/XBiubiuLA4.PNG"','')
    # 去除重复项目
    # write_json()
    # 将节点更新时间等写入配置文件
    if (boxurl.find('uptime') > -1):
        LocalFile.write_LocalFile('./res/tvlist.json', boxurl.strip('\r\n'))
        print('Line-532:TvList.json已更新，共更新网址[' + str(iii) + ']。')

    LocalFile.write_LocalFile('./out/all', tvlist.strip('\r\n'))
    LocalFile.write_LocalFile('./res/live.txt', alllive)
    print('Line-535:/res/live.txt已更新。')

    # 检测parses url 是否能正常访问
    parses = r_parses.replace(' ','').replace('\r','').replace('\n','').replace('//{','{').strip('{').strip('}')
    r_parses = '{"name":"解析聚合","type":3,"url":"Demo"},\r\n{"name":"Json并发","type":2,"url":"Parallel"},\r\n{"name":"Json轮询","type":2,"url":"Sequence"},'
    for oneparse in parses.split('},{'):        
        try:
            oneparse = '{' + oneparse + '}'
            if(oneparse.find('"name":"') > -1 and oneparse.find('"url":"') > -1):
                onep = json.loads(oneparse)
                if(r_parses.find(onep['url']) == -1 and r_parses_err.find(onep['url']) == -1):
                    ustat = NetFile.url_stat(onep['url'], 60, 60)
                    if(ustat == 404 or ustat == 0):
                        r_parses_err += '\r\n' + str(ustat) + ':' + oneparse + ','
                    else:
                        r_parses += '\r\n' + oneparse + ','
        except Exception as ex:
            LocalFile.write_LogFile('Main-Line-496-Exception:\n' + str(ex) + '\n' + oneparse)
    LocalFile.write_LocalFile('./res/r_parses.txt', r_parses.strip('\r\n'))
    print('Line-561:/res/r_parses.txt已更新。')
    LocalFile.write_LocalFile('./res/r_parses_err.txt', r_parses_err.strip('\r\n'))
    print('Line-563:/res/r_parses_err.txt已更新。')

    # 读取所有节点到allonesite新记录后面。
    # alltypename = LocalFile.read_LocalFile("./res/typename.txt").replace('\r','')
    # tvlists = []
    # with open('./res/tvlist.json', 'r', encoding='utf-8') as f:
    #     tvlists = json.load(f)
    # num_item = len(tvlists)
    # alltv = ''
    # oldtypename = ''
    # for ii in alltypename.split('\n'):
    #     for i in range(num_item):
    #         try:
    #             typename = tvlists[i]['typename'].decode("unicode-escape")
    #             tvname = tvlists[i]['tvname'].decode("unicode-escape")
    #             tvurl = tvlists[i]['tvurl'].decode("unicode-escape")
    #             if(tvname.find(ii) == -1 or typename == ii):
    #                 if(ii == oldtypename):
    #                     alltv += '\r\n' + typename + ',' + tvurl
    #                 else:
    #                     alltv += '\r\n\r\n' + typename + ',#genre#'
    #             # tvname = load_dict[i]['tvname']
    #             # tvmd5 = load_dict[i]['tvmd5']
    #             # tvurl = load_dict[i]['tvurl']
    #         except Exception as ex:
    #             print('Main-Line-102-Exception:' + str(ex) + '\noneesite:' + i)
    # alltv = alltv.strip('\n').encode('utf-8')
    # # allboxs.json = base64.b64encode(boxsites.strip('\n').encode('utf-8')).decode('utf-8')
    # LocalFile.write_LocalFile('./out/all', alltv)
    # print('Line-293-Node整理成功，共有记录' + str(iii) + '条。')


# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if(menu == 'check'):
    try:
        rename = LocalFile.read_LocalFile('./res/rename.txt').replace('\r','').replace('\n\n','\n')
        if(os.path.exists('./out/all')):
            tvbox = LocalFile.read_LocalFile('./out/all').replace('\r','').replace('\n\n','\n')
        else:
            tvbox = LocalFile.read_LocalFile('./res/all').replace('\r','').replace('\n\n','\n')
        r_sites_err = LocalFile.read_LocalFile("./res/r_sites_err.txt")
        addtv = ''
        nsfw = ''
        spare = ''
        for i in tvbox.split('\n'):
            try:
                if(i != '' and r_sites_err.find('"jar":"./') == -1 and r_sites_err.find(i) == -1 and i.find('"key":') > -1 and i.find('"name":') > -1 and i.find('"type":') > -1):
                    ii = i.replace('//{','{').strip(',').replace('"type":0','"type":1')
                    tv = json.loads(ii)
                    # 检查自定义Jar文件是否存在
                    if(ii.find('"jar":"') > -1):
                        jar = tv['jar']
                        if(jar.find('http') == 0):
                            ustat = NetFile.url_stat(jar, 60, 60)
                            if(ustat == 404 or ustat == 0):
                                ii = ii.replace(',"jar":"' + jar + '"', '')
                    # 自定义电影网站名称
                    if(ii.find('"name"') > -1 and ii.find('"key"') > -1 ):
                        if(rename.find(tv['key']) > -1):
                            newname = StrText.get_str_btw(rename.replace('\r',''), tv['key'] + ':', '\n', 0)
                            tv['name'] = newname
                            ii = json.dumps(tv)                              
                    # 过滤重复的电影网站
                    if((addtv + spare + nsfw).find(ii) > -1):
                        continue
                    # 过滤重复Key的电影网站
                    if((addtv + nsfw).find('"key":"' + tv['key'] + '"') > -1):
                        spare += '\r\n' + ii + ','
                        continue
                    # 分类去重
                    id = tv['type']
                    if(id == 1 or id == 4):
                        api = tv['api']
                        if((addtv + nsfw + r_sites_err).find(api) > -1):
                            continue
                        else:
                            if(api.find('http') == 0):
                                ustat = NetFile.url_stat(api, 60, 60)
                                if(ustat == 404 or ustat == 0):
                                    r_sites_err += '\r\n' + str(ustat) + ':' + ii + ','
                                    continue
                    elif(id == 3):
                        if(ii.find('"ext":"') > -1):
                            ext = tv['ext']
                            if((addtv + nsfw + r_sites_err).find(ext) > -1):
                                continue
                            else:
                                if(ext.find('http') == 0):
                                    ustat = NetFile.url_stat(ext, 60, 60)
                                    if(ustat == 404 or ustat == 0):
                                        r_sites_err += '\r\n' + str(ustat) + ':' + ii + ','
                                        continue
                    else:
                        spare += '\r\n' + ii + ','
                    
                    if(tv['name'].find('*') > -1):
                        nsfw += '\r\n' + ii + ','
                    elif(ii.find('"key":') > -1 and ii.find('"name":') > -1 and ii.find('"type":') > -1):
                        addtv += '\r\n' + ii + ','
                else:
                    print('Main-Line-612-not-tvsite-url:' + i)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-614-Exception:' + str(ex) + '\ntvsite:' + i)
        
        LocalFile.write_LocalFile('./res/r_sites_err.txt', r_sites_err.strip('\r\n'))
        print('Line-563:/res/r_sites_err.txt已更新。')

        r_spider = LocalFile.read_LocalFile("./res/r_spider.txt")
        r_spider = '{\r\n//Update:' + str(datetime.datetime.now()) + '\r\n\r\n' + r_spider
        r_lives = LocalFile.read_LocalFile("./res/r_lives.txt")
        r_parses = LocalFile.read_LocalFile("./res/r_parses.txt")
        r_parses = '\r\n\r\n"parses":[\r\n' + r_parses.replace('},\n{','},\r\n{').strip(',') + '\r\n],'
        r_flags = LocalFile.read_LocalFile("./res/r_flags.txt")
        r_flags = '\r\n\r\n' + r_flags
        r_ijk = LocalFile.read_LocalFile("./res/r_ijk.txt").replace('},{','},\r\n{').replace('[{','[\r\n{')
        r_ijk = '\r\n\r\n' + r_ijk
        r_ijk = r_ijk.replace('\r','').replace('\n','\r\n')
        r_ads = LocalFile.read_LocalFile("./res/r_ads.txt")
        r_ads = '\r\n\r\n' + r_ads + '\r\n}'

        r_pushagent = LocalFile.read_LocalFile("./res/r_pushagent.txt")

        LocalFile.write_LocalFile('./out/tvbox.txt', r_spider + '\r\n\r\n' + r_lives + '\r\n\r\n"sites":[' + addtv + '\r\n' + r_pushagent + '\r\n],'
            + r_parses + r_flags + r_ijk + r_ads)
        LocalFile.write_LocalFile('./out/nsfw.txt', r_spider + '\r\n\r\n' + r_lives + '\r\n\r\n"sites":[' + nsfw + '\r\n' + r_pushagent + '\r\n],'
            + r_parses + r_flags + r_ijk + r_ads)
        LocalFile.write_LocalFile('./out/all', '"sites":[\r\n//Update:' + str(datetime.datetime.now()) + '\r\n' + addtv + '\r\n' + nsfw + '\r\n' + spare + '\r\n' + r_pushagent + '\r\n],')
    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-623-Exception:' + str(ex))