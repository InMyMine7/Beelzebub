import requests, re, os, sys, codecs, random               
from multiprocessing.dummy import Pool                          
from time import time as timer  
import time
from random import sample
from colorama import Fore                               
from colorama import Style                              
from pprint import pprint                               
from colorama import init
from googlesearch import search
from lib.tools.utils import banner, list_grabber, clear

init(autoreset=True)
year = time.strftime("%y")
month = time.strftime("%m")

def site1():
    try:
        dom = input('\033[97m[\033[92m~\033[97m] Enter Domain Name (com,org,net) : ')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        for page in range(1, 100):
            url = "https://azstats.org/top/domain-zone/" + dom + "/" + str(page)
            req = requests.get(url, headers=headers, timeout=15).content.decode('utf-8')  
            if "Domain" in req:
                cek = re.findall(r'style="margin-left: 0;">(.*?)</a>', req)
                for xx in cek:
                    print('[\033[92m+\033[97m] https://' + xx)
                    with open('Result/domain.txt', 'a') as f:
                        f.write('https://' + xx + '\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')
                
    except Exception as e:
        print(f"Error: {e}")

def site2():
    try:
        dom = input('\033[97m[\033[92m~\033[97m] Enter Domain Name (com,org,net) : ')
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ')
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        for page in range(int(awalbertemu), int(terakhirbertemu)):
            url = "https://bestwebsiterank.com/domains/." + dom + "/" + str(page)
            req = requests.get(url, headers=headers, timeout=15).content.decode('utf-8')  # Python 3 change
            if "Domain" in req:
                cinta = re.findall(r'<a href="https://bestwebsiterank.com/(.*?)/"><img src="', req)
                for xx in cinta:
                    kamu = xx.replace("https://bestwebsiterank.com/", "")
                    print('[\033[92m+\033[97m] https://' + kamu)
                    with open('Result/domain.txt', 'a') as f:
                        f.write('https://' + kamu + '\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')
                
    except Exception as e:
        print(f"Error: {e}")

