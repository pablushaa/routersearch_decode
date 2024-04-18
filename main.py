from colorama import init, Fore, Back, Style # nekit privet
from urllib import request
import ipaddress
import threading
import socket
import time
import json

# loading configs
with open('settings/config.json') as file:
    cfg = json.load(file)
 
ports = []
for port in list(cfg["ports"]): ports.append(str(port))
must_letters = cfg["lettets"]
ignore_unknown = cfg["ign_unknown"]
search = open("settings/search.txt").read().split("\n")
banlist = open("settings/banlist.txt").read().split("\n")
if not search or search == [""]: bsearch = False
else: bsearch = True
if not banlist or banlist == [""]: blist = False
else: blist = True

socket.setdefaulttimeout(0.1)

# printing scan info
print(f"{Style.BRIGHT}Ports:{Style.RESET_ALL} {Fore.CYAN}{' '.join(ports)}{Style.RESET_ALL} ")
if bsearch: print(f"{Style.BRIGHT}Searching:{Style.RESET_ALL} {Fore.GREEN}{bsearch}{Style.RESET_ALL}")
else: print(f"{Style.BRIGHT}Searching:{Style.RESET_ALL} {Fore.RED}{bsearch}{Style.RESET_ALL}")
if blist: print(f"{Style.BRIGHT}Banlist:{Style.RESET_ALL} {Fore.GREEN}{blist}{Style.RESET_ALL}")
else: print(f"{Style.BRIGHT}Banlist:{Style.RESET_ALL} {Fore.RED}{blist}{Style.RESET_ALL}")
if must_letters: print(f"{Style.BRIGHT}Must title have letters:{Style.RESET_ALL} {Fore.GREEN}{must_letters}{Style.RESET_ALL}")
else: print(f"{Style.BRIGHT}Must title have letters:{Style.RESET_ALL} {Fore.RED}{must_letters}{Style.RESET_ALL}")
if ignore_unknown: print(f"{Style.BRIGHT}Ignore unknown titles:{Style.RESET_ALL} {Fore.GREEN}{ignore_unknown}{Style.RESET_ALL}")
else: print(f"{Style.BRIGHT}Ignore unknown titles:{Style.RESET_ALL} {Fore.RED}{ignore_unknown}{Style.RESET_ALL}")

print("=" * 30)

# vsyakiye funccii

def get_ip_range(line):
    l = line.replace("\n", "").split("-")
    start_ip = l[0]
    end_ip = l[1]
    try:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)

        ip_range = []
        for ip in range(int(start), int(end) + 1):
            ip_range.append(str(ipaddress.IPv4Address(ip)))

        return ip_range

    except ValueError as e:
        print("Error:", e)
        return None


def check(url):
    try:
        sock = socket.socket()
        add = url.split(":")
        sock.connect((add[0], int(add[1])))
    except: return False
    else:
        sock.close(); return True


def letters(s):
    if must_letters:
        return any(char.isalpha() for char in s)
    else: return True


def get_title(url):
    try:
        with request.urlopen(url) as response:
            html = str(response.read())
        title = html.lower().split("<title>")[1].split("<")[0]
        if letters(title) and must_letters:
            return title
        elif not must_letters:
            return title
        else:
            return "Unknown/redirect"

    except: return "Unknown/redirect"


def scan(ip):
    if check(ip) == True:
        url = f"http://{ip}"
        title = get_title(url)
        if bsearch:
            for elem in search:
                if elem in title and elem != "Unknown/redirect":
                    print(f"{Style.BRIGHT}{url}{Style.RESET_ALL} >> {Fore.CYAN}{title}{Style.RESET_ALL}")
        elif any(item in title for item in banlist): pass
        elif title == "Unknown/redirect" and ignore_unknown == False:
            print(f"{Style.BRIGHT}{url}{Style.RESET_ALL} >> {Fore.CYAN}{title}{Style.RESET_ALL}")
        elif title != "Unknown/redirect":
            print(f"{Style.BRIGHT}{url}{Style.RESET_ALL} >> {Fore.CYAN}{title}{Style.RESET_ALL}")


start_time = time.time()

# main for wow

for line in open("settings/ips.txt").readlines():
    for ip in get_ip_range(line):
        for port in ports:
            lol = f"{ip}:{port}"
            thread = threading.Thread(target=lambda: scan(lol))
            thread.start()

end_time = time.time()
print(f"Scanned all ips in {int(end_time - start_time)} seconds")