'''
多线程获取所有url的标题
'''

# coding: utf-8
from queue import Queue
import time
import threading
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


class A():
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

    def writefile(self,row):
        with open('urls_titles.txt','a+',encoding='gbk') as f:
            f.write(row + '\n')

    def scan(self):
        while True:
            if self.queue.empty():
                exit('empty')

            url = self.queue.get()
            self.request(url.strip())
            # if self.request(url) :
            #     self.lock.acquire()
            #     print(url)
            #     self.lock.release()
            #     time.sleep(0.1)

    def request(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0)',
                        }
        print(url)
        try:
            response = requests.get(url=url, headers=headers, verify=False, timeout=8)
            #print(response)
            if response.status_code == 200 :
                soup = BeautifulSoup(response.text, "html.parser")
                print(soup.title.string)
                print(type(soup.title.string))
                s = ''.join(soup.title.string)
                if s :
                    self.writefile(url + '\t' + s)
                    print(url + '\t' + s)

                return soup.title
                #return response.test

        except Exception as e:
            #print(e)
            return False

    def threads_run(self):
        for i in range(20):
            t = threading.Thread(target=self.scan,)
            t.start()
            #t.join()       #注意这儿一定不能加这个，加了就变成只有线程1执行了

if __name__ == "__main__" :
    A = A('hw_url_2021-05-09_09-17-07.txt')