def site3():
    try:
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ')
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ')
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        for page in range(int(awalbertemu), int(terakhirbertemu)):
            url = "https://www.topmillion.net/pages/websites/page/"+str(page)+"/"
            req = requests.get(url, headers=headers, timeout=15).text
            if "All websites" in req:
                cinta = re.findall(r'https://(.*?)?w=400" alt="Thumbnail" />', req)
                for xx in cinta:
                    kamu = xx.replace('?', '')
                    print('[\033[92m+\033[97m] https://'+kamu)
                    with open('Result/domain.txt','a') as f:
                        f.write('https://'+kamu+'\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")

def site4():
    try:
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ')
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ')
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        for page in range(int(awalbertemu), int(terakhirbertemu)):
            url = "https://www.dubdomain.com/index.php?page="+str(page)+"/"
            req = requests.get(url, headers=headers, timeout=15).text
            if "Recently Analyzed" in req:
                cinta = re.findall(r'data-src="(.*?)"', req)
                for xx in cinta:
                    kamu = xx.replace('https://www.google.com/s2/favicons?domain_url=', '')
                    print('[\033[92m+\033[97m] https://'+kamu)
                    with open('Result/domain.txt','a') as f:
                        f.write('https://'+kamu+'\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")

def site5():
    try:
        dom = input('\033[97m[\033[92m~\033[97m] Enter Domain Name (com,org,net) : ')
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ')
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ')
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        for page in range(int(awalbertemu), int(terakhirbertemu)):
            url = "http://pluginu.com/domain-zone/"+dom+"/"+str(page)
            req = requests.get(url, headers=headers, timeout=15).text
            if "Websites in domain zone" in req:
                cinta = re.findall(r'<button class="btn btn-default pull-left" type="button">\n  (.*?)</button></a>', req)
                for xx in cinta:
                    kamu = xx.replace("http://pluginu.com/", "")
                    print('[\033[92m+\033[97m] ttps://'+kamu)
                    with open('Result/domain.txt','a') as f:
                        f.write('https://'+kamu+'\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")

def site6():
    try:
        dom = input('\033[97m[\033[92m~\033[97m] Enter Theme Name (divi, avada, etc) : ')
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ')
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ')
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        for page in range(int(awalbertemu), int(terakhirbertemu)):
            url = "https://themetix.com/"+dom+"/"+str(page)
            req = requests.get(url, headers=headers, timeout=15).text
            if "Themes List" in req:
                cinta = re.findall(r' <img class="d-block w-100" src="/images/wpts-sss/(.*?).jpg" alt="', req)
                for xx in cinta:
                    kamu = xx.replace("https://themetix.com/", "")
                    print('[\033[92m+\033[97m] https://'+kamu)
                    with open('Result/domain.txt','a') as f:
                        f.write('https://'+kamu+'\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")

def site7():
    try:
        date = input('\033[97m[\033[92m~\033[97m] Enter yyyy/mm/dd (2023-11-09) : ' )
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36'}
        req = requests.get("https://www.uidomains.com/browse-daily-domains-difference/0/"+date, headers=headers, timeout=15).text
        if 'Domains' in req:
            cinta = re.findall(r'<li>(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z]{1,63}</li>', req)
            for xx in cinta:
                kamu = xx.replace('<li>', '').replace('</li>', '')
                print('[\033[92m+\033[97m]  https://'+kamu)
                with open('Result/domain.txt','a') as f:
                    f.write('https://'+kamu+'\n')
        else:
            print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")

def site8():
    try:
        dom = input('\033[97m[\033[92m~\033[97m] Enter yyyy/mm/dd (2023-06-19) :')
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ')
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ')
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        for page in range(int(awalbertemu), int(terakhirbertemu)):
            url = "https://websitebiography.com/new_domain_registrations/"+dom+"/"+str(page)+"/"
            req = requests.get(url, headers=headers, timeout=15).text
            if "New Domain Registrations" in req:
                cinta = re.findall(r"<a href='https://(.*?).websitebiography.com' title='More", req)
                for xx in cinta:
                    kamu = xx.replace("https://themetix.com/", "")
                    print('[\033[92m+\033[97m] https://'+kamu)
                    with open('Result/domain.txt','a') as f:
                        f.write('https://'+kamu+'\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")
        
def site9():
    try:
        date = input('\033[97m[\033[92m~\033[97m] Enter Kyword (edu, gov, love, you): ' )
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36'}
        req = requests.get("https://website.informer.com/search.php?query="+date, headers=headers, timeout=15).text
        if 'Websites' in req:
            cinta = re.findall(r'data-domain="(.*)"', req)
            for xx in cinta:
                kamu = xx.replace('<li>', '').replace('</li>', '')
                print('[\033[92m+\033[97m]  https://'+kamu)
                with open('Result/domain.txt','a') as f:
                    f.write('https://'+kamu+'\n')
        else:
            print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")

def site10():
    try:
        dom = input('\033[97m[\033[92m~\033[97m] Enter Domain Name (com,org,net) : ')
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ')
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ')
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        for page in range(int(awalbertemu), int(terakhirbertemu)):
            url = "https://www.greensiteinfo.com/domains/"+dom+"/"+str(page)+"/"
            req = requests.get(url, headers=headers, timeout=15).text
            if "Domains" in req:
                cinta = re.findall(r'https://www.greensiteinfo.com/search/(.*?)/ >', req)
                for xx in cinta:
                    kamu = xx.replace("https://www.greensiteinfo.com/search/", "")
                    print('[\033[92m+\033[97m] ttps://'+kamu)
                    with open('Result/domain.txt','a') as f:
                        f.write('https://'+kamu+'\n')
            else:
                print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks For using our tools :)')

    except Exception as e:
        print(f"Error: {e}")
        

def dork_search(dork_query, num_results=10, delay=2):
    print(f"Searching with dork: {dork_query}\n")
    file_path = "Result/dork_search.txt"

    try:
        with open(file_path, "a", buffering=1) as file:  
            for url in search(dork_query, num_results=num_results, sleep_interval=delay):
                print('[\033[92m+\033[97m] ' + url)
                file.write(url + "\n")
                file.flush()  

    except Exception as e:
        print(f"There is an error: {e}")

def dork_main():
    dork = input("Enter Google Dork: ")
    jumlah = int(input("The number of results you want to retrieve: "))
    jeda = int(input("Delay between searches (seconds): "))

    dork_search(dork, num_results=jumlah, delay=jeda)

    print("\nResults are being saved in Result/dork_search.txt")



def site12():
    try:
        dom = input('\033[97m[\033[92m~\033[97m] Enter Domain Name (com,org,net) : ').strip()
        awalbertemu = input('\033[97m[\033[92m~\033[97m] First page : ').strip()
        terakhirbertemu = input('\033[97m[\033[92m~\033[97m] Last Page : ').strip()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        result_file = 'Result/domain.txt'

        for page in range(int(awalbertemu), int(terakhirbertemu) + 1):
            url = f"https://onshopify.com/domain-zone/{dom}/{page}"
            print(f'\033[97m[\033[92m~\033[97m] Fetching: {url}')

            try:
                req = requests.get(url, headers=headers, timeout=15)
                req.raise_for_status()
                html = req.text

                if "Websites in domain" in html:
                    matches = re.findall(r'<button class="btn btn-default pull-left" type="button">\s*(.*?)\s*</button>', html)
                    
                    if matches:
                        with open(result_file, 'a') as f:
                            for domain in matches:
                                domain = domain.strip()
                                full_url = f"https://{domain}"
                                print(f'[\033[92m+\033[97m] {full_url}')
                                f.write(full_url + '\n')
                    else:
                        print('\033[97m[\033[91m-\033[97m] No valid domains found on this page.')

                else:
                    print('\033[97m[\033[92m~\033[97m] Done Grabbing, Thanks for using our tools :)')
                    break

            except requests.exceptions.RequestException as err:
                print(f'\033[91m[ERROR]\033[97m Failed to fetch {url} - {err}')

    except Exception as e:
        print(f'\033[91m[ERROR]\033[97m {e}')

def digidaw():
    clear()
    print(banner)
    print(list_grabber)
    menu = input('\033[97m[\033[92m~\033[97m] : ')
    try:
        if menu == '1':
            site1()
        if menu == '2':
            site2()
        if menu == '3':
            site3()
        if menu == '4':
            site4()
        if menu == '5':
            site5() 
        if menu == '6':
            site6() 
        if menu == '7':
            site7()
        if menu == '8':
            site8()
        if menu == '9':
            site9()
        if menu == '10':
            site10()
        if menu == '11':
            dork_main()
        if menu == '12':
            site12()
    except:
        pass
    
if __name__ == '__main__':
    digidaw()
