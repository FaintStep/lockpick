import subprocess
import re
import os
import datetime
import requests
import json
import argparse
from ftplib import FTP

LOG_DIR = "logs"
PROMPT_FILE = "prompts/recon_summary.txt"

# Functions

def banner():
    banner = r"""
    

         .-'''-.           _..._                                                   _..._                   
.---.   '   _    \      .-'_..._''.                                             .-'_..._''.                
|   | /   /` '.   \   .' .'      '.\    .       _________   _...._      .--.  .' .'      '.\    .          
|   |.   |     \  '  / .'             .'|       \        |.'      '-.   |__| / .'             .'|          
|   ||   '      |  '. '             .'  |        \        .'```'.    '. .--.. '             .'  |          
|   |\    \     / / | |            <    |         \      |       \     \|  || |            <    |          
|   | `.   ` ..' /  | |             |   | ____     |     |        |    ||  || |             |   | ____     
|   |    '-...-'`   . '             |   | \ .'     |      \      /    . |  |. '             |   | \ .'     
|   |                \ '.          .|   |/  .      |     |\`'-.-'   .'  |  | \ '.          .|   |/  .      
|   |                 '. `._____.-'/|    /\  \     |     | '-....-'`    |__|  '. `._____.-'/|    /\  \     
'---'                   `-.______ / |   |  \  \   .'     '.                     `-.______ / |   |  \  \    
                                 `  '    \  \  \'-----------'                            `  '    \  \  \   
                                   '------'  '---'                                         '------'  '---' 

"""
    red = "\033[91m"
    reset = "\033[0m"
    print(red + banner + reset)

def run_nmap(target):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"nmap_{timestamp}.txt")
    print(f"[INFO] Running nmap scan on {target}...")

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    command = ["nmap","-sV","-p-","-A","-T4",target]
    with open(log_file, "w") as output:
        subprocess.run(command,stdout=output)

    print(f"[INFO] Nmap results saved to {log_file}")
    return log_file

def guess_os(nmap_output):
    os_guess = "unknown"

    with open(nmap_output, "r") as f:
        content = f.read().lower()

    # Common indicators from OS detection, banners, or service strings
    if "windows" in content or "microsoft" in content:
        os_guess = "windows"
    elif "linux" in content or "ubuntu" in content or "debian" in content or "centos" in content:
        os_guess = "linux"
    elif "samba" in content:
        os_guess = "linux"  # SMB on Linux usually means Samba

    print(f"[INFO] OS Guess: {os_guess}")
    return os_guess

def extract_http_ports(nmap_output):
    http_ports = []

    with open(nmap_output, 'r') as f:
        lines = f.readlines()

        for line in lines:
            # Use regex to find lines where common HTTP ports numbers are included
            if 'http' in line and 'open' in line:
                  match = re.search(r'(\d+)/tcp\s+open\s+http', line)
                  if match:
                    http_ports.append(match.group(1))
        
        # Return a list of found ports
        return http_ports

def find_subdomains(target):
    command = ["ffuf","-H", f"Host:FUZZ.{target}","-w","/home/user/Wordlists/Discovery/DNS/bitquark-subdomains-top100000.txt","-u",target]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR,f"subdomains_{timestamp}.txt")
    with open(log_file,"w") as output:
        subprocess.run(command,stdout=output)

    print(f"DNS fuzzing saved to {log_file}")
    return log_file

def check_anonymous_ftp(target):
    try:
        ftp = FTP(target)
        ftp.login()
        print(f"[+] Anonymous FTP access is available on {target}!")
        ftp.quit()
    except Exception as e:
        print(f"[-] Failed to login anonymously on {target}. Reason: {e}")

def check_smb_guest(target):
    try:
        print(f"[INFO] Checking SMB guest access on {target}...")
        command = [
            "smbclient", "-L", f"//{target}/", "-N", "-g"
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)

        if "Disk|" in result.stdout or "IPC|" in result.stdout:
            print(f"[+] SMB guest access appears to be enabled on {target}")
            return True
        else:
            print(f"[-] SMB guest access denied or no shares visible on {target}")
            return False

    except Exception as e:
        print(f"[ERROR] SMB guest check failed: {e}")
        return False

