import os
import re
import requests
from colorama import Fore, init
from multiprocessing.dummy import Pool
from lib.tools.utils import clear, banner
from lib.tools.colors import wh, r, g
from urllib.parse import urlparse

init(convert=True)

class settings:
    y = Fore.YELLOW
    r = Fore.RED
    b = Fore.BLUE

def clean():
    lines_seen = set()
    outfile = open('Result/sites.txt', "a")
    infile = open('Result/sitelist.txt', "r")
    for line in infile:
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    infile.close()
    if os.name == "nt":
        os.system("del Result/sitelist.txt")
    else:
        os.system("rm -rf Result/sitelist.txt")
    print(f"{wh}{g}+{wh}] Duplicate sites removed successfully!")
    print(f"{wh}{g}+{wh}]  Sites saved as {g}Result/sites.txt!")

binglist = [
"http://www.bing.com/search?q=&count=50&first=1",
"http://www.bing.com/search?q=&count=50&first=51",
"http://www.bing.com/search?q=&count=50&first=101",
"http://www.bing.com/search?q=&count=50&first=151",
"http://www.bing.com/search?q=&count=50&first=201",
"http://www.bing.com.br/search?q=&count=50&first=1",
"http://www.bing.com.br/search?q=&count=50&first=51",
"http://www.bing.com.br/search?q=&count=50&first=101",
"http://www.bing.at/search?q=&count=50&first=1",
"http://www.bing.at/search?q=&count=50&first=51",
"http://www.bing.at/search?q=&count=50&first=101",
"http://www.bing.be/search?q=&count=50&first=1",
"http://www.bing.be/search?q=&count=50&first=51",
"http://www.bing.be/search?q=&count=50&first=101",
"http://www.bing.cl/search?q=&count=50&first=1",
"http://www.bing.cl/search?q=&count=50&first=51",
"http://www.bing.cl/search?q=&count=50&first=101",
"http://www.bing.co.at/search?q=&count=50&first=1",
"http://www.bing.co.at/search?q=&count=50&first=51",
"http://www.bing.co.at/search?q=&count=50&first=101",
"http://www.bing.com.au/search?q=&count=50&first=1",
"http://www.bing.com.au/search?q=&count=50&first=51",
"http://www.bing.com.au/search?q=&count=50&first=101",
"http://www.bing.com.cn/search?q=&count=50&first=1",
"http://www.bing.com.cn/search?q=&count=50&first=51",
"http://www.bing.com.cn/search?q=&count=50&first=101",
"http://www.bing.cz/search?q=&count=50&first=1",
"http://www.bing.cz/search?q=&count=50&first=51",
"http://www.bing.cz/search?q=&count=50&first=101",
"http://www.bing.de/search?q=&count=50&first=1",
"http://www.bing.de/search?q=&count=50&first=51",
"http://www.bing.de/search?q=&count=50&first=101",
"http://www.bing.dk/search?q=&count=50&first=1",
"http://www.bing.dk/search?q=&count=50&first=51",
"http://www.bing.dk/search?q=&count=50&first=101",
"http://www.bing.ca/search?q=&count=50&first=1",
"http://www.bing.ca/search?q=&count=50&first=51",
"http://www.bing.ca/search?q=&count=50&first=101",
"http://www.bing.sg/search?q=&count=50&first=1",
"http://www.bing.sg/search?q=&count=50&first=51",
"http://www.bing.sg/search?q=&count=50&first=101",
"http://www.bing.se/search?q=&count=50&first=1",
"http://www.bing.se/search?q=&count=50&first=51",
"http://www.bing.se/search?q=&count=50&first=101",
"http://www.bing.pl/search?q=&count=50&first=1",
"http://www.bing.pl/search?q=&count=50&first=51",
"http://www.bing.pl/search?q=&count=50&first=101",
"http://www.bing.no/search?q=&count=50&first=1",
"http://www.bing.no/search?q=&count=50&first=51",
"http://www.bing.no/search?q=&count=50&first=101",
"http://www.bing.nl/search?q=&count=50&first=1",
"http://www.bing.nl/search?q=&count=50&first=51",
"http://www.bing.nl/search?q=&count=50&first=101",
"http://www.bing.net.nz/search?q=&count=50&first=1",
"http://www.bing.net.nz/search?q=&count=50&first=51",
"http://www.bing.net.nz/search?q=&count=50&first=101",
"http://www.bing.lv/search?q=&count=50&first=1",
"http://www.bing.lv/search?q=&count=50&first=51",
"http://www.bing.lv/search?q=&count=50&first=101",
"http://www.bing.lt/search?q=&count=50&first=1",
"http://www.bing.lt/search?q=&count=50&first=51",
"http://www.bing.lt/search?q=&count=50&first=101",
"http://www.bing.it/search?q=&count=50&first=1",
"http://www.bing.it/search?q=&count=50&first=51",
"http://www.bing.it/search?q=&count=50&first=101",
"http://www.bing.is/search?q=&count=50&first=1",
"http://www.bing.is/search?q=&count=50&first=51",
"http://www.bing.is/search?q=&count=50&first=101",
"http://www.bing.in/search?q=&count=50&first=1",
"http://www.bing.in/search?q=&count=50&first=51",
"http://www.bing.in/search?q=&count=50&first=101",
"http://www.bing.ie/search?q=&count=50&first=1",
"http://www.bing.ie/search?q=&count=50&first=51",
"http://www.bing.ie/search?q=&count=50&first=101",
"http://www.bing.hu/search?q=&count=50&first=1",
"http://www.bing.hu/search?q=&count=50&first=51",
"http://www.bing.hu/search?q=&count=50&first=101",
"http://www.bing.fr/search?q=&count=50&first=1",
"http://www.bing.fr/search?q=&count=50&first=51",
"http://www.bing.fr/search?q=&count=50&first=101",
"http://www.bing.com.sg/search?q=&count=50&first=1",
"http://www.bing.com.sg/search?q=&count=50&first=51",
"http://www.bing.com.sg/search?q=&count=50&first=101",
"http://www.bing.co.uk/search?q=&count=50&first=1",
"http://www.bing.co.uk/search?q=&count=50&first=51",
"http://www.bing.co.uk/search?q=&count=50&first=101",
"http://www.bing.co.nz/search?q=&count=50&first=1",
"http://www.bing.co.nz/search?q=&count=50&first=51",
"http://www.bing.co.nz/search?q=&count=50&first=101",
"http://www.bing.co.jp/search?q=&count=50&first=1",
"http://www.bing.co.jp/search?q=&count=50&first=51",
"http://www.bing.co.jp/search?q=&count=50&first=101",
"http://www.bing.ch/search?q=&count=50&first=1",
"http://www.bing.ch/search?q=&count=50&first=51",
"http://www.bing.ch/search?q=&count=50&first=101",
"http://www.bing.com.tr/search?q=&count=50&first=1",
"http://www.bing.com.tr/search?q=&count=50&first=51",
"http://www.bing.com.tr/search?q=&count=50&first=101",
"http://www.bing.com.pr/search?q=&count=50&first=1",
"http://www.bing.com.pr/search?q=&count=50&first=51",
"http://www.bing.com.pr/search?q=&count=50&first=101",
"http://www.bing.com.ar/search?q=&count=50&first=1",
"http://www.bing.com.ar/search?q=&count=50&first=51",
"http://www.bing.com.ar/search?q=&count=50&first=101",
"http://www.bing.com.co/search?q=&count=50&first=1",
"http://www.bing.com.co/search?q=&count=50&first=51",
"http://www.bing.com.co/search?q=&count=50&first=101",
"http://www.bing.com.es/search?q=&count=50&first=1",
"http://www.bing.com.es/search?q=&count=50&first=51",
"http://www.bing.com.es/search?q=&count=50&first=101",
"http://www.bing.fi/search?q=&count=50&first=1",
"http://www.bing.fi/search?q=&count=50&first=51",
"http://www.bing.fi/search?q=&count=50&first=101",
"http://www.bing.bo/search?q=&count=50&first=1",
"http://www.bing.bo/search?q=&count=50&first=51",
"http://www.bing.bo/search?q=&count=50&first=101",
"http://www.bing.com.do/search?q=&count=50&first=1",
"http://www.bing.com.do/search?q=&count=50&first=51",
"http://www.bing.com.do/search?q=&count=50&first=101",
"http://www.bing.gr/search?q=&count=50&first=1",
"http://www.bing.gr/search?q=&count=50&first=51",
"http://www.bing.gr/search?q=&count=50&first=101",
"http://www.bing.com.hk/search?q=&count=50&first=1",
"http://www.bing.com.hk/search?q=&count=50&first=51",
"http://www.bing.com.hk/search?q=&count=50&first=101",
"http://www.bing.com.hr/search?q=&count=50&first=1",
"http://www.bing.com.hr/search?q=&count=50&first=51",
"http://www.bing.com.hr/search?q=&count=50&first=101",
"http://www.bing.com.mx/search?q=&count=50&first=1",
"http://www.bing.com.mx/search?q=&count=50&first=51",
"http://www.bing.com.mx/search?q=&count=50&first=101",
"http://www.bing.com.my/search?q=&count=50&first=1",
"http://www.bing.com.my/search?q=&count=50&first=51",
"http://www.bing.com.my/search?q=&count=50&first=101",
"http://www.bing.ph/search?q=&count=50&first=1",
"http://www.bing.ph/search?q=&count=50&first=51",
"http://www.bing.ph/search?q=&count=50&first=101",
"http://www.bing.com.pr/search?q=&count=50&first=1",
"http://www.bing.com.pr/search?q=&count=50&first=51",
"http://www.bing.com.pr/search?q=&count=50&first=101",
"http://www.bing.pt/search?q=&count=50&first=1",
"http://www.bing.pt/search?q=&count=50&first=51",
"http://www.bing.pt/search?q=&count=50&first=101",
"http://www.bing.com.ro/search?q=&count=50&first=1",
"http://www.bing.com.ro/search?q=&count=50&first=51",
"http://www.bing.com.ro/search?q=&count=50&first=101",
"http://www.bing.ru/search?q=&count=50&first=1",
"http://www.bing.ru/search?q=&count=50&first=51",
"http://www.bing.ru/search?q=&count=50&first=101",
"http://www.bing.com.sa/search?q=&count=50&first=1",
"http://www.bing.com.sa/search?q=&count=50&first=51",
"http://www.bing.com.sa/search?q=&count=50&first=101",
"http://www.bing.si/search?q=&count=50&first=1",
"http://www.bing.si/search?q=&count=50&first=51",
"http://www.bing.si/search?q=&count=50&first=101",
"http://www.bing.sk/search?q=&count=50&first=1",
"http://www.bing.sk/search?q=&count=50&first=51",
"http://www.bing.sk/search?q=&count=50&first=101",
"http://www.bing.com.ua/search?q=&count=50&first=1",
"http://www.bing.com.ua/search?q=&count=50&first=51",
"http://www.bing.com.ua/search?q=&count=50&first=101",
"http://www.bing.com.uy/search?q=&count=50&first=1",
"http://www.bing.com.uy/search?q=&count=50&first=51",
"http://www.bing.com.uy/search?q=&count=50&first=101",
"http://www.bing.vn/search?q=&count=50&first=1",
"http://www.bing.vn/search?q=&count=50&first=51",
"http://www.bing.vn/search?q=&count=50&first=101"
]

