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
    "check_smb_guest": check_smb_guest,
    "enum4linux_ng": enum4linux_ng,
    "gowitness": gowitness
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

        if step.get("disabled"):
            print(f"[SKIP] Skipping disabled step: {step['name']}")
            continue

        if condition:
            if not evaluate_condition(condition, state):
                print(f"[-] Skipping {name} due to failed condition.")
                continue

        if tool not in TOOL_FUNCTIONS:
            print(f"[!] Unknown tool: {tool}")
            continue

        resolved_args = resolve_args(args, state, target , wordlist)
        print(f"[+] Running {name} ({tool}) with args: {resolved_args}")
        result = TOOL_FUNCTIONS[tool](**resolved_args)

        # Save result into state using step name
        state[name] = result
    print(f"State of step: {state}")
    update_report_state(state, target)

def update_report_state(state, target):
    path = f"logs/report_state_{target}.json"
    report = {}

    # Load existing state
    if os.path.exists(path):
        with open(path, "r") as f:
            report = json.load(f)

    # Update
    report["nmap"] = state.get("nmap_scan") or "No Nmap scan result"
    report["ftp"] = state.get("ftp_check") or ""
    report["smb"] = state.get("check_smb_guest") or ""
    report["subdomains"] = state.get("dns_fuzz") or []
    report["http_paths"] = state.get("fuzz_http_80") or []
    report["screenshots"] = os.path.join(state.get("screenshot_web", ""), "gowitness.jsonl")

    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    
    summarize_report(report)


if __name__ == "__main__":
    # Set up argument parser to ingest target IP/global variables
    parser = argparse.ArgumentParser(description="Lockpick: Recon and Exploit Assistant")
    parser.add_argument("--model",default="llama3",help="Ollama model")
    parser.add_argument("--summarize",action="store_true", help="Use mistral to summarize recon results")
    parser.add_argument("--t", required=True, help="Target IP or hostname")
    parser.add_argument("--w", required=True, help="Wordlist for webdir fuzzing")
    parser.add_argument("--chain", required=True, default="action_chains/default.json", help="Path to action chain JSON")
    args = parser.parse_args()
    banner()
    chain = load_chain(args.chain)
    run_chain(chain, args.t, args.w)