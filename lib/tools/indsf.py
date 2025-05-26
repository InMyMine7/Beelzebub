import sys
import asyncio
import requests
import re
from asyncio import Semaphore
from datetime import datetime
from colorama import Fore, init
import time
import httpx

from lib.tools.utils import banner, clear
from lib.tools.colors import wh, r, g, res, y

# Inisialisasi warna
init(autoreset=True)
fr = Fore.RED
fg = Fore.GREEN
fy = Fore.YELLOW
fb = Fore.BLUE
fw = Fore.WHITE
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

# Daftar untuk hasil eksploitasi
SIGNS = ['Uname:', 'Uname :', 'SEA-GHOST MINSHELL', '[ Avaa Bypassed ]', '0byt3m1n1 Shell', 
        '<title>File manager</title>', '<title>000</title>', 'Gel4y Mini Shell', 'PHP File Manager', 
        'Shell Bypass 403 GE-C666C', 'b374k 2.8', 'x3x3x3x_5h3ll', 'Mr.Combet WebShell', 'Negat1ve Shell', 
        '<title>Tiny File Manager</title>', 'Webshell', 'L I E R SHELL', '0byte v2 Shell', '-rw-r--r--', 
        '//0x5a455553.github.io/MARIJUANA/icon.png', 'MSQ_403', 'Public Shell Version 2.0', '<title>Fuxxer</title>', 
        '<span>Upload file:</span', '<title>WIBUHAX0R1337 - ShelL</title>', '<title>Simple Shell</title>', 
        'Cod3d By AnonymousFox', '<a href="?"><img src="https://github.com/fluidicon.png" width="30" height="30" alt=""></a>', 
        '<h1>Ghost Exploiter Team Official</h1>', '<h2>Your IP :', '<input type="submit" name="mkdir" value="Make directory">',
        '<title>请勿使用非法用途</title>', '<div class="corner text-secondary">shell bypass 403</div>', 
        '<input type="submit" value="ok">', 'type="submit" value="upload"', '#block-css#', 'vulncode', 
        '<title>||TINY SHELL ||</title>', '<small>Copyright © 2021 - Haxor Clan</small>', '<title>#shwty</title>', 
        'Upload File : <input type="file" name="file" />', '<h1>Mad Tools Shell</h1>', 'input type="file" id="inputfile" name="inputfile"', 
        '&nbsp;Backdoor Destroyer', 'KCT MINI SHELL 403', '<a href="https://github.com/Den1xxx/Filemanager">', 
        'title>V4Mp</title', 'AlkantarClanX12', 'j3mb03dz m4w0tz sh311', '<title>Mini Shell</title>', '403WebShell', 
        'SeoOk', 'FilesMan', '<h1>{ INDOSEC }</h1>', '<title>Simple File Manage Design by index.php</title>', 
        'MINI MO Shell', '[ HOME ]', '" name="command" placeholder="Command"', 'WSO 4.2.6', 'input type="text" readonly="1" id="upload_visible"', 
        'ALFA TEaM Shell', '<title>Get S.H.E.L.L.en v1.0 | BY ..</title>', 'Hunter Neel', 
        'input type="submit" value="Upload Image" name="submit"','-rwxr-xr-x', 'drwxr-xr-x', 
        '-rw-r--r--', 'BlackDragon', '<h1>[ Shin Bypassed ]</h1>', '<title>Qu?n lý File</title>', 
        '<body>%PDF-0-1<', 'http://www.ubhteam.org/images/UBHFinal1.png', '404-server!!', 'Vuln!! patch it Now!', 
        'B Ge Team File Manager', 'MisterSpyv7up', 'Raiz0WorM', 'input type="file" name="__"><input name="_" type="submit" value="Upload"', 
        'Black Bot', '{Ninja-Shell}', 'Upload File<', 'Yohohohohohooho', 'WSO 4.2.5', 'Madstore.sk!', 'Backdoor Destroyer', 
        './AlfaTeam', 'nopebee7 [@] skullxploit', 'X0MB13', 'https://github.com/fluidicon.png', 'Priv8 Sh3ll!', 'ABC Manager', 
        'TheAlmightyZeus', 'Tryag File Manager', 'WSO 5.1.4', 'aDriv4-Priv8 TOOL', '[ HOME SHELL ]', 'X-Sec Shell V.3', 
        'C0d3d By Dr.D3m0', 'Doc Root:', 'One Hat Cyber Team', 'p0wny@shell:~#', 'WSOX ENC', 
        'Bypass 403 Forbidden / 406 Not Acceptable / Imunify360 / Mini Shell', 'Graybyt3 Was Here', 
        'Powered By Indonesian Darknet', 'PHU Mini Shell', '[ Mini Shell ]', 'TEAM-0ROOT', '#p@@#', 
        '[+] MINI SH3LL BYPASS [+]', 'CHips L Pro sangad', 'ineSec Team Shell', 'ALFA TEaM Shell - v4.1-Tesla', 
        'xichang1', 'Mini Shell By Black_Shadow', 'WHY MINI SHELL', 'Shal Shell Kontol:V', '200400', 'params decrypt fails','TripleDNN',  "form method=\"post\" enctype=\"multipart/form-data\"><input type=\"file\" name=\"__\"><input name=\"_\" type=\"submit\" value=\"Upload\"",
        "input type=\"submit\" value=\"Upload\" name=\"gecko-up-submit\"",
        "onclick=\"cmd.value=",
        "; cmd.focus(); return false;\">Clear cmd<",
        "input type=\"text\" size=\"4\" id=\"fetch_port\" name=\"fetch_port\" value=\"80\"",
        "input type=\"text\" size=\"40\" id=\"fetch_path\" name=\"fetch_path\" value=\"\"",
        "<input type=\"file\" id=\"upload_files\" name=\"upload_files\" multiple=\"multiple\">",
        "input type=\"file\" name=\"fileToUpload\" id=\"fileToUpload\"",
        "input type=text name=path><input type=\"file\" name=\"files\"><input type=submit value=\"Up\"",
        "Upload:</b> <input type=\"file\" id=\"upload\" name=\"upload\"",
        "input type=\"file\" name=\"gecko-file\" id=\"\"><input type=\"submit\" class=\"upload-submit\" name=\"upload-submit\" value=\"Upload\"",
        "Enjoy it </h1><html><head><title>Upload files...<",
        "Local file: <input type =",
        ">Shell Command<",
        "#content_loading#",
        "#block-css#",
        "input type=\"file\" name=\"fileToUpload\" id=\"fileToUpload\"",
        "input type=\"submit\" name=\"submit\" value=\"  >>\"",
        "form method=POST enctype=\"multipart/form-data\" action=\"\"><input type=text name=path><input type=\"file\" name=\"files\"><input type=submit value=\"Up\"",
        "ABC Manager",
        "<title>dfsfkjltyerg</title>",
        "-rw-r--r--",
        "TheAlmightyZeus",
        "LinuXploit",
        "????JFIF??x?x????",
        "©TheAlmightyZeus",
        "Jijle3",
        "WSO 5.1.4",
        "WSO YANZ ENC BYPASS",
        "Yanz Webshell!",
        "FilesMAn",
        "WSO 4.2.5",
        "WSO 2.6",
        "WSO YANZ ENC BYPASS",
        "WSOX ENC",
        "WSO 4.2.6",
        "drwxr-xr-x",
        "WSO 2.5",
        "Uname:",
        "FoxWSO v1.2",
        "WebShellOrb 2.6",
        "File manager -",
        "Cod3d By aDriv4",
        "bondowoso black hat shell",
        "Upload File :",
        "BlackDragon",
        "RxRHaCkEr",
        "| PHP 7.4.20 |",
        "xXx Kelelawar Cyber Team xXx",
        "Code By Kelelawar Cyber Team",
        "Cod3d By AnonymousFox",
        "UnknownSec",
        "shell bypass 403",
        "UnknownSec Shell",
        "drwxrwxr-x",
        "aDriv4",
        "[ HOME SHELL ] ",
        "RC-SHELL v2.0.2011.1009",
        "<title>Mini Shell</title>",
        "Mini Shell",
        "F4st~03 Bypass 403",
        "Negat1ve Shell",
        "Copyright negat1ve1337",
        "value=\"Make directory\"",
        "[+[MAD TIGER]+]",
        "Franz Private Shell",
        "Webshell V1.0",
        ">Cassano Bypass <",
        "TEAM-0ROOT Uploader",
        "Fighter Kamrul Plugin",
        "- FierzaXploit -",
        "Simple,Responsive & Powerfull",
        "<title>FierzaXploit</title>",
        "input type=\"hidden\" name=\"pilihan\" value=\"upload\"",
        "<div id=\"snackbar\"></div>",
        "Current dir:",
        "Minishell",
        "Current directory:",
        "#0x2525",
        "[ ! ] Cilent Shell Backdor [ ! ]",
        "{Ninja-Shell}",
        "type=\"button\">Upload File<",
        "Simple File Manage Design by index.php",
        "Powered By Indonesian Darknet",
        "Mini Shell",
        "root:root",
        "Mini Shell By Black_Shadow",
        "Current dir:",
        "FileManager Version 0.2 by ECWS",
        "xichang1",
        "aDriv4-Priv8 TOOL",
        "B Ge Team File Manager",
        "MARIJuANA",
        "kliverz1337",
        "Indramayu Cyber",
        "ineSec Team Shell",
        "CHips L Pro sangad",
        "Doc Root:",
        "[+] MINI SH3LL BYPASS [+]",
        "TEAM-0ROOT",
        "#No_Identity",
        "Tiny File Manager 2.4.3",
        "[ Mini Shell ]",
        "PHU Mini Shell",
        "//0x5a455553.github.io/MARIJUANA/icon.png",
        "Powered By Indonesian Darknet",
        "Mr.Combet Webshell",
        "MSQ_403",
        "#wp_config_error#",
        "Graybyt3 Was Here",
        "Bypass Sh3ll",
        "Bypass 403 Forbidden / 406 Not Acceptable / Imunify360 / Mini Shell",
        "One Hat Cyber Team",
        "C0d3d By Dr.D3m0",
        "Gel4y Mini Shell",
        "Uname :",
        "SEA-GHOST MINSHELL",
        "[ Avaa Bypassed ]",
        "0byt3m1n1 Shell",
        "FierzaXploit {Mini Shell }",
        "<title>File manager</title>",
        "<title>000</title>",
        "PHP File Manager",
        "Shell Bypass 403 GE-C666C",
        "b374k 2.8",
        "x3x3x3x_5h3ll",
        "<title>Tiny File Manager</title>",
        "L I E R SHELL",
        '<div class="corner text-secondary">shell bypass 403</div>',
        "0byte v2 Shell",
        "Public Shell Version 2.0",
        "<title>Fuxxer</title>",
        "<span>Upload file:</span",
        "<title>WIBUHAX0R1337 - ShelL</title>",
        "SIMPEL BANGET NIH SHELL",
        "ps7n4K3CBK",
        "Function putenv()",
        "Modified By #No_Identity",
        "Lambo [Beta]",
        "./AlfaTeam",
        "| PHP 7.4.27 |",
        "WIBUHAX0R1337",
        "<title>Simple Shell</title>",
        "<a href=\"?\"><img src=\"https://github.com/fluidicon.png\" width=\"30\" height=\"30\" alt=\"\"></a>",
        "<h1>Ghost Exploiter Team Official</h1>",
        "<h2>Your IP :",
        "<input type=\"submit\" name=\"mkdir\" value=\"Make directory\">",
        "<title>请勿使用非法用途</title>",
        "<div class=\"corner text-secondary\">shell bypass 403</div>",
        "<input type=\"submit\" value=\"ok\">",
        "vulncode",
        "<title>||TINY SHELL ||</title>",
        "<small>Copyright © 2021 - Haxor Clan</small>",
        "<title>#shwty</title>",
        "Upload File : <input type=\"file\" name=\"file\" />",
        "<h1>Mad Tools Shell</h1>",
        "input type=\"file\" id=\"inputfile\" name=\"inputfile\"",
        "&nbsp;Backdoor Destroyer",
        "KCT MINI SHELL 403",
        "<a href=\"https://github.com/Den1xxx/Filemanager\">",
        "title>V4Mp</title",
        "AlkantarClanX12",
        "j3mb03dz m4w0tz sh311",
        "title>Smoker Backdoor</title>",
        "403WebShell",
        "<h1>{ INDOSEC }</h1>",
        "<title>Simple File Manage Design by index.php</title>",
        "MINI MO Shell",
        "[ HOME ]",
        "\" name=\"command\" placeholder=\"Command\"",
        "input type=\"text\" readonly=\"1\" id=\"upload_visible\"",
        "ALFA TEaM Shell",
        "<title>Get S.H.E.L.L.en v1.0",
        "Hunter Neel",
        "input type=\"submit\" value=\"Upload Image\" name=\"submit\"",
        "-rwxr-xr-x",
        "<h1>[ Shin Bypassed ]</h1>",
        "<title>Qu?n lý File</title>",
        "http://www.ubhteam.org/images/UBHFinal1.png",
        "404-server!!",
        "Vuln!! patch it Now!",
        "MisterSpyv7up",
        "Raiz0WorM",
        "Black Bot",
        "Madstore.sk!",
        "nopebee7 [@] skullxploit",
        "X0MB13",
        "https://github.com/fluidicon.png",
        "Priv8 Sh3ll!",
        "ABC Manager",
        "TheAlmightyZeus",
        "Tryag File Manager",
        "WSO 5.1.4",
        "aDriv4-Priv8 TOOL",
        "X-Sec Shell V.3",
        "p0wny@shell:~#",
        "WSOX ENC",
        "Graybyt3 Was Here",
        "Powered By Indonesian Darknet",
        "PHU Mini Shell",
        "TEAM-0ROOT",
        "Priv8 WebShell",
        "m1n1 Shell",
        "m1n1 5h3ll",
        "priv8 mini shell",
        "#p@@#",
        "[+] MINI SH3LL BYPASS [+]",
        "ineSec Team Shell",
        "ALFA TEaM Shell - v4.1-Tesla",
        "xichang1",
        "Mini Shell By Black_Shadow",
        "WHY MINI SHELL",
        "Shal Shell Kontol:V",
        "TripleDNN",
        "#0x1877",
        "<title>请勿使用非法用途</title>",
        "<title>#CLS-LEAK#</title>",
        "X4Exploit",
        "kill_the_net",
        "<title>kaylin",
        ">Lock Shell</a></li>",
        "<title>MATTEKUDASAI</title>",
        "PHP-SHELL HUNTER",
        "United Tunsian Scammers",
        "Web Console",
        "United Bangladeshi Hackers",
        "xichang1",
        "<title>IndoXploit</title>",
        "config root man",
        "<title>Legion</title>",
        "Shell Uploader",
        "walex says Fuck Off Kids:",
        "X_Shell",
        "izocin",
        "x7root",
        "X7-ROOT",
        "iCloud1337 private shell",
        "private shell",
        "SuramSh3ll",
        "U7TiM4T3_H4x0R Plugin",
        "Walkers404 Xh3ll B4ckd00r",
        "<title>R@DIK@L</title>",
        "<title>PhpShells.Com</title>",
        "MarukoChan Priv8",
        "King RxR Was",
        "<div><h5>DSH v0.1</h5>",
        "RxR HaCkEr",
        "SOQOR Shell By : HACKERS PAL",
        'input type="file" name="__"><input name="_" type="submit" value="Upload"', 
        '<input type="file" name="apx"',
        '#0x2525',
        'name="uploader" id="uploader"',
        'input type="file" name="file"><input name="_upl" type="submit"',
        '<title>Upload files...</title>',
        '<button>Gaskan</button>',
        '<input type="file" size="20" name="uploads" /> <input type="submit" value="upload" />',
        'input type=text name=path><input type="file" name="files"><input type=submit value="Up"',
        '<input type="file" size="20" name="file_jpg" /> <input type="submit" value="upload" />',
        'type="file"><input type="submit" value="Upload"',
        'Notice: Do not delete or modify the CERT-FILE',
        'aDriv4-Priv8 TOOL',
        'Drive Uploader',
        'DeathShop Uploader',
        'http://www.ubhteam.org/images/UBHFinal1.png',
        'ini PHP Upload By Haxgeno7',
        'input type="submit" value="Upload Image" name="submit"',
        'input type="submit" name="linknya" class="up" value="Upload',
        'input type="file" name="__"><input name="_" type="submit" value="Upload"',
        '<input type=hidden name=p1 value=',
        'Gelişmiş Dosya Yöneticisi',
        'form method=POST enctype="multipart/form-data" action=""><input type=text name=path><input type="file" name="files"><input type=submit value="Up"',
        '<title>./LahBodoAmat Uploader shells</title>',
        'Upload File: <input type="file" name="file"\' type="button">',
        '<button>Gaskan</button>',
        '<title>Upload files...</title>',
        '<input type="file" name="fileToUpload" id="fileToUpload"',
        'name="uploader" id="uploader"><input type="file" name="file"><input name="_upl" type="submit" id="_upl"<Upl file</a></td>'
        '<input name="ext" type="text" value=".php"/>'
        'type="file"/><input type="submit" value="doit"/></form>',  
        "input type=\"file\" name=\"a\"&gt;&lt;input name=\"x\" type=\"submit\" value=\"x\""
        "Nyanpasu!!!",
        "<input type=\"file\" name=\"mbdfiles\"/>",
        "<title>UPLOADER KCT-OFFICIAL</title>",
        "form method=\"post\"",
        "input type=\"submit\" name=\"submit\" value=\"Upload\"",
        "form method=\"post\" enctype=\"multipart/form-data\"><input type=\"file\" name=\"__\"><input name=\"_\" type=\"submit\" value=\"Upload\"",
        "input type=\"file\" name=\"upload\"",
        "input type=\"file\"",
        "input type='submit' name='upload' value='upload",
        "Tryag File Manager",
        "TheAlmightyZeus",
        "input type=\"file\" name=\"file\" size=\"50\"><input name=\"_upl\" type=\"submit\" id=\"_upl\" value=\"Upload\"",
        "input type=\"hidden\" name=\"pilihan\" value=\"upload\"",
        "<div id=\"snackbar\"></div>",
        "<input type=\"file\" name=\"apx\"",
        "#0x2525",
        "name=\"uploader\" id=\"uploader\"",
        "input type=\"file\" name=\"file\"><input name=\"_upl\" type=\"submit\"",
        "<title>Upload files...</title>",
        "<button>Gaskan</button>",
        "<input type=\"file\" size=\"20\" name=\"uploads\" /> <input type=\"submit\" value=\"upload\" />",
        "input type=text name=path><input type=\"file\" name=\"files\"><input type=submit value=\"Up\"",
        "<input type=\"file\" size=\"20\" name=\"file_jpg\" /> <input type=\"submit\" value=\"upload\" />",
        "type=\"file\"><input type=\"submit\" value=\"Upload\"",
        "Notice: Do not delete or modify the CERT-FILE",
        "aDriv4-Priv8 TOOL",
        "aDriv4 Uploader",
        "DeathShop Uploader",
        "http://www.ubhteam.org/images/UBHFinal1.png",
        "ini PHP Upload By Haxgeno7",
        "input type=\"submit\" value=\"Upload Image\" name=\"submit\"",
        "input type=\"submit\" name=\"linknya\" class=\"up\" value=\"Upload",
        "input type=\"file\" name=\"__\"><input name=\"_\" type=\"submit\" value=\"Upload\"",
        "<input type=hidden name=p1 value=",
        "Gelişmiş Dosya Yöneticisi",
        "form method=POST enctype=\"multipart/form-data\" action=\"\"><input type=text name=path><input type=\"file\" name=\"files\"><input type=submit value=\"Up\"",
        "<title>./LahBodoAmat Uploader shells</title>",
        "Upload File: <input type=\"file\" name=\"file\"' type=\"button\">",
        "<button>Gaskan</button>",
        "<title>Upload files...</title>",
        "<input type=\"file\" name=\"fileToUpload\" id=\"fileToUpload\"",
        "name=\"uploader\" id=\"uploader\"><input type=\"file\" name=\"file\"><input name=\"_upl\" type=\"submit\" id=\"_upl\"<Upl file</a></td>",
        "<input name=\"ext\" type=\"text\" value=\".php\"/>",
        "type=\"file\"/><input type=\"submit\" value=\"doit\"/></form>",
        "class=\"Input\" type=\"file\" name=\"file_n[]\"",
        "<input type=\"file\" name=\"upoleuid\"/><input type=\"submit\" value=\"ddok\"/></form>",
        "Ajout nouvelle actualité",
        "<br/>Security Code: <br/><input name=\"security_code\" value=\"\"/>",
        "File mu mas : <input name=\"file\" type=\"file\"",
        "<form id = \"file_uploader\" name = \"file_uploader\" target=\"_blank\"",
        "<input type=\"text\" name=\"target\" size=\"100\" value=\"Location where file will be uploaded (include file name!)\"",
        "<input type=\"file\" name=\"uploaded_file\"></input>",
        "<input id=\"submit\" type=\"submit\" name=\"submit\" value=\"Upload me!\">",
        "<form enctype=\"multipart/form-data\" method=\"post\">",
        "Choose a file to upload: <input name=\"uploadedfile\" type=\"file\" />",
        "<form enctype=\"multipart/form-data\" method=\"POST\">",
        "<input name=\"uploadedfile\" type=\"file\"/>",
        "<input type=\"submit\" value=\"-----\">",
        "<title>RansomWeb BlackCoders XploiterCrew</title>",
        "Priv8 Uploader",
        "Priv8 Home Root Uploader",
        "Pr1v8 Upl0ader",
        "Upl04d3r",
        "Upl0od Your T0ols",
        "Upload File : <input type=\"file\" name=\"file\" />", 'type="password" name="pwdyt"',
        '%PDF-0-1<form action',
        'form method=post>Password: <input type=password name=pass><input type=submit value=',
        '<input type="password" name="pwd" title="Password" autofocus>',
        '"<pre align=center><form method=post>Password<br>',
        '<html><head><title>Login</title></head><body><form action="" method="POST">',
        "type=\"password\" name=\"pwdyt\"",
        "%PDF-0-1<form action",
        "name='watching",
        "<input type=password name=pass",
        "form method=post>Password: <input type=password name=pass><input type=submit value=",
        "<input type=\"password\" name=\"pwd\" title=\"Password\" autofocus>",
        "\"<pre align=center><form method=post>Password<br>",
        "<html><head><title>Login</title></head><body><form action=\"\" method=\"POST\">",
        "<title>DRUNK SHELL BETA </title>",
        "<input type=password name='xxx'>",
        "b374k&nbsp;<span class=",
        "<pre align=center><form method=post>Password<br><input type=password name=pass",
        "pre align=center><form method=post>Password: <input type=password name=pass><input type=submit value=",
        "input type=\"submit\" name=\"submit\" value=\"  >>\"",'Leaf PHPMailer</title>',
        '<title>xLeet PHPMailer</title>',
        '<title>alexusMailer 2.0</title>']

