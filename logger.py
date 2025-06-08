import os
from datetime import datetime

def init_log(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"{timestamp}_log.md")
    with open(log_path) as f:
        f.write(f"# Lockpick Recon Log - {timestamp}\n")
    return log_path

def log_step(log_path,title,command,output,max_length=2000):
    if len(output) > max_length:
        output = output[:max_length] + "\n[...output truncated...]"
    with open(log_path, "a") as f:
        f.write(f"\n## {title}\n")
        f.write(f"**Command:** `{command}`\n")
        f.write(f"**Output:**\n```\n");
        f.write(output.strip() + "\n```\n")



    
