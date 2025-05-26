import requests  
import os 
import json
import re
import time
import platform
from colorama import Fore, init  
from lib.tools.utils import r, g, wh, res, bg_red, banner, clear

# Inisialisasi colorama biar output di terminal ada warnanya kaya idup gweh
init(autoreset=True)
def global_pilih():
    print(f"""
{g}[{wh}1{g}]{wh} Zone-H Grabber        
{g}[{wh}2{g}]{wh} ZoneXsec Grabber{res}     
{g}[{wh}3{g}]{wh} HaxorID Grabber{res}           
          """)


class ZoneH_Grabber:
    def __init__(self, config_path="lib/files/config.json"):
        clear()
        print(banner)
        self.PHPSESSID = ""
        self.ZHE = ""
        self.ResultFileName = ""
        self.Python_Version = platform.python_version()

        # Load session values from JSON config if available
        self.load_config(config_path)

    def load_config(self, config_path):
        if os.path.isfile(config_path):
            with open(config_path, 'r') as file:
                config = json.load(file)
                zone_h_config = config.get("zone-h_config", {})
                self.PHPSESSID = zone_h_config.get("phpsessid", "")
                self.ZHE = zone_h_config.get("zhe", "")

    def save_config(self):
        config = {
            "zone-h_config": {
                "phpsessid": self.PHPSESSID,
                "zhe": self.ZHE
            }
        }
        with open("lib/files/config.json", "w") as file:
            json.dump(config, file, indent=4)

    def save(self, name, isi, a='a'):
        try:
            with open(name, a) as op:
                op.write(isi)
        except Exception as e:
            print(f"{wh}[{r}!{wh}] Error saving to file: {res}{e}")

    def input_phpsessid(self):
        self.PHPSESSID = self.input(f'{wh}[{g}+{wh}] Re-enter PHPSESSID = {res}')
        if self.PHPSESSID:
            self.save_config()  # Save new value to JSON

    def input_zhe(self):
        self.ZHE = self.input(f'{wh}[{g}+{wh}] Re-enter ZHE= ')
        if self.ZHE:
            self.save_config()  # Save new value to JSON


    def get_urls(self, source):
        # Regex to capture text within <td> tags
        r = re.findall(r'<td>(.*?)<\/td>', source, re.DOTALL)
        urls = []
        
        for item in r:
            cleaned_item = item.strip()  # Remove surrounding whitespace
            # Use regex to capture the full URL (without file paths)
            match = re.match(r'([a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,}))', cleaned_item)
            if match:
                base_url = match.group(1)  # Get the base URL
                urls.append(base_url)

        return urls


    def Grab(self):
        if not self.ResultFileName:
            self.ResultFileName = self.input(f'{wh}[{g}+{wh}] Input Result File Name: [Ex: Result.txt]=> ') or 'mirror_grab.txt'
            self.ResultFileName = f"Result/{self.ResultFileName}" 
            print(f'{wh}[{g}+{wh}] Results will be stored in: {self.ResultFileName}\n\n>_Start.')

        i = 1
        while i <= 50:
            try:
                self.Url = f"{self.SetUrl}page={i}"
                cookies = {'PHPSESSID': self.PHPSESSID, 'ZHE': self.ZHE}
                req = requests.get(self.Url, cookies=cookies)

                print(f"Status Code: {req.status_code}")  # Show status code

                if '<input type="text" name="captcha"' in req.text:
                    print(f'{wh}[{r}!{wh}] CAPTCHA detected. Please re-enter PHPSESSID.')
                    self.input_phpsessid()  # Re-enter PHPSESSID

                elif '<html><body>-<script type="text/javascript"' in req.text:
                    print(f'{wh}[{r}!{wh}] An error occurred with PHPSESSID or ZHE. Please re-enter both.')
                    self.input_phpsessid()  # Re-enter PHPSESSID
                    self.input_zhe()  # Re-enter ZHE

                else:
                    # Process and save URLs if no error
                    urls = self.get_urls(req.text)
                    i += 1

                    if urls:
                        print(f'\nURL: {self.Url}')
                        for url in urls:
                            print(f"{wh}[{g}+{wh}] Grabbed {url}")  # Print the found URL
                            self.save(self.ResultFileName, f'{url}\n')  # Save the full URL
                    else:
                        print(f"{wh}[{g}+{wh}] Done Grabbing")
                        break

                time.sleep(1)  # Pause to avoid getting blocked

            except KeyboardInterrupt:
                print(f'{wh}[{r}!{wh}] Operasi dihentikan oleh pengguna (Ctrl + C)')
                exit()
            except Exception as e:
                print(f"{wh}[{r}!{wh}] Error: {e}")  # Handle errors

    def input(self, q):
        if int(self.Python_Version[0]) == 3:
            return input(str(q))
        elif int(self.Python_Version[0]) == 2:
            return input(str(q))

    def menu(self):
        print(f'''
{wh}[{g}1{wh}] Mass Grab notifier 
{wh}[{g}2{wh}] Single grab notifier
{wh}[{g}3{wh}] Grab from Special Archive
{wh}[{g}4{wh}] Grab from Archive
{wh}[{g}5{wh}] Grab from Onhold
        ''')
        try:
            menu = int(input(f"{wh}[{g}SELECT{wh}] : {res}")) 
            if menu == 1:
                list = self.input(f'{wh}[{g}+{wh}] List Nick : {res}')
                if list and os.path.isfile(list):
                    bukabaju = open(list, 'r').read().strip().split('\n')
                    for u in bukabaju:
                        if u:
                            self.SetUrl = 'http://zone-h.org/archive/notifier=' + u + '?'
                            self.Grab()
                else:
                    print(f'{wh}[{r}!{wh}] Ur list not found {bg_red}{list}{res}')
            elif menu == 2:
                self.notifier = self.input(f'{wh}[{g}+{wh}] Notifier{wh} : {res}')
                if self.notifier:
                    self.SetUrl = 'http://zone-h.org/archive/notifier=' + self.notifier + '?'
                    self.Grab()
            elif menu == 3:
                self.SetUrl = 'http://zone-h.org/archive/special=1/'
                self.Grab()
            elif menu == 4:
                self.SetUrl = 'http://zone-h.org/archive/'
                self.Grab()
            elif menu == 5:
                self.SetUrl = 'https://www.zone-h.org/archive/published=0/'
                self.Grab()
            else:
                print(f'{wh}[{r}!{wh}]Error -> Exit.')
        except ValueError:
            print(f'{wh}[{r}!{wh}] ValueError ~> Error ~> Exit.')
        except:
            pass
        
