import subprocess
import re
import os
import datetime
import requests
import json
import argparse

# Set up argument parser to ingest target IP
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


