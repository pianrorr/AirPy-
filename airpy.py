import argparse
import socket
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
        description="AirPy - Python Tools",
        epilog="example: & python airpy.py --dnslookup domain.com"
        )
parser.add_argument("--hostname", action="store_true")
parser.add_argument("--pscan")
parser.add_argument("--dnslookup")
parser.add_argument("--source")
parser.add_argument("--crawler")
args = parser.parse_args()

def scan(ports):
    with socket.socket(socket.AF_INET) as s:
        s.settimeout(3)
        try:
            hasil = s.connect_ex((args.pscan, ports))
            if hasil == 0:
                print(f"[✓] Port Open {ports}")
            else:
                print(f"[x] Port Close {ports}")
        except socket.timeout:
            print(f"[-] Port Timeout {ports}")
        except ConnectionRefusedError:
            print(f"[!] Conection Rejected")
        except ConnectionResetError:
            print("[!] Connection Was Focibly Closed")
        except Exception as e:
            print(f"[!] ERROR: {e}")

if args.pscan:
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(scan, [21,22,23,25,53,80,110,111,135,139,143,443,445,587,993,995,1433,3306,3389,5432,5900,6379,8080,8443])

try:
    if args.hostname:
        print(f"HOSTNAME: {socket.gethostname()}")
    if args.dnslookup:
        print(f"Domain: {args.dnslookup}")
        print(f"IP ADDRESS: {socket.gethostbyname(args.dnslookup)}")

    if args.source:
        r = requests.get(args.source, timeout=5)
        print(r.text)
    if args.crawler:
        r = requests.get(args.crawler, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        print("-- CRAWLING ALL LINK --")
        for link in soup.find_all("a"):
            print(link.get("href"))

except requests.exceptions.Timeout:
    print("[-] TIMEOUT")
except socket.gaierror as e:
    print(f"DNS LOOKUP ERROR: {e}")
except OSError as e:
    print(f"SOCKET ERROR: {e}")
except ConnectionRefusedError:
    print(f"[!] Conection Rejected")
except ConnectionResetError:
    print("[!] Connection Was Focibly Closed")
except Exception as e:
    print(f"[!] ERROR: {e}")
