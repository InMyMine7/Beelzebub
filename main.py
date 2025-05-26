import sys
import asyncio
import os

from lib.tools.utils import clear, banner, List, pepek, donate
from lib.tools.colors import r, g, wh, res, bg_red
from lib.tools.dm import dork
from lib.tools.dk import dk
from lib.tools.cmc import cmx
from lib.tools.dg import digidaw
from lib.tools.mr import komeng
from lib.tools.rs import wutwut
from lib.tools.p import notnot
from lib.tools.ipr import hihiha
from lib.tools.ipc import koncet
from lib.tools.drc import xontol
from lib.tools.sf import apsigblk
from lib.tools.uplwp import blublub
from lib.tools.indsf import kontolbgt
from lib.tools.lr import urfavmine
from lib.tools.cker import BruteForceTool
from lib.tools.brt import wp
if not os.path.exists('Result'):
    os.makedirs('Result')

async def menu():
    clear()
    print(banner + List)
    while True:
        try:
            pilih = input(f"{wh}[{g}-{wh}] root@Beelzebub : ")

            if pilih == "1":
                clear()
                print(banner)
                print (f"{wh}[{g}1{res}]{wh} Shell Finder {g}(Find backdoor on website from list in lib/files/shell-path.txt) {res}\n{wh}[{g}2{res}]{wh} IndexOf Shell Finder {g}(Find backdoor on directory index of website from list in lib/files/path.txt)\n{wh}[{g}3{res}]{wh} Priv8 AutoXploit \n")
                beelz = input(f"{wh}[{g}-{wh}] root@Beelzebub : {res}")
                if beelz == "1":
                    await apsigblk()
                elif beelz == "2":
                    await kontolbgt()
                elif beelz == "3":
                    clear()
                    print(pepek)
            elif pilih == "2":
                komeng()
            elif pilih == "3":
                digidaw()
            elif pilih == "4":
                dork()
            elif pilih == "5":
                dk()
            elif pilih == "6":
                cmx()
            elif pilih == "7":
                wutwut()
            elif pilih == "8":
                notnot()
            elif pilih == "9":
                hihiha()
            elif pilih == "10":
                koncet()
            elif pilih == "11":
                xontol()
            elif pilih == "12":
                await wp()
            elif pilih == "13":
                urfavmine()
            elif pilih == "14":
                tool = BruteForceTool()
                tool.cker()
            elif pilih == "15":
                blublub()
            elif pilih == "98":
                clear()
                print(donate)
            elif pilih == "99":
                print("Thanks for using my tools <3")
                sys.exit(0)
            else:
                print(f"{r}Invalid choice. Please enter a valid option.{res}")
                continue

            back = input(f"\n{wh}[{g}?{wh}] Back to main menu? (y/n): ")
            if back.lower() == "y":
                clear()
                print(banner + List)
                continue
            else:
                print("Thanks for using my tools <3")
                sys.exit(0)

        except FileNotFoundError:
            print(f"{wh}[{g}!{wh}] Error: File Not Found")
            sys.exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(menu())
    except (KeyboardInterrupt, EOFError):
        print(f"\n{bg_red}Program terminated by user.{res}")
        sys.exit(0)

