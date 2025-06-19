import json
import os
import argparse
from summarize import summarize_report

def add_manual_finding(target, finding, question=None, report_dir="logs"):
    path = os.path.join(report_dir, f"report_state_{target}.json")

    if not os.path.exists(path):
        print( f"[!] No existing report found for {target}")
        return
    
    with open(path, "r") as f:
        report = json.load(f)

    finding_entry = {"text": finding.strip()}
    if question:
        finding_entry["question"] = question.strip()
    
    report.setdefault("manual_findings", [])

    if finding_entry not in report["manual_findings"]:
            report["manual_findings"].append(finding_entry)
            with open(path, "w") as f:
                json.dump(report, f, indent=2)
            print(f"[+] Added manual finding to {target}: {finding}")
    else:
        print(f"[=] Finding already exists. Skipping duplicate.")
    
    print("[*] Re-analyzing with LLM..\n")
    summarize_report(report, args.model)

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", required=True, help="Target domain")
    parser.add_argument("--add-finding", "-f", required=True, help="Manual finding to add")
    parser.add_argument("--question", "-q", help="Optional question to include for LLM")
    parser.add_argument("--model", choices=["mistral", "gemma:7b", "llama3"], default="mistral", help="Which LLM model to use")
    args = parser.parse_args()

    add_manual_finding(args.target,args.add_finding,args.question)