class ZoneXSecGrabber:
    def __init__(self):
        clear()
        print(banner)
        self.ResultFileName = ""

    def save(self, name, content, mode='a'):
        folder = "Result"  # Nama folder untuk menyimpan hasil
        if not os.path.exists(folder):
            os.makedirs(folder)  # Buat folder jika belum ada

        file_path = os.path.join(folder, name)  # Gabungkan folder dengan nama file

        try:
            with open(file_path, mode) as file:
                file.write(content)
        except Exception as e:
            print(f"{wh}[{r}!{wh}] Error saving to file: {res}{e}")


    def get_urls(self, source):
        # Regex untuk menangkap domain
        r = re.findall(r'<td>(.*?)<\/td>', source)
        urls = []
        
        for item in r:
            cleaned_item = item.strip()  # Menghapus spasi di sekitar
            # Gunakan regex untuk menangkap domain
            match = re.match(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', cleaned_item)
            if match:
                base_url = match.group(1)  # Ambil nama domain
                urls.append(base_url)

        return list(set(urls))  

    def grab(self):
        if not self.ResultFileName:
            self.ResultFileName = input(f'{wh}[{g}+{wh}] Enter Result File Name (e.g., Result.txt): {res}') or 'mirror_grab.txt'
            self.ResultFileName = f"{self.ResultFileName}"  # Tambahkan folder           
            print(f'{wh}[{g}+{wh}] Results will be stored in: Result/{self.ResultFileName}\n\nStarting...')

        i = 1
        while i <= 50:
            try:
                self.Url = f"{self.SetUrl}page={i}"
                response = requests.get(self.Url)

                urls = self.get_urls(response.text)
                i += 1

                if urls:
                    print(f'\nURL: {self.Url}')
                    for url in urls:
                        print(f"{wh}[{g}+{wh}] Grabbed {url}")
                        self.save(self.ResultFileName, f'{url}\n')
                else:
                    print(f"{wh}[{g}+{wh}] No more URLs found. Stopping.")
                    break

                time.sleep(1)
            except KeyboardInterrupt:
                print(f'{wh}[{r}!{wh}] Operation interrupted by user (Ctrl + C)')
                break
            except Exception as e:
                print(f"{wh}[{r}!{wh}] Error: {e}")

    def menu(self):
        print(f'''
{g}[{wh}1{g}]{wh} Grab from Special Archive
{g}[{wh}2{g}]{wh} Grab from Archive
{g}[{wh}3{g}]{wh} Grab from Onhold
{g}[{wh}4{g}]{wh} Grab From Attacker {res}
        ''')
        try:
            choice = int(input(f"{wh}[{g}Select an Option{wh}]: {res}"))
            if choice == 1:
                self.SetUrl = 'https://zone-xsec.com/special/'
                self.grab()
            elif choice == 2:
                self.SetUrl = 'https://zone-xsec.com/archive/'
                self.grab()
            elif choice == 3:
                self.SetUrl = 'https://zone-xsec.com/onhold/'
                self.grab()
            elif choice == 4:
                self.notifier = input(f'{wh}[{g}+{wh}] Notifier: {res}')  # Corrected the input method
                if self.notifier:
                    self.SetUrl = f'https://zone-xsec.com/archive/attacker/{self.notifier}/'
                    self.grab()
            else:
                print(f"{wh}[{r}!{wh}] Invalid Option. Exiting.")
        except ValueError:
            print(f"{wh}[{r}!{wh}] ValueError - Exiting.")
        except Exception as e:
            print(f"{wh}[{r}!{wh}] Error: {e}")


class HaxoridGrabber:
    def __init__(self):
        clear()
        print(banner)
        self.ResultFileName = ""

    def save(self, name, content, mode='a'):
        """Saves the content to a specified file."""
        try:
            with open(name, mode) as file:
                file.write(content)
        except Exception as e:
            print(f"{wh}[{r}!{wh}] Error saving to file: {res}{e}")

    def get_urls(self, source):
        # Regex untuk menangkap nilai dari atribut alt dengan target='_blank'
        r = re.findall(r"alt='([^']+)'", source)
        urls = []

        for item in r:
            cleaned_item = item.strip()  # Menghapus spasi di sekitar
            # Gunakan regex untuk menangkap domain
            match = re.match(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', cleaned_item)
            if match:
                base_url = match.group(1)  # Ambil nama domain
                urls.append(base_url)

        return list(set(urls))  


    def grab(self):
        if not self.ResultFileName:
            self.ResultFileName = input(f'{wh}[{g}+{wh}] Enter Result File Name (e.g., Result.txt): {res}') or 'mirror_grab.txt'
            self.ResultFileName = f"{self.ResultFileName}"  # Tambahkan folder
            print(f'{wh}[{g}+{wh}] Results will be stored in: Result/{self.ResultFileName}\n\nStarting...')

        page = 1
        while True:  # Loop indefinitely until a stop condition is met
            try:
                self.Url = f"{self.SetUrl}?page={page}"
                response = requests.get(self.Url)

                if response.status_code != 200:
                    print(f"{wh}[{r}!{wh}] Failed to retrieve data from {self.Url}. Status Code: {response.status_code}")
                    break  # Exit if there's an error fetching the page

                urls = self.get_urls(response.text)

                if urls:
                    print(f'\nURL: {self.Url}')
                    for url in urls:
                        print(f"{wh}[{g}+{wh}] Grabbed {url}")
                        self.save(self.ResultFileName, f'{url}\n')
                    page += 1  # Increment page number for the next request
                else:
                    print(f"{wh}[{g}+{wh}] No more URLs found on page {page}. Stopping.")
                    break  # Stop if no valid URLs were found

                time.sleep(1)  # Pause to avoid overwhelming the server
            except KeyboardInterrupt:
                print(f'{wh}[{r}!{wh}] Operation interrupted by user (Ctrl + C)')
                break
            except Exception as e:
                print(f"{wh}[{r}!{wh}] Error: {e}")

    def menu(self):
        """Displays the menu and handles user input for scraping options."""
        print(f'''
{wh}[{g}1{wh}] Grab from Haxorid Archive
{wh}[{g}2{wh}] Grab from Haxorid Onhold
{wh}[{g}3{wh}] Grab from Haxorid Special
{wh}[{g}4{wh}] Grab Domain From Attacker
        ''')
        try:
            choice = int(input(f"{wh}[{g}Select an Option{wh}]: {res}"))
            if choice == 1:
                self.SetUrl = 'https://hax.or.id/archive'
                self.grab()
            elif choice == 2:
                self.SetUrl = 'https://hax.or.id/archive/onhold'
                self.grab()
            elif choice == 3:
                self.SetUrl = 'https://hax.or.id/archive/special'
                self.grab()
            elif choice == 4:
                self.notifier = input(f'{wh}[{g}+{wh}] Notifier: {res}')  # Corrected the input method
                if self.notifier:
                    self.SetUrl = f'https://hax.or.id/archive/attacker/{self.notifier}&'
                    self.grab()
            else:
                print(f"{wh}[{r}!{wh}] Invalid Option. Exiting.")
        except ValueError:
            print(f"{wh}[{r}!{wh}] ValueError - Exiting.")
        except Exception as e:
            print(f"{wh}[{r}!{wh}] Error: {e}")

# -- Main
def komeng():
    clear()
    print(banner)
    global_pilih()
    choice = input(f"{g}[{wh}SELECT{g}] {wh}: {res}") 
    if choice == '1':
        zoneh_grab = ZoneH_Grabber()  
        zoneh_grab.menu()  
    elif choice == '2':
        xsec_grabber = ZoneXSecGrabber()
        xsec_grabber.menu()
    elif choice == '3':
        haxorid_grabber = HaxoridGrabber()
        haxorid_grabber.menu()
    else:
        print("Invalid choice, please select again.")

if __name__ == "__main__":
    komeng()
