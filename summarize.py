import json
import requests
import os

def summarize_report(report_data, model="mistral", endpoint="http://localhost:11434/api/generate"):
    prompt = "Analyze the following penetration test results. Identify potential attack paths, vulnerabilities, or follow-up recon suggestions. What technologies are running? What does the website look like? Provide suggestions as to what might be most valuable to investigate or attempt to exploit next.\n\n"

    if "nmap" in report_data and os.path.exists(report_data["nmap"]):
        prompt += "## Nmap Results:\n"
        with open(report_data["nmap"], "r") as f:
            for line in f:
                prompt += f"- {line.strip()}\n"

    if "ftp" in report_data and report_data["ftp"]:
        prompt += f"\n## Anonymous FTP Access: {report_data['ftp']}\n"

    if "smb" in report_data and report_data["smb"]:
        prompt += f"\n## SMB Guest Access: {report_data['smb']}\n"

    if "subdomains" in report_data and report_data["subdomains"]:
        prompt += "\n## Subdomains Discovered:\n"
        for sub in report_data["subdomains"]:
            prompt += f"- {sub}\n"

    if "http_paths" in report_data and report_data["http_paths"]:
        prompt += "\n## Web Paths Discovered:\n"
        for path in report_data["http_paths"]:
            prompt += f"- {path}\n"

    if "screenshots" in report_data and os.path.exists(report_data["screenshots"]):
        prompt += "\n## gowitness Web Metadata:\n"
        with open(report_data["screenshots"], "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    prompt += f"- URL: {entry.get('url')}\n"
                    prompt += f"  - Title: {entry.get('title')}\n"
                    prompt += f"  - Status Code: {entry.get('status_code')}\n"
                    headers = entry.get("headers")
                    if isinstance(headers, dict):
                        for k, v in headers.items():
                            prompt += f"    - Header: {k}: {v}\n"
                    print(f"[DEBUG] Parsed gowitness entry: {entry}")
                except json.JSONDecodeError:
                    continue

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    print("[INFO] Sending prompt to LLM...")
    print("[DEBUG] Final prompt sent to model:\n", prompt)
    try:
        res = requests.post(endpoint, json=payload)
        res.raise_for_status()
        data = res.json()
        summary = data.get("response", "").strip()
        print("[INFO] LLM summarization complete.")
        print(f"Lockpick says: {summary}")
        return summary
    except Exception as e:
        print(f"[ERROR] Failed to summarize: {e}")
        return None

