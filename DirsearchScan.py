'''
使用dirsearch批量扫描，主要解决dirsearch -l扫描时会报错停掉的问题
'''
import subprocess
import os
import sys


class DirsearchScan:
    def __init__(self, file):
        self.file = file
        self.num = 0
        self.scan()

    def scan(self):
        with open(self.file, 'r') as f:
            for i in f.readlines():
                try:
                    _ = 'python3 dirsearch.py -x 301,302,403,404 -u {0} --full-url --csv-report {1}.csv'.format(i.strip(), self.num)
                    subp = subprocess.run(_, shell=True, timeout=120)
                    self.num += 1
                except subprocess.TimeoutExpired:
                    self.kill_process()
                    os.system('ps aux | grep dirsearch')

    def kill_process(self):
        process = os.popen("ps aux | grep 'dirsearch' | awk '{print $2}'").read()
        os.system('kill -9 {}'.format(process.replace('\n', ' ')))

A = DirsearchScan(sys.argv[1])
