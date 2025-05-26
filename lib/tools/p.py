import sys
import os
import socket
import time
import random
from colorama import *
from colorama import Fore, Back, init
from lib.tools.utils import clear, banner
from lib.tools.utils import r, g, wh
def getIP(site):
    site = site.strip()
    try:
        if 'http://' not in site and 'https://' not in site:
            IP1 = socket.gethostbyname(site)
            print(f"{wh}[{g}+{wh}] IP: " + IP1)
            with open('Result/ips.txt', 'a') as f:
                f.write(IP1 + '\n')
        elif 'http://' in site or 'https://' in site:
            url = site.replace('http://', '').replace('https://', '').replace('/', '')
            IP2 = socket.gethostbyname(url)
            print(f"{wh}[{g}+{wh}] IP: " + IP2)
            with open('Result/ips.txt', 'a') as f:
                f.write(IP2 + '\n')
    except:
        pass

def notnot():
    clear()
    print(banner)
    nam = input(f'{wh}[{g}+{wh}] Domain List name : ')
    with open(nam, 'r') as f:
        for i in f:
            getIP(i)

if __name__ == "__main__":
    notnot()