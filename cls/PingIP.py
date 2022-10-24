#!/usr/bin/env python3

import base64
import json
import requests
import socket
import subprocess
import time
#import logging
#logger = logging.getLogger("Sub")
from cls.LocalFile import LocalFile
from cls.IsValid import IsValid
from cls.StrText import StrText

class PingIP():
    def tcp_ping(host, port):
        alt=0
        suc=0
        fac=0
        _list = []
        while True:
            if fac >= 3 or (suc != 0 and fac + suc >= 10):
                break
        #	logger.debug("fac: {}, suc: {}".format(fac, suc))
            try:
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                st=time.time()
                s.settimeout(3)
                s.connect((host, int(port)))
                s.close()
                deltaTime = time.time()-st
                alt += deltaTime
                suc += 1
                _list.append(deltaTime)
            except (socket.timeout):
                fac+=1
                _list.append(0)
                #logger.warn("TCP Ping (%s,%d) Timeout %d times." % (host,port,fac))
                print("TCP Ping Timeout %d times." % fac)
            except Exception as ex:
                #logger.exception("TCP Ping Exception:")
                #print("TCP Ping Exception:" + str(ex))
                _list.append(0)
                fac+=1
        if suc==0:
        #    return (0,0,_list)
            return suc
        #return (alt/suc,suc/(suc+fac),_list)
        mstime = int(alt*1000/suc)
        return mstime

    def google_ping(address, port=1080):
        alt=0
        suc=0
        fac=0
        _list = []
        while True:
            if fac >= 3 or (suc != 0 and fac + suc >= 10):
                break
            try:
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((address,port))
                st=time.time()
                s.send(b"\x05\x01\x00")
                s.recv(2)
                s.send(b"\x05\x01\x00\x03\x0agoogle.com\x00\x50")
                s.recv(10)
                s.send(b"GET / HTTP/1.1\r\nHost: google.com\r\nUser-Agent: curl/11.45.14\r\n\r\n")
                s.recv(1)
                s.close()
                deltaTime = time.time()-st
                alt += deltaTime
                suc += 1
                _list.append(deltaTime)
            except (socket.timeout):
                fac += 1
                _list.append(0)
                #logger.warn("Google Ping Timeout %d times." % (fac))
            except Exception:
                print("Google Ping Exception:")
                _list.append(0)
                fac += 1
        if (suc == 0):
            return (0,0,_list)
        return (alt/suc,suc/(suc+fac),_list)

    def get_ping_time(ip):
        num = 0
        try:
            result = subprocess.call('ping -w 1000 -n 1 ' + ip,stdout=subprocess.PIPE,shell=True)
            if result == 0:
                h = subprocess.getoutput('ping ' + ip)
                num = h.split('平均 = ')[1].replace('ms', '')
        except:
            num = 0
        return num

    def check_alive(ip):
        result = subprocess.call('ping -w 1000 -n 1 %s' %ip,stdout=subprocess.PIPE,shell=True)
        if result == 0:
            h = subprocess.getoutput('ping ' + ip)
            returnnum = h.split('平均 = ')[1]
            info = ('\033[32m%s\033[0m 能ping通，延迟平均值为：%s' %(ip,returnnum))
            print('\033[32m%s\033[0m 能ping通，延迟平均值为：%s' %(ip,returnnum))
            #return info
        else:
            with open('notong.txt','a') as f:
                f.write(ip)
            info = ('\033[31m%s\033[0m ping 不通！' % ip)
            #return info
            print('\033[31m%s\033[0m ping 不通！' % ip)
            
    def nodespeedtest(confile):
        # 启动v2ray
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","--config","%s/clients/config.json" % os.getcwd()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","--config","{}/clients/config.json".format(os.getcwd())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray.exe","--config","{}/clients/config.json".format(os.getcwd())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","--config","%s/clients/config.json" % os.getcwd()])
        # s = subprocess.Popen(["./clients/xray/xray.exe","--config","{}/clients/config.json".format(os.getcwd())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # s = subprocess.Popen(["./clients/xray/xray","--config","%s/clients/config.json" % os.getcwd()])
        # s = subprocess.Popen(["./clients/xray/xray","--config","/mnt/mmcblk2p4/NodeSpeed/clients/config.json"])
        # s = subprocess.Popen(["./clients/xray/xray --config /mnt/mmcblk2p4/NodeSpeed/clients/config.json"])
        # s = subprocess.Popen("./clients/xray/xray --config /mnt/mmcblk2p4/NodeSpeed/clients/config.json" shell=True)
        # s = subprocess.Popen(["./clients/xray/xray", "--config", "/mnt/mmcblk2p4/NodeSpeed/clients/config.json"])
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","--config","/mnt/mmcblk2p4/NodeSpeed/clients/config.json"],shell=True,stdout=subprocess.PIPE)
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","--config","/mnt/mmcblk2p4/NodeSpeed/clients/config.json"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print('confile:' + confile)        
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","config","/mnt/mmcblk2p4/NodeSpeed/clients/v2ray-core/config.json"])
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","--config","%s/config.json" % os.getcwd()])
        # s = subprocess..Popen(["./clients/v2ray-core/v2ray","--config","%s/config.json" % os.getcwd()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray","--config",confile])
        # s = subprocess.Popen(["./clients/v2ray-core/v2ray test /mnt/mmcblk2p4/NodeSpeed/clients/v2ray-core/config.json"])
        s = subprocess.Popen(["./clients/v2ray-core/v2ray","run","/mnt/mmcblk2p4/NodeSpeed/clients/v2ray-core/config.json"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        print('s.pid:' + str(s.pid))
        time.sleep(2)
        '''
        serverStr = '127.0.0.1'
        port = 8080
        proxies = {'http': 'http://localhost:' + str(port),
                    'https': 'http://localhost:' + str(port)}
        #proxies = {'http': 'http://' + serverStr + ':' + str(port),
        #            'https': 'http://' + serverStr + ':' + str(port)}
        session = requests.Session()
        session.proxies.update(proxies)
        url = 'https://policies.google.com/terms?hl=zh-CN&fg=1#toc-intro'
        html = session.get(url).text
        print(html)

        TIME_OUT_RPing = 100
        URL_webtest = 'https://www.google.com/generate_204'
        try:
            response = session.get(URL_webtest,timeout= TIME_OUT_RPing*2);
            response = session.get(URL_webtest,timeout= TIME_OUT_RPing);
            tDelay = response.elapsed.total_seconds()*1000
            print('tDelay:' + str(tDelay))
        except Exception as e:
            print('wSpeed response Error end at port: %s with host: %s'           % ( port, serverStr))
            #configJson['RPingTime'] = float("inf")
            #return -1

        url = 'http://clients3.google.com/generate_204'
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 204:
                print(response.status_code)
                response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)

        print("开始批量ping所有IP！")
        with open('ip.txt', 'r') as f:      #ip.txt为本地文件记录所有需要检测连通性的ip
            for i in f:
                p = multiprocessing.Process(target=PingIP.check_alive, args=(i,))
                #p.start()

        print('查询域名IP-' + IpAddress.get_country('www.baidu.com'))
        '''
        # socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1087)
        # socket.socket = socks.socksocket

        delay = -1
        filesize = 0
        deltaTime = 0
        st = time.time()
        '''
        try:
            s = requests.session()
            s.proxies = {'http': 'socks5://127.0.0.1:1087'}
            s.headers = {'Connection':'close'}
            s.keep_alive = False
            print('S-CONT-LEN:' + str(len(s.get('https://www.baidu.com/').text)))
        except Exception as ex:
            time.sleep(3)
            print('Line-500-Exception:' + str(ex))
        '''        
        try:
            serverStr = '127.0.0.1'
            port = 1087
            session = requests.Session()
            #proxies = {'http': 'http://localhost:' + str(port),
            #            'https': 'http://localhost:' + str(port)}
            #session.proxies.update(proxies)
            
            #session.proxies = {'http': 'socks5://localhost:' + str(port)}
            session.proxies = {'http': 'socks5://' + serverStr + ':' + str(port)}
            session.headers = {"Connection":"close"}
            session.keep_alive = False # 关闭多余连接

            # url = 'https://policies.google.com/terms?hl=zh-CN&fg=1#toc-intro'
            # url = 'https://www.baidu.com'
            url = 'https://cachefly.cachefly.net/1mb.test'
            # rq = session.get(url, timeout = 20)
            rq = session.get(url, timeout = 20)
            rq.encoding = "utf-8"
            if (rq.status_code == 200):
                #filez = rq.text
                filesize = len(rq.text)
                deltaTime = time.time() - st
                #filesize = 1048576
                #filesize = 341553
                if(filesize >= 1048000):
                    delay = int(filesize / 1024 / deltaTime)
                else:
                    delay = 0
            else:
                delay = 0
            print('rq.status_code-[' + str(rq.status_code) + ']-filesize-[' + str(filesize) + ']-deltaTime-[' + str(deltaTime) + ']-kbs-[' + str(delay) + 'KB/s]')
            time.sleep(3)
            session.close()
            s.kill()
            # s.kill(SIGKILL)
            # os.killpg(p.pid, signal.SIGUSR1)
        except Exception as ex:
            time.sleep(3)
            print('Down-File-is-False:filesize-[' + str(filesize) + ']-deltaTime:[' + str(deltaTime) + ']-delay-[' + str(delay) + ']-Exception:\n' + str(ex))
        return delay

    def node_config_json(j, confile):
        try:
            if(j.find('ss://') == 0):
                onenode = j.split("#", 1) # 第二个参数为 1，返回两个参数列表
                oldname = onenode[1]
                onenode = (base64.b64decode(onenode[0][5:].encode("utf-8")).decode("utf-8"))
                # chacha20-ietf-poly1305:12f4863a-b470-40c9-8c3a-47606b1012b5@n18.emovpn.xyz:443
                port = onenode.rsplit(':', 1)[1]
                address = StrText.get_str_btw(onenode, "@", ":")
                method = onenode.split(':', 1)[0]
                password = StrText.get_str_btw(onenode, ":", "@")

                onenode = '	"outbound": {\n'
                onenode = onenode + '		"protocol": "shadowsocks",\n'
                onenode = onenode + '		"settings": {\n'
                onenode = onenode + '			"servers":\n'
                onenode = onenode + '			[\n'
                onenode = onenode + '				{\n'
                onenode = onenode + '					"email": "love@v2ray.com",\n'
                onenode = onenode + '					"address": "' + address + '",\n'
                onenode = onenode + '					"port": ' + port + ',\n'
                onenode = onenode + '					"method": "' + method + '",\n'
                onenode = onenode + '					"password": "' + password + '",\n'
                onenode = onenode + '					"ota": false,\n'
                onenode = onenode + '					"level": 0\n'
                onenode = onenode + '				}\n'
                onenode = onenode + '			]\n'
                onenode = onenode + '		}\n'
                onenode = onenode + '	},'
            elif(j.find('trojan://') == 0):
                #trojan://8cf83f44-79ff-4e50-be1a-585c82338912@t2.ssrsub.com:8443?sni=douyincdn.com#name
                onenode = j[9:].replace('?', '#')
                password = onenode.split('@', 1)[0]
                address = StrText.get_str_btw(onenode, '@', ':')
                if(onenode.find('#') == -1):
                    onenode = onenode + '#' + address
                port = StrText.get_str_btw(onenode, ':', '#')
                sni = ''
                if(onenode.find('sni') > -1):
                    sni = StrText.get_str_btw(onenode, 'sni=', '#')

                onenode = '	"outbound": {\n'
                onenode = onenode + '		"protocol": "trojan",\n'
                onenode = onenode + '		"settings": {\n'
                onenode = onenode + '			"servers":\n'
                onenode = onenode + '			[\n'
                onenode = onenode + '				{\n'
                onenode = onenode + '					"email": "love@v2ray.com",\n'
                onenode = onenode + '					"address": "' + address + '",\n'
                onenode = onenode + '					"port": ' + port + ',\n'
                onenode = onenode + '					"password": "' + password + '",\n'
                onenode = onenode + '					"level": 0\n'
                onenode = onenode + '				}\n'
                onenode = onenode + '			]\n'
                onenode = onenode + '		},\n'
                onenode = onenode + '		"streamSettings": {\n'
                if(sni != ''):
                    onenode = onenode + '			"security": "tcp",\n'
                    onenode = onenode + '			"security": "tls",\n'
                    onenode = onenode + '			"sni": "' + sni + '"\n'
                onenode = onenode + '		}\n'
                onenode = onenode + '	},'
            elif(j.find('vmess://') == 0):
                aonenode = (base64.b64decode(j[8:].encode("utf-8")).decode("utf-8"))
                '''
                {
                    "v": "2",
                    "ps": "-美国-137.175.30.251",
                    "add": "137.175.30.251",
                    "port": "111",
                    "id": "77cd775c-1c0a-11ec-a1a8-00163c1393a8",
                    "aid": "0",
                    "scy": "auto",
                    "net": "tcp",
                    "type": "vmess",
                    "host": "",
                    "path": "/",
                    "tls": "",
                    "sni": ""
                }
                {
                    "v": "2",
                    "ps": "https://1808.ga",
                    "add": "ff5.uuv2.co.uk",
                    "port": "80",
                    "id": "fbf53107-1b42-3da5-a77d-6ad22544c0e9",
                    "aid": "2",
                    "scy": "auto",
                    "net": "ws",
                    "type": "none",
                    "host": "t.me/vpnhat",
                    "path": "/v2ray",
                    "tls": "none",
                    "sni": ""
                }                
                "streamSettings": {
                    "network": "ws",
                    "security": "tls",
                    "wsSettings": {
                        "path": "/ws",
                        "headers": {
                        "host": "tls.glloyd.com"
                        }
                    }
                }
                '''
                node = json.loads(aonenode)

                onenode = '	"outbound": {\n'
                onenode = onenode + '        "protocol": "vmess",\n'
                onenode = onenode + '        "settings": {\n'
                onenode = onenode + '            "vnext":\n'
                onenode = onenode + '            [\n'
                onenode = onenode + '                {\n'
                onenode = onenode + '                    "address": "' + node['add'] + '",\n'
                onenode = onenode + '                    "port": ' + node['port'] + ',\n'
                onenode = onenode + '                    "users": [{"id": "' + node['id'] + '", "alterId": ' + node['aid'] + ', "security": "' + node['scy'] + '", "level": 0}]\n'
                onenode = onenode + '                }\n'
                onenode = onenode + '            ],\n'
                onenode = onenode + '            "servers": null,\n'
                onenode = onenode + '            "response": null\n'
                onenode = onenode + '        },\n'
                onenode = onenode + '        "streamSettings":\n'
                onenode = onenode + '        {\n'
                onenode = onenode + '            "network": "' + node['net'] + '",\n'
                if(node['tls'] == 'tls' or node['tls'] == 'True' or node['tls'] == 'true'):
                    onenode = onenode + '            "security": "tls",\n'
                    if(aonenode.find('"sni":') > -1):
                        onenode = onenode + '            "sni":"' + node['sni'] + '",\n'
                    if(aonenode.find('certificateFile') > -1 and aonenode.find('keyFile:') > -1):
                        onenode = onenode + '            "tlsSettings": {\n'
                        onenode = onenode + '                "certificates": [\n'
                        onenode = onenode + '                "{\n'
                        onenode = onenode + '                "    "certificateFile": "/etc/v2ray/v2ray.crt", // 证书文件 \n'
                        onenode = onenode + '                "    "keyFile": "/etc/v2ray/v2ray.key" // 密钥文件 \n'
                        onenode = onenode + '                "}]\n'
                        onenode = onenode + '            },\n'
                    else: #none ''
                        onenode = onenode + '            "tlsSettings": {},\n'
                else:
                    onenode = onenode + '            "security": "none",\n'
                # 不同传输协议，配置不同信息
                if(node['net'] == 'tcp'):
                    onenode = onenode + '            "tcpSettings": {}\n'
                elif(node['net'] == 'kcp'):
                    onenode = onenode + '            "kcpSettings": {}\n'
                elif(node['net'] == 'ws'):
                    onenode = onenode + '            "wsSettings": \n'
                    onenode = onenode + '            {\n'
                    if(aonenode.find('"path":') > -1 and aonenode.find('"ws-headers":') > -1):
                        onenode = onenode + '                "path": "' + node['path'] + '",\n'
                        if(aonenode.find('"ws-headers":') > -1 and aonenode.find('"Host":') > -1):
                            onenode = onenode + '                "headers": {"host": "' + node['Host'] + '"}\n'
                        elif(aonenode.find('"ws-headers":') > -1 and aonenode.find('"host":') > -1):
                            onenode = onenode + '                "headers": {"host": "' + node['host'] + '"}\n'
                        elif(aonenode.find('"ws-headers":') > -1 and aonenode.find('"HOST":') > -1):
                            onenode = onenode + '                "headers": {"host": "' + node['HOST'] + '"}\n'
                    else:
                        if(aonenode.find('"path":') > -1):
                            onenode = onenode + '                "path": "' + node['path'] + '"\n'
                        elif(aonenode.find('"ws-headers":') > -1):
                            if(aonenode.find('"ws-headers":') > -1 and aonenode.find('"Host":') > -1):
                                onenode = onenode + '                "headers": {"host": "' + node['Host'] + '"}\n'
                            elif(aonenode.find('"ws-headers":') > -1 and aonenode.find('"host":') > -1):
                                onenode = onenode + '                "headers": {"host": "' + node['host'] + '"}\n'
                            elif(aonenode.find('"ws-headers":') > -1 and aonenode.find('"HOST":') > -1):
                                onenode = onenode + '                "headers": {"host": "' + node['HOST'] + '"}\n'
                    onenode = onenode + '            }\n'
                elif(node['net'] == 'quic'):
                    onenode = onenode + '            "quicSettings": {}\n'
                elif(node['net'] == 'grpc'):
                    onenode = onenode + '            "grpcSettings": {\n'
                    onenode = onenode + '                "serviceName": "" //填写你的 ServiceName\n'
                    onenode = onenode + '            }\n'
                #if(node['net'] == 'http'):
                #onenode = onenode + '            "httpSettings":{\n'
                #onenode = onenode + '                "path": "' + node['path'] + '"\n'
                #onenode = onenode + '            },\n'
                onenode = onenode + '		}\n'
                onenode = onenode + '	},'

            log = LocalFile.read_LocalFile('./res/config-log.json')
            inbound = LocalFile.read_LocalFile('./res/config-inbound.json')
            levels = LocalFile.read_LocalFile("./res/config-levels.json")
            onenode = log + '\n' + inbound + '\n' + onenode + '\n' + levels
            print('开始生成节点文件:' + confile)
            LocalFile.write_LocalFile(confile, onenode)
            time.sleep(2)
        except Exception as ex:
            print('Create-File-Config-Exception:\n' + str(ex))
        return onenode