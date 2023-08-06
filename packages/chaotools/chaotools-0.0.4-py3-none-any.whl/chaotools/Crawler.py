import requests
import os
import random
import time
import sqlite3
import threading
import xml.etree.ElementTree as ET
#from fake_useragent import UserAgent 傻逼 fake_useragent，直接本地不行吗，非得从网上下载，运行程序半天没反应就是在等你个憨批在下载
requests.packages.urllib3.disable_warnings()    #关闭警告
#python setup.py sdist bdist_wheel
#twine upload dist/*
class Crawler:
    SimpleHeaders = {
        "Host": "",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.198Safari/537.36",
        "Accept": "*/*",
        "Cookie": ""
    }
    Headers = {
        "Host": "",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.198Safari/537.36",
        "Accept": "*/*",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Referer": "",
        "Origin": "",
        "Content-Length": "",
        "Content-Type": "",
        "Cookie": ""
    }
    def __init__(self,filename,sqlcreate,info,threadnum=1,timeout=20,sleeptime=1,maxtrynum=5):
        '''
        初始化爬虫配置
        :param url:
        :param filename:
        :param sqlsave:
        :param sqlcreate:
        :param info:
        :param threadnum:
        :param timeout:
        :param sleeptime:
        :param maxtrynum:
        '''
        self.filename=filename
        self.timeout = timeout
        self.threadnum=threadnum
        self.sleeptime=sleeptime
        self.maxtrynum=maxtrynum
        self.sqlcreate = sqlcreate
        self.info = info
        self.semphore = threading.Semaphore(self.threadnum)
        self.lockdb = threading.Lock()
        self.locklog = threading.Lock()
        if not os.path.exists("log"):os.mkdir('log')


    def parse(self):
        pass

    def getHeaders(self):
        return Crawler.SimpleHeaders

    def getproxies (self):
        proxies ={
            "http": "http://127.0.0.1:10808", "https": "https://127.0.0.1:10808"
        }
        return proxies

    def print_and_log(self,msg):
        print(msg)
        self.log(msg)

    def error(self,msg):
        print(msg)
        msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  + " => "  + msg
        errorpath = os.path.join(os.getcwd(), "log", time.strftime("%Y-%m-%d", time.localtime()) + '_error.txt')
        if self.locklog.acquire():
            with open(errorpath, 'a', encoding='utf-8') as f:
                f.write('\n' + msg)
            self.locklog.release()

    def log(self,msg):
        msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  + " => "  + msg
        logpath=os.path.join(os.getcwd(),"log",time.strftime("%Y-%m-%d", time.localtime())+'.txt')
        if self.locklog.acquire():
            with open(logpath, 'a', encoding='utf-8') as f:
                f.write('\n' + msg)
            self.locklog.release()

    def randomsleep(self,max):
        if max==0:return
        elif max>=1:
            sleeptime = float(format(random.randint(max - 1, max + 1) + random.random(), '1.2f'))
            time.sleep(sleeptime)

    def createsqlite(self):
        conn = sqlite3.connect(f"{self.filename}.db")
        c = conn.cursor()
        c.execute(self.sqlcreate)
        conn.commit()
        conn.close()
        print("成功创建表")


    def infotosql(self):
        pass

    def save(self,info):
        '''
        sqltext = f"INSERT OR IGNORE INTO info (link,releasedate,content,magnet,attach) " \
                  f"VALUES ('{info['link']}','{info['releasedate']}', '{info['content']}', '{info['magnet']}', '{info['attach']}')"
        '''
        if self.lockdb.acquire():
            conn = sqlite3.connect(f'{self.filename}.db')
            cursor = conn.cursor()
            cursor.execute(self.infotosql(info))
            conn.commit()
            conn.close()
            self.lockdb.release()
            self.log("成功保存到数据库")

    def read(self,tablename):
        '''
        info = {"link": "", "type": "", "reply": 0, "view": 0, "releasedate": "", "lastcommentdate": "",
                "hasimg": False, "attach": False, "score": False, "hot": 0, "title": ""}
        '''
        conn = sqlite3.connect(f"{self.filename}.db")
        c = conn.cursor()
        c.execute(f"SELECT * FROM {tablename}")
        result = c.fetchall()
        conn.close()
        infos = []
        keys=list(self.info.keys())
        for i in range(len(result)):
            info = {}
            for j in range(len(keys)):
                info[keys[j]]=result[i][j]
            infos.append(info)
        return infos

    def crawlwithsemphore(self,i,maxcount,url):
        if self.semphore.acquire():
            print(f"{str(i+1)}/{maxcount}:{url}")
            success = False
            trynum = 0  # 设置最大请求次数
            while not success and trynum<=self.maxtrynum:
                try:
                    r = requests.get(url, headers=self.getHeaders(), verify=False, timeout=self.timeout)
                    r.encoding = 'UTF-8'
                    success = True
                    trynum += 1
                except requests.exceptions.ConnectTimeout as e1:
                    # 超时
                    self.print_and_log(str(e1))
                    trynum+=1
                except requests.exceptions.ConnectionError as e2:
                    # 远程主机强迫关闭了一个现有的连接
                    self.print_and_log(str(e2))
                    trynum += 1
                except Exception as e:
                    self.print_and_log(str(e))
                    trynum += 1
            if success:
                sourcecode = r.text
                if r.status_code == 200 and sourcecode != "":
                    self.save(self.parse(sourcecode,url))
                else:
                    self.error("错误：" + str(r.status_code))
            else:
                self.error("无法访问：" + url)
            self.randomsleep(self.sleeptime)
            self.semphore.release()

    def crawl(self,urls):
        if not os.path.exists(f'{self.filename}.db'): self.createsqlite()
        for i in range(len(urls)):
            t=threading.Thread(target=self.crawlwithsemphore,args=(i,len(urls),urls[i]))
            t.start()