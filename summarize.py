import json
import requests

def summarize_gowitness_jsonl(jsonl_path, model="mistral", endpoint="http://localhost:11434/api/generate"):
    entries = []
    with open(jsonl_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                entries.append(data)
            except json.JSONDecodeError:
                continue

    prompt = "Analyze the following web service scan results and summarize any interesting technologies, misconfigurations, or attack surface paths. Focus on titles, server headers, and HTTP status codes.\n\n"
    for entry in entries:
        prompt += f"- URL: {entry.get('url')}\n"
        prompt += f"  - Title: {entry.get('title')}\n"
        prompt += f"  - Status Code: {entry.get('status_code')}\n"
        headers = entry.get("headers")
        if isinstance(headers, dict):
            for k, v in headers.items():
                prompt += f"    - Header: {k}: {v}\n"
        elif isinstance(headers, list):
            for header in headers:
                prompt += f"    - Header: {header}\n"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    print("[INFO] Sending prompt to LLM...")
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


