import requests
import os

def summarize_log(log_path,prompt_path="prompts/summary.txt",model="Mistral",export_path="exports/pasteable_summary.md"):
    with open(prompt_path, "r") as f:
        prompt = f.read()
    with open(log_path, "r") as f:
        log = f.read()

    full_prompt = f"{prompt}\n\n{log}"
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt" : full_prompt,
        "stream": False
    })

    summary = response.json().get("response", "[No response received]")

    with open(log_path, "a") as f:
        f.write("\n## AI Summary\n")
        f.write(summary + "\n")

    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, "w") as f:
        f.write(summary)

    return summary