VALID_EXTENSIONS = ['.php', '.phtml', '.php3', '.php4', '.phar', '.shtml', '.cgi', '.py', '.sh', '.alfa', '.pl']
INVALID_EXTENSIONS = ['.txt', '.js', '.css', '.jpg', '.jpeg', '.png', '.gif', '.ico']

class ShellScanner:
    def __init__(self, concurrency=20):
        self.start_time = time.time()
        self.scanned_count = 0
        self.found_count = 0
        self.error_count = 0
        self.semaphore = Semaphore(concurrency)

    async def get_domain(self, site):
        try:
            site = site.strip().lower().replace('http://', '').replace('https://', '')
            return site.split('/')[0].split(':')[0]
        except Exception as e:
            print(f"{fr}[!] Error processing domain {site}: {e}")
            return None

    async def send_request(self, url, path):
        full_url = f"{url.rstrip('/')}/{path.lstrip('/')}"
        if len(full_url) > 300:
            return None
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=15, verify=False, headers=headers) as client:
                response = await client.get(full_url)
                return response
        except httpx.RequestError:
            return None

    async def check_backdoors(self, response):
        if response and response.status_code == 200:
            content = response.text.lower()
            for sign in SIGNS:
                if sign.lower() in content:
                    return sign
        return None

    async def write_result(self, filename, url):
        try:
            with open(filename, 'a') as f:
                f.write(f"{url}\n")
        except Exception as e:
            print(f"{fr}[!] Error writing to {filename}: {e}")

    async def check_file(self, base_url, file_path):
        try:
            full_url = f"{base_url.rstrip('/')}/{file_path.lstrip('/')}"
            response = await self.send_request(base_url, file_path)
            backdoor = await self.check_backdoors(response)
            if backdoor:
                self.found_count += 1
                print(f"{fg}[+] Found {backdoor} in {full_url}")
                await self.write_result("Result/found_shells.txt", full_url)
                return True  # Shell ditemukan
            else:
                print(f"{fr}[-] Not vulnerable: {full_url}")
            self.scanned_count += 1
        except Exception as e:
            self.error_count += 1
            print(f"{fr}[!] Error checking {file_path}: {e}")
        return False

    async def traverse_directory(self, base_url, current_path, visited_paths=None):
        if visited_paths is None:
            visited_paths = set()

        if current_path in visited_paths:
            return False

        visited_paths.add(current_path)
        response = await self.send_request(base_url, current_path)
        if response and response.status_code == 200:
            if 'Index of' in response.text:
                print(f"{fw}[i] Index page: {base_url}/{current_path}")
                links = re.findall(r'<a\s+href="([^"]+)"', response.text)
                for link in links:
                    if link in ('../', '/', '') or link.startswith('?'):
                        continue

                    next_path = f"{current_path.rstrip('/')}/{link.lstrip('/')}"
                    if self.is_valid_file(link):
                        found = await self.check_file(base_url, next_path)
                        if found:
                            return True
                    elif not any(ext in link for ext in INVALID_EXTENSIONS) and '.' not in link:
                        found = await self.traverse_directory(base_url, next_path, visited_paths)
                        if found:
                            return True
            else:
                print(f"{fw}[i] Non-index page: {base_url}/{current_path}")
        else:
            print(f"{fr}[!] Error accessing {base_url}/{current_path}")
        return False

    def is_valid_file(self, filename):
        return any(filename.endswith(ext) for ext in VALID_EXTENSIONS) and not any(filename.endswith(ext) for ext in INVALID_EXTENSIONS)

    async def scan_site(self, site):
        base_url = await self.get_domain(site)
        if not base_url:
            return
        full_url = f"http://{base_url}"
        print(f"{fb}[*] Scanning: {full_url}")

        with open('lib/files/Path.txt', 'r') as f:
            paths = [line.strip() for line in f if line.strip()]
        for path in paths:
            found = await self.traverse_directory(full_url, path)
            if found:
                break  # Hentikan jika shell ditemukan

    def print_stats(self):
        duration = time.time() - self.start_time
        print(f"\n{fg}=== Scan Complete ===")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Files Scanned: {self.scanned_count}")
        print(f"Shells Found: {self.found_count}")
        print(f"Errors: {self.error_count}")


