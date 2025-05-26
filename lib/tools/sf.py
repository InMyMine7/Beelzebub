import asyncio
import httpx
import sys
import os
from colorama import Fore, init
from lib.tools.utils import r, g, wh, res, bg_red, c, banner, clear
init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_shell_signatures():
    return [
        
        'Uname:', 'Uname :', 'SEA-GHOST MINSHELL', '[ Avaa Bypassed ]', '0byt3m1n1 Shell', 
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
  "input type=\"submit\" value=\"Upload\" name=\"gecko-up-submit\"","<title>GOOGLE</title>", "#!*&@#!*&@#", 'Function putenv()', '<h1>芝麻web文件管理V1.00</h1>', 'Chitoge kirisaki <3', 'Faizzz-Chin ShellXploit', 'Ghazascanner File Manager',
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
  'input type="file" name="__"><input name="_" type="submit" value="Upload"'
    ]

def load_uploader_signatures():
    return [
        
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
        'aDriv4 Uploader',
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
        'type="file"/><input type="submit" value="doit"/></form>'
    ]

def load_pass_shell_signatures():
    return [
        
        'type="password" name="pwdyt"',
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
        "input type=\"submit\" name=\"submit\" value=\"  >>\""  
    ]

def load_mailer_signatures():
    return [
        'Leaf PHPMailer</title>',
        '<title>xLeet PHPMailer</title>',
        '<title>alexusMailer 2.0</title>'
    ]

async def finder(url, client):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        
        try:
            listaa = open('lib/files/shell-path.txt', 'r', encoding='utf-8', errors='ignore').read().splitlines()
        except FileNotFoundError:
            print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] SHELL LIST NOT FOUND")
            return

        shell_signatures = load_shell_signatures()
        uploader_signatures = load_uploader_signatures()
        pass_shell = load_pass_shell_signatures()
        mailer_signatures = load_mailer_signatures()

        for script in listaa:
            full_url = url.rstrip('/') + '/' + script.lstrip('/')
            try:
                resp = await client.get(full_url)
                content = resp.text

                if any(sig in content for sig in shell_signatures):
                    print(f"{wh}[{g}+{wh}] [GOTCHAAAA!!!] {full_url}")
                    os.makedirs('Result', exist_ok=True)
                    with open('Result/shell.txt', 'a') as f:
                        f.write(full_url + '\n')
                    break

                elif any(sig in content for sig in uploader_signatures):
                    print(f"{wh}[{g}+{wh}] [GOTCHAAAA!!!] {full_url}")
                    os.makedirs('Result', exist_ok=True)
                    with open('Result/uploader-shell.txt', 'a') as f:
                        f.write(full_url + '\n')
                    break

                elif any(sig in content for sig in mailer_signatures):
                    print(f"{wh}[{g}+{wh}] [GOTCHAAAA!!!] {full_url}")
                    os.makedirs('Result', exist_ok=True)
                    with open('Result/mailer.txt', 'a') as f:
                        f.write(full_url + '\n')
                    break

                elif any(sig in content for sig in pass_shell):
                    print(f"{wh}[{g}+{wh}] [GOTCHAAAA!!!] {full_url}")
                    os.makedirs('Result', exist_ok=True)
                    with open('Result/pass-shell.txt', 'a') as f:
                        f.write(full_url + '\n')
                    break

                else:
                    print(f"{wh}[{r}!{wh}] [NOT FOUND] {full_url}")

            except httpx.RequestError:
                print(f"{wh}[{c}~{wh}] [WEBSITE DIE] {url}")
                return

    except Exception as e:
        print(f"{bg_red}[ERROR] {str(e)}")

async def apsigblk():
    clear()
    print(banner)
    print(f"{wh}[{g}+{wh}] Using tools PRIV8 SHELL FINDER\n")

    try:
        file_name = input(f'{wh}[{g}~{wh}] WEBSITE LIST : ')
        with open(file_name, 'r', encoding="utf8", errors='ignore') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        threads = int(input(f'{wh}[{g}~{wh}] THREAD (concurrency) : '))
        semaphore = asyncio.Semaphore(threads)

        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            tasks = []
            for url in targets:
                tasks.append(worker(url, client, semaphore))
            await asyncio.gather(*tasks)

    except FileNotFoundError:
        print(f"{wh}[{r}!{wh}]  FILE NOT FOUND")
    except Exception as e:
        print(f"{bg_red}[ERROR] {str(e)}")

async def worker(url, client, semaphore):
    async with semaphore:
        await finder(url, client)

if __name__ == '__main__':
    try:
        asyncio.run(apsigblk())
    except KeyboardInterrupt:
        print("\n" + f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Exiting...")
        sys.exit()