def dorkscan(dork):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for bing in binglist:
        bingg = bing.replace("&count", dork + "&count")
        try:
            r = requests.get(bingg, headers=headers, timeout=10)
            checktext = r.text
            checktext = checktext.replace("<strong>", "")
            checktext = checktext.replace("</strong>", "")
            checktext = checktext.replace('<span dir="ltr">', '')
            checksites = re.findall('<cite>(.*?)</cite>', checktext)
            from urllib.parse import urlparse

            for sites in checksites:
                try:
                    # Clean the URL first
                    sites = sites.split(' ')[0]  # Take only the first part if there are spaces
                    sites = sites.split('›')[0].strip()  # Remove everything after › and strip whitespace
                    
                    # Parse the URL properly
                    if not sites.startswith(('http://', 'https://')):
                        sites = 'http://' + sites
                    
                    parsed_url = urlparse(sites)
                    domain = parsed_url.scheme + "://" + parsed_url.netloc
                    
                    if domain and len(domain) > 7:  # Make sure we have more than just http://
                        print(f"{wh}[{g}+{wh}] {domain}")
                        with open("Result/sitelist.txt", "a") as f:
                            f.write(domain + "\n")
                except:
                    continue  # Skip malformed URLs
        except:
            continue  # Skip failed requests

def dk():
    clear()
    print(banner)
    print(f"{wh}[{g}+{wh}] Using Tools Dork Scanner.")
    dorklist = input(f"{wh}[{g}?{wh}] Dorklist : ")
    
    # Create Result directory if it doesn't exist
    if not os.path.exists('Result'):
        os.makedirs('Result')
        
    try:
        # Clear previous results
        if os.path.exists('Result/sitelist.txt'):
            os.remove('Result/sitelist.txt')
        if os.path.exists('Result/sites.txt'):
            os.remove('Result/sites.txt')
            
        dorks = open(dorklist, 'r').read().splitlines()
        print(f"{wh}[{g}!{wh}] Scan started! Please wait...")
        
        # Create thread pool and scan
        pp = Pool(70)
        pr = pp.map(dorkscan, dorks)
        
        print(f"\n{wh}[{g}!{wh}] Cleaning results...")
        clean()
        
    except FileNotFoundError:
        print(f"{wh}[{r}!{wh}] Dorklist not found!")
    except Exception as e:
        print(f"{wh}[{r}!{wh}] An error occurred: {str(e)}")

if __name__ == "__main__":
    dk()