async def kontolbgt():
    try:
        clear()
        print(banner)
        print(f"{wh}[{g}+{wh}] Using tools IndexOf Shell Finder\n")
        site_file = input(f"{wh}[{g}+{wh}] WEBSITE LIST : ").strip()
        thread_input = input(f"{wh}[{g}+{wh}] THREAD (concurrency) : ").strip()

        try:
            concurrency = int(thread_input)
            if concurrency < 1:
                raise ValueError
        except ValueError:
            print(f"{fr}{wh}[{r}!{wh}] Invalid thread count. Must be a positive integer.")
            return

        with open(site_file, 'r') as f:
            sites = [line.strip() for line in f if line.strip()]

        if not sites:
            print(f"{fr}{wh}[{r}!{wh}][!] No valid targets found in {site_file}")
            return

        scanner = ShellScanner(concurrency)
        print(f"{wh}[{g}+{wh}] Starting scan with {len(sites)} targets using {concurrency} threads\n")

        sem = Semaphore(concurrency)

        async def limited_scan(site):
            async with sem:
                await scanner.scan_site(site)

        tasks = [limited_scan(site) for site in sites]
        await asyncio.gather(*tasks)

        scanner.print_stats()

    except Exception as e:
        print(f"{fr}{wh}[{r}!{wh}][!] Fatal error: {e}")


if __name__ == "__main__":
    asyncio.run(kontolbgt())
