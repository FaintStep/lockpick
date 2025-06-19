```
                    ██▓     ▒█████   ▄████▄   ██ ▄█▀ ██▓███   ██▓ ▄████▄   ██ ▄█▀
                    ▓██▒    ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓██░  ██▒▓██▒▒██▀ ▀█   ██▄█▒ 
                    ▒██░    ▒██░  ██▒▒▓█    ▄ ▓███▄░ ▓██░ ██▓▒▒██▒▒▓█    ▄ ▓███▄░ 
                    ▒██░    ▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ▒██▄█▓▒ ▒░██░▒▓▓▄ ▄██▒▓██ █▄ 
                    ░██████▒░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄▒██▒ ░  ░░██░▒ ▓███▀ ░▒██▒ █▄
                    ░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒▒▓▒░ ░  ░░▓  ░ ░▒ ▒  ░▒ ▒▒ ▓▒
                    ░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░░▒ ░      ▒ ░  ░  ▒   ░ ░▒ ▒░
                    ░ ░   ░ ░ ░ ▒  ░        ░ ░░ ░ ░░        ▒ ░░        ░ ░░ ░ 
                        ░  ░    ░ ░  ░ ░      ░  ░             ░  ░ ░      ░  ░   
                                    ░                            ░               
```



# Automated Recon & LLM-based Analysis for Offensive Security
Primarily designed for local use in labs, CTFs, or structured red team exercises.

# Features
- Modular Recon Chains: Implement your unique methodology. Define action chains with JSON to dictate the specifics of your workflow. Run only the automated scans and check you like, or simply use the default. "Steps" can also be disabled via a flag value in the action_chains JSON structure as a simple on/off switch if you'd rather not remove the action altogether. Helps with quick testing and modifications to methodology. 

- LLM Summarization: Pair scan output with local LLMs (via Ollama) for summarization of findings and recommendations around additional enumeration and exploitation. Lockpick currently supports choices for mistral, LLaMA3, and Gemma:7B out-of-the-box. This is easily modifiable with some simple tweaks if you have a preference for other models.

- Manual Findings Support: Add your own findings (SQLi, LFI, XSS, SSRF) using arguments in report.py. This allows you to take notes as you learn more about your targets. A finding can also be paired with a question via the --question flag (also in report.py) to create finding/question sets that then get fed back to the LLM for up-to-date output that takes developments into consideration.

- Persistent Reporting: report_state_{target}.json captures all scan results and manual inputs across a target lifecycle. This could simply be modified directly if someone wishes to bypass the CLI and instead write out their findings as they were in a text document.

# Requirements
- Python 3.8+
- Ollama (for local LLM inference)
- Dependency tools and libaries:
    - nmap
    - ffuf
    - gowitness

Planned requirements.txt to come.

# Quick Start
# Run default chain
```
python3 runner.py --target example.htb --chain action_chains/default.json
```

# Add manual finding and re-summarize
```
python3 report.py --target example.htb --add-finding "LFI found at /download?file=../../../etc/passwd" --question "What files might be sensitive on Apache servers?"
```

# View the live summarized report
```
cat logs/report_state_example.json
```

# Roadmap
- requirements.txt for easy installation of dependencies
- More Windows-specific attack automation (BloodHound collection, Kerberoasting, AS-REP)
- Report export to HTML or markdown

This tool is intended for authorized testing, training, and research only. Unauthorized access to systems using this tool is strictly prohibited.