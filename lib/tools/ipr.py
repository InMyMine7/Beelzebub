from lib.tools.utils import banner, clear
from lib.tools.colors import wh, r, g, res
def scan(site):

    ur = site.rstrip()
    ch = site.split('\n')[0].split('.')
    ip1 = ch[0]
    ip2 = ch[1]
    ip3 = ch[2]
    taz = str(ip1) + '.' + str(ip2) + '.'
    i = 0
    while i <= 255:
        i += 1
        c = 0
        while c <= 255:
            c += 1
            print(f'{wh}[{g}+{wh}] Ranging ==>' + str(taz) + str(c) + '.' + str(i))
            with open('Result/range.txt', 'a') as file:
                file.write(str(taz) + str(c) + '.' + str(i) + '\n')

def hihiha():    
    try:
        clear()
        print(banner)
        nam = input(f'{wh}[{g}+{wh}] List IPs: ')
        try:
            with open(nam, 'r') as f:
                for site in f:
                    scan(site)
            print(f'{wh}[{g}+{wh}] Scanning is complete. Results are saved in {g}Result/range.txt{res}')
            
        except FileNotFoundError:
            print(f"{wh}[{g}!{wh}] Error: File '{nam}' tidak ditemukan!")
        except Exception as e:
            print(f"{wh}[{g}!{wh}] An error occurred: {str(e)}")

    except Exception as e:
        print(f"{wh}[{g}!{wh}] Terjadi error fatal: {str(e)}")

if __name__ == "__main__":
    hihiha()