import json
import argparse
import re
from recon import *

# Registry of allowed tool functions
TOOL_FUNCTIONS = {
    "run_nmap": run_nmap,
    "guess_os": guess_os,
    "extract_http_ports": extract_http_ports,
    "find_subdomains": find_subdomains,
    "fuzz_http_dirs": fuzz_http_dirs,
    "check_anonymous_ftp": check_anonymous_ftp,
    "check_smb_guest": check_smb_guest
}

def load_chain(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def resolve_args(args_dict, state, target, wordlist):
    resolved = {}
    for k, v in args_dict.items():
        if isinstance(v, str):
            # Replace {{target}} placeholder
            v = v.replace("{{target}}", target)
            v = v.replace("{{wordlist}}", wordlist)
            # Handle references like $step_name
            if v.startswith("$"):
                ref_key = v[1:]
                v = state.get(ref_key)
        resolved[k] = v
    return resolved

def evaluate_condition(condition, state):
    try:
        return eval(condition, {}, state)
    except Exception as e:
        print(f"[!] Failed to evaluate condition '{condition}': {e}")
        return False

def run_chain(chain, target, wordlist):
    state = {}
    for step in chain:
        name = step["name"]
        tool = step["tool"]
        args = step.get("args", {})
        condition = step.get("condition")

        if condition:
            if not evaluate_condition(condition, state):
                print(f"[-] Skipping {name} due to failed condition.")
                continue

        if tool not in TOOL_FUNCTIONS:
            print(f"[!] Unknown tool: {tool}")
            continue

        resolved_args = resolve_args(args, state, target, wordlist)
        print(f"[+] Running {name} ({tool}) with args: {resolved_args}")
        result = TOOL_FUNCTIONS[tool](**resolved_args)

        # Save result into state using step name
        state[name] = result
    print(f"State of step: {state}")
    return state

if __name__ == "__main__":
    # Set up argument parser to ingest target IP/global variables
    parser = argparse.ArgumentParser(description="Lockpick: Recon and Exploit Assistant")
    parser.add_argument("--model",default="mistral",help="Ollama model")
    parser.add_argument("--summarize",action="store_true", help="Use mistral to summarize recon results")
    parser.add_argument("--t", required=True, help="Target IP or hostname")
    parser.add_argument("--w", required=True, help="Wordlist for webdir fuzzing")
    parser.add_argument("--chain", required=True, default="action_chains/default.json", help="Path to action chain JSON")
    args = parser.parse_args()
    banner()
    chain = load_chain(args.chain)
    run_chain(chain, args.t, args.w)