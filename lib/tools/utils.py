import os
import platform
import ctypes
import sys
from lib.tools.colors import r, wh, g, res, yl, bg_gr, bg_wh, bg_red, rst,c, o

def set_console_title(title):
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif platform.system() in ["Linux", "Darwin"]:
        sys.stdout.write(f"\33]0;{title}\a")
        sys.stdout.flush()
    else:
        print("")

set_console_title("Beelzebub >_")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

banner = f'''
{g}
 ▄▄▄▄   ▓█████ ▓█████  ██▓    ▒███████▒▓█████  ▄▄▄▄    █    ██  ▄▄▄▄   
▓█████▄ ▓█   ▀ ▓█   ▀ ▓██▒    ▒ ▒ ▒ ▄▀░▓█   ▀ ▓█████▄  ██  ▓██▒▓█████▄ 
▒██▒ ▄██▒███   ▒███   ▒██░    ░ ▒ ▄▀▒░ ▒███   ▒██▒ ▄██▓██  ▒██░▒██▒ ▄██
▒██░█▀  ▒▓█  ▄ ▒▓█  ▄ ▒██░      ▄▀▒   ░▒▓█  ▄ ▒██░█▀  ▓▓█  ░██░▒██░█▀  
░▓█  ▀█▓░▒████▒░▒████▒░██████▒▒███████▒░▒████▒░▓█  ▀█▓▒▒█████▓ ░▓█  ▀█▓
░▒▓███▀▒░░ ▒░ ░░░ ▒░ ░░ ▒░▓  ░░▒▒ ▓░▒░▒░░ ▒░ ░░▒▓███▀▒░▒▓▒ ▒ ▒ ░▒▓███▀▒
▒░▒   ░  ░ ░  ░ ░ ░  ░░ ░ ▒  ░░░▒ ▒ ░ ▒ ░ ░  ░▒░▒   ░ ░░▒░ ░ ░ ▒░▒   ░ 
 ░    ░    ░      ░     ░ ░   ░ ░ ░ ░ ░   ░    ░    ░  ░░░ ░ ░  ░    ░ 
 ░         ░  ░   ░  ░    ░  ░  ░ ░       ░  ░ ░         ░      ░      
      ░                       ░                     ░                ░ v1.6 Remaster                                                                                     
    |{wh} Coded By '/Mine7 {g} | {wh}t.me/minesepen {g}| {wh}github.com/InMyMine7 {g}| 
  {res}'''

List = f'''
{wh}[{g}1{res}]{yl} Priv8 Beelzebub{res} {g}(Priv8 Shell finder, index of shell finder, autoxploit, and more)
{wh}[{g}2{res}]{yl} Mirror Grabber {g}(zoneh, zonexsec, haxorid){o}
{wh}[{g}3{res}]{yl} Domain Grabber {g}(Grabber by keyword, date, extension, Wordpress, google dorking and more) {o}
{wh}[{g}4{res}]{yl} Dork Maker {g}(wordpress, joomla, opencart) {res}
{wh}[{g}5{res}]{yl} Dork Scanner {res}
{wh}[{g}6{res}]{yl} CMS Checker {g}(Wp, joomla, drupal, magento, shopify, blogger, pretashop, wix, Squarespace and more.) {res}
{wh}[{g}7{res}]{yl} ReverseIP {g}(6 api) {res}
{wh}[{g}8{res}]{yl} Domain To IP{res}
{wh}[{g}9{res}]{yl} IPrange{res}
{wh}[{g}10{res}]{yl} IP live checker{res}
{wh}[{g}11{res}]{yl} URL Cleaner {g}(domain duplicate remover) {res}
{wh}[{g}12{res}]{yl} WP-Brute xmlrpc and wplogin {g}(auto upload shell from plugin and theme){res}
{wh}[{g}13{res}]{yl} env scanner {g}(get SMTPs, twilio, aws key, nexmo, mysql ){res}
{wh}[{g}14{res}]{yl} Combolist Checker {g}(wordpres, cpanel, whm, webmail and more){res}
{wh}[{g}15{res}]{yl} Wordpress auto upload shell {g}(fromat www.site.com/wp-login.php#user@pass){res}

{wh}[{g}98{res}]{yl} Donate for fast update{res}
{wh}[{g}99{res}]{yl} EXIT{res}
'''

menu_rev = '''
\033[97m[\033[92m+\033[97m] Reverse IP with 6 api

\033[97m[\033[92m+\033[97m] 1. FAST BUT LESS DOMAIN
\033[97m[\033[92m+\033[97m] 2. SLOW BUT MORE DOMAIN
'''
list_grabber = '''
\033[97m[\033[92m+\033[97m] 1. Domain Grabber Azstats
\033[97m[\033[92m+\033[97m] 2. Domain Grabber Bestwebsiterank
\033[97m[\033[92m+\033[97m] 3. Domain Grabber Topmillion
\033[97m[\033[92m+\033[97m] 4. Domain Grabber Dubdomain
\033[97m[\033[92m+\033[97m] 5. Wordpress Domain Grabber
\033[97m[\033[92m+\033[97m] 6. Wordpress Theme Grabber
\033[97m[\033[92m+\033[97m] 7. Domain Grabber By Date v1 (\033[93m use vpn opsional \033[97m)
\033[97m[\033[92m+\033[97m] 8. Domain Grabber By Date v2 (\033[93m use vpn opsional \033[97m)
\033[97m[\033[92m+\033[97m] 9. Domain Grabber By Keyword
\033[97m[\033[92m+\033[97m] 10. Domain Grabber Greensite
\033[97m[\033[92m+\033[97m] 11. Google Dorking
\033[97m[\033[92m+\033[97m] 12. Domain Grabber Onshopify
'''
combolist_list = '''
\033[97m[\033[92m+\033[97m] Crack WP panel from Combo List
\033[97m[\033[92m+\033[97m] Crack cPanel from Combo List
\033[97m[\033[92m+\033[97m] Crack SMTP from Combo List
\033[97m[\033[92m+\033[97m] Crack WHM from Combo List
\033[97m[\033[92m+\033[97m] Crack Webmails from Combo List

'''
pepek = '''
  /$$$$$$                               
 /$$__  $$                              
| $$  \__/  /$$$$$$   /$$$$$$  /$$$$$$$ 
|  $$$$$$  /$$__  $$ /$$__  $$| $$__  $$
 \____  $$| $$  \ $$| $$  \ $$| $$  \ $$
 /$$  \ $$| $$  | $$| $$  | $$| $$  | $$
|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$  | $$
 \______/  \______/  \______/ |__/  |__/
                                        
                                        
                                        
'''

donate = '''
saweria : saweria.co/InMyMine7
Buymecoffe : buymeacoffee.com/inmymine72
btc : bc1qlx7n3x3wvacd6dnpv48ksk9zfvu7pvk904xr3s
'''