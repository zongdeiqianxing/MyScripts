'''
多线程批量扫描svn和git目录泄露
python3 svn_git_scan.py 1.txt
'''

from queue import Queue
import time
import threading
import requests
from urllib.parse import urljoin
import warnings
import sys
warnings.filterwarnings("ignore")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0)',}

class Scan():
    def __init__(self,file):
        self.queue = Queue()
        self.file = file
        self.readfile()

        self.lock = threading.Lock()
        self.threads_run()

    def readfile(self):
        with open(self.file,'r') as f:
            for i in f.readlines():
                if not i.startswith('http'):
                    i = 'http://' + i

                self.queue.put(i)

    def writefile(self,file,row):
        with open(file,'a+',encoding='gbk') as f:
            f.write(row)

    def scan(self):
        while True:
            if self.queue.empty():
                exit('empty')

            url = self.queue.get()
            self.git_request(url)
            self.svn_request(url)

    def git_request(self,url):
        url = urljoin(url.strip(),'/.git/config')
        print('gitscan : ' + url)
        try:
            response = requests.get(url=url, headers=headers, verify=False, timeout=5)
            #print(response)
            if response.status_code == 200 and  r'[remote' in response.text:
                self.writefile('gitscan_result.txt',url)
                print(url+' **'*20)
                return True

        except Exception as e:
            #print(e)
            return False

    def svn_request(self,url):
        url = urljoin(url.strip(),'/.svn/entries')
        print('svnscan : ' + url)
        try:
            response = requests.get(url=url, headers=headers, verify=False, timeout=5)
            #print(response)
            if response.status_code == 200 :
                self.writefile('svnscan_result.txt',url+'\n')
                print(url+' **'*20)
                return True

        except Exception as e:
            #print(e)
            return False

    def threads_run(self):
        for i in range(20):
            t = threading.Thread(target=self.scan,)
            t.start()

if __name__ == "__main__" :
    #A = A('hw_url_2021-05-09_09-17-07.txt')
    if not sys.argv[1]:
        print('usage: python3 git_svn_scan.py xx.txt')

    A = Scan(sys.argv[1])
