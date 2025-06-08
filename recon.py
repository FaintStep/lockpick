import subprocess
import re
import os
import datetime
import requests
import json
import argparse

# Set up argument parser to ingest target IP/global variables
parser = argparse.ArgumentParser(description="Lockpick: Recon and Exploit Assistant")
parser.add_argument("target",help="Target IP address")
parser.add_argument("wordlist",help="Wordlist for ffuf fuzzer")
parser.add_argument("--model",default="mistral",help="Ollama model")
parser.add_argument("--summarize",action="store_true", help="Use mistral to summarize recon results")
# Possible future addition of --url-path to insert FUZZ at different parts of URL, more dynamic/automated FUZZING
args = parser.parse_args()

TARGET = args.target
WORDLIST = args.wordlist
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
    print(f"[+] Running nmap scan on {target}...")

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    command = ["nmap","-sV","-p-","-A","-T4",target]
    with open(log_file, "w") as output:
        subprocess.run(command,stdout=output)

    print(f"[+] Nmap results saved to {log_file}")
    return log_file

# Main execution
if __name__ == "__main__":
    banner()
    nmap_output = run_nmap(TARGET)


