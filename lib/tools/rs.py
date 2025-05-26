import requests
from bs4 import BeautifulSoup
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import tldextract
import cloudscraper
from lib.tools.utils import clear, banner, menu_rev
from lib.tools.colors import wh, g, r, yl
import re, os, contextlib

def useragent() -> str:
    useragent = []
    try:
        if not useragent:
            agent = open('lib/files/user-agent.txt', 'r', encoding='utf8').read().splitlines()
            useragent.extend(agent)
        return random.choice(useragent)
    except: 
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'

class tld:
    def extract(domain):
        domain = tldextract.extract(str(domain)).domain + "." + tldextract.extract(str(domain)).suffix
        return domain

class rapiddns:
    def ext_domain(ip):
        hypetime = random.uniform(0.2, 2)
        time.sleep(hypetime)
        endpoint = f"https://rapiddns.io/sameip/{ip}?full=1&t=None#result"
        User_agent = {"User-Agent": random.choice(useragent())}
        try:
            req = requests.get(endpoint, headers=User_agent, timeout=2)
            if "Same IP Website" in req.text:
                soup = BeautifulSoup(req.text, "html.parser")
                table = soup.find("table", {"class": "table table-striped table-bordered"})
                tbody = table.find("tbody")
                tr = tbody.find_all("tr")
                print(f"{r}[+]{g} FROM {yl} {ip}  == DOMAINS{g}[{r}{(len(tr))}{g}]")
                for i in tr:
                    td = i.find_all("td")
                    domain = (tld.extract(td[0].text))
                    save(domain)
            else:
                pass
        except:
            pass

class tntcode:
    def ext_domain(ip):
        endpoint = f"https://domains.tntcode.com/ip/{ip}"
        User_agent = {"User-Agent": random.choice(useragent())}
        try:
            hype = random.uniform(1, 7)
            time.sleep(hype)
            req = cloudscraper.create_scraper()
            req = req.get(endpoint, headers=User_agent, timeout=2)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html.parser")
                textarea = soup.find("textarea")
                domains = textarea.text.split("\n")
                print(f"{r}[+]{g} FROM {yl} {ip}  == DOMAINS{g}[{r}{(len(domains))}{g}]")
                for domain in domains:
                    save(str(domain))
            else:
                pass
        except Exception:
            pass

class spyonweb:
    def ext_domain(ip):
        try:
            hypetime = random.uniform(1, 4)
            time.sleep(hypetime)
            endpoint = f"http://ip.yqie.com/iptodomain.aspx?ip={ip}"
            user_agent = {"User-Agent": random.choice(useragent())}
            req = requests.get(endpoint, headers=user_agent, timeout=2)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html.parser")
                table = soup.find('table', class_='table')
                data_rows = table.find_all('tr')[1:]
                domains = [row.find_all('td')[1].text.strip() for row in data_rows]
                print(f"{r}[+]{g} FROM {yl} {ip}  == DOMAINS{g}[{r}{(len(domains))}{g}]")
                for domain in domains:
                    domain = (tld.extract(domain))
                    save(domain)
            else:
                pass
        except Exception:
            pass

class webscan:
    def ext_domain(ip):
        try:
            url = f"https://api.webscan.cc/?action=query&ip={ip}"
            User_agent = {"User-Agent": random.choice(useragent())}
            response = requests.get(url, headers=User_agent, timeout=2).json()
            for i in range(len(response)):
                domain = response[i]["domain"]
                print(f"{r}[+]{g} FROM {yl} {ip}  == DOMAINS{g}[{r}{(len(domain))}{g}]")
                domains = tld.extract(domain)
                save(domains)
        except Exception:
            pass

class lol1:
    def rev3(ip):
        try:
            req1 = requests.get('https://networksdb.io/domains-on-ip/'+str(ip), timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}).text
            rr = re.findall('<pre class="threecols">.*?</pre>',req1, re.DOTALL)[0]
            rr = rr.replace('<pre class="threecols">','').replace('</pre>','')
            domains = rr.split('\n')
            print(f"{r}[+]{g} FROM {yl} {ip}  == DOMAINS{g}[{r}{(len(domains))}{g}]")
            for domain in domains:
                domain = (tld.extract(domain))
                save(domain)
        except:
            pass

class lol2:
    def rev4(ip):
        try:
            req1 = requests.get('https://www.chaxunle.cn/ip/'+str(ip)+'.html', timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}).text
            rrr = re.findall("https://www.chaxunle.cn/ip/(.*?).html", req1)
            domains = rrr
            print(f"{r}[+]{g} FROM {yl} {ip}  == DOMAINS{g}[{r}{(len(domains))}{g}]")
            for domain in domains:
                domain = (tld.extract(domain))
                save(domain)
        except:
            pass

def save(i):
    mylist = []
    yy = r'Result/reversed.txt'
    with contextlib.suppress(Exception):
        if not i.startswith("http://") and not i.startswith("https://"):
            i = f"http://{i}"
    if not os.path.exists(yy):
        new_file = open('Result/reversed.txt', 'a+', encoding="utf-8", errors="ignore")
        new_file.close()
    if len(mylist) > 1:
        mylist.clear()
        mylist.append(i)
        open(yy, "a+", encoding="utf-8",  errors="ignore").write(i + "\n")
    elif i not in mylist:
        mylist.append(i)
        open(yy, "a+", encoding="utf-8",  errors="ignore").write(i + "\n")


def process_task2(line, q):
    q.put(rapiddns.ext_domain(line.strip()))
    q.put(tntcode.ext_domain(line.strip()))
    q.put(spyonweb.ext_domain(line.strip()))
    q.put(webscan.ext_domain(line.strip()))
    q.put(lol1.rev3(line.strip()))
    q.put(lol2.rev4(line.strip()))

def process_task1(line, q):
    q.put(rapiddns.ext_domain(line.strip()))
    q.put(webscan.ext_domain(line.strip()))
    q.put(lol1.rev3(line.strip()))
    q.put(lol2.rev4(line.strip()))

def worker_proc1(file, thread):
    q = Queue()
    with ThreadPoolExecutor(max_workers=int(thread)) as executor:
        with open(file, "r") as f:
            tasks = [executor.submit(process_task1, line.strip(), q) for line in f]
            for task in as_completed(tasks):
                task.result()
    return q

def worker_proc2(file, thread):
    q = Queue()
    with ThreadPoolExecutor(max_workers=int(thread)) as executor:
        with open(file, "r") as f:
            tasks = [executor.submit(process_task2, line.strip(), q) for line in f]
            for task in as_completed(tasks):
                task.result()
    return q

def func1():
    file = input("\033[97m[\033[92m+\033[97m] GIVE ME IP LIST : ")
    thread = 50
    q = worker_proc1(file, thread)
    while not q.empty():
        print(q.get())

def func2():
    file = input("\033[97m[\033[92m+\033[97m] GIVE ME IP LIST : ")
    thread = 50
    q = worker_proc2(file, thread)
    while not q.empty():
        print(q.get())

def wutwut():
    clear()
    print(banner)
    print(menu_rev)
    while True:
        rev = input("\n\033[97m[\033[92m=\033[97m] Choice : ")
        if rev == "1":
            func1()
            break
        elif rev == "2":
            func2()
            break
        
if __name__ == "__main__":
    wutwut()