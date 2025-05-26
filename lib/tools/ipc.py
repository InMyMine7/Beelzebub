import socket
import requests
import re
import sys
import threading
from queue import Queue
from itertools import cycle
from multiprocessing.dummy import Pool as ThreadPool
from lib.tools.utils import banner, clear
from lib.tools.colors import wh, r, g, res, y

def check_ip(ip):
    try:
        ip = ip.replace('\n', '').replace('\r', '').strip()
        if not re.match(r'^\d+\.\d+\.\d+\.\d+$', ip):
            print(r + '[xx] Invalid IP Format >>> ' + ip + wh)
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, 80)) 

        if str(result) != '0':
            print(f'{wh}[{r}!{wh}] Dead IP : {r}' + ip + f"{res}")
            with open('Result/Badip.txt', 'a') as f:
                f.write(ip + '\n')
        else:
            print(f'{wh}[{g}+{wh}] Good IP : {g}' + ip + f'{res}')
            with open('Result/Goodip.txt', 'a') as f:
                f.write(ip + '\n')

    except Exception as e:
        print(f'{wh}[{r}!{wh}] Error Checking IP : {r}' + ip + ':' + str(e) + f'{res}')
    finally:
        sock.close()

def koncet():
    clear()
    print(banner)
    ip_list_file = input(f'{wh}[{g}+{wh}] Enter the list file path: {res}')
    try:
        with open(ip_list_file, 'r') as f:
            ip_list = f.readlines()
    except FileNotFoundError:
        print(f'{wh}[{g}+{wh}] File not found! ')
        return
    except Exception as e:
        print(f'{wh}[{r}!{wh}] Error reading file: ' + str(e) )
        return

    # Input jumlah thread
    threads = input(f'{wh}[{g}+{wh}] Enter number of threads: {wh}')
    try:
        threads = int(threads)
        if threads <= 0:
            raise ValueError(f"{wh}[{r}~{wh}] Threads must be positive!")
    except ValueError:
        print(f'{wh}[{r}!{wh}] Invalid number of threads!')
        return
    
    print(f'{wh}[{g}!{wh}] Starting IP checking with {y}{threads} {res}threads...')
    pool = ThreadPool(threads)
    pool.map(check_ip, ip_list) 
    pool.close()
    pool.join()

    print(f'{wh}[{g}+{wh}] Done!! Check results in {g}Result/Goodip.txt and {r}Result/Badip.txt!!')

if __name__ == '__main__':
    koncet()