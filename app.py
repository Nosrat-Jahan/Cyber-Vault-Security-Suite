"""
-----------------------------------------------------------------------------
FILE     : cyber_vault_v9.py
VERSION  : 9.9.9 [Enterprise Security Suite]
DEV      : Nosrat Jahan
ACADEMIC : BSc in Computer Science & Engineering
-----------------------------------------------------------------------------
"""

from flask import Flask, render_template_string, request, jsonify
import hashlib
import re
import webbrowser

app = Flask(__name__)

# Core Logic: Advanced Password Complexity Analysis
def perform_security_audit(payload):
    score = 0
    if len(payload) >= 8: score += 1
    if re.search(r"[a-z]", payload) and re.search(r"[A-Z]", payload): score += 1
    if re.search(r"[0-9]", payload): score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', payload): score += 1
    
    status_map = {0: "Insecure", 1: "Weak", 2: "Average", 3: "Good", 4: "Robust"}
    return status_map.get(score, "Insecure"), (score / 4) * 100

# Professional Slate & Cyan Theme Design
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cyber-Vault | Security Engine</title>
    <style>
        :root {
            --bg: #0b0e14;
            --card: #151921;
            --accent: #00f2ff;
            --text: #f0f6fc;
            --muted: #8b949e;
            --border: #30363d;
        }
        .gray-mode {
            --bg: #f6f8fa;
            --card: #ffffff;
            --accent: #0969da;
            --text: #1f2328;
            --muted: #656d76;
            --border: #d0d7de;
        }
        body {
            background: var(--bg); color: var(--text);
            font-family: 'Segoe UI', system-ui, sans-serif;
            margin: 0; display: flex; flex-direction: column; align-items: center;
            min-height: 100vh; transition: background 0.4s ease;
        }
        .app-container {
            width: 90%; max-width: 580px; margin-top: 80px;
            background: var(--card); padding: 45px; border-radius: 28px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.6); border: 1px solid var(--border);
        }
        .branding { text-align: center; margin-bottom: 40px; }
        .branding h1 { font-size: 2.4rem; font-weight: 900; letter-spacing: 6px; margin: 0; color: var(--accent); }
        .branding p { color: var(--muted); font-size: 0.85rem; margin-top: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }

        .input-group { margin-bottom: 35px; }
        .input-label { font-size: 0.75rem; font-weight: 800; color: var(--muted); text-transform: uppercase; margin-bottom: 15px; display: block; }
        .cyber-input { width: 100%; box-sizing: border-box; background: rgba(0,0,0,0.25); border: 2px solid var(--border); padding: 18px; color: var(--text); border-radius: 16px; font-size: 1.1rem; outline: none; transition: 0.3s; }
        .cyber-input:focus { border-color: var(--accent); box-shadow: 0 0 20px rgba(0, 242, 255, 0.15); }

        .stat-bar { display: flex; justify-content: space-between; font-weight: 800; margin-bottom: 12px; font-size: 0.95rem; }
        .progress-track { height: 10px; background: rgba(255,255,255,0.05); border-radius: 30px; overflow: hidden; margin-bottom: 45px; }
        .progress-bar { height: 100%; width: 0%; transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1); background: var(--accent); }

        .hash-vault { background: rgba(0,0,0,0.4); padding: 25px; border-radius: 18px; border: 1px solid var(--border); position: relative; }
        .vault-label { color: var(--accent); font-size: 0.75rem; font-weight: 900; display: block; margin-bottom: 15px; text-transform: uppercase; }
        .hash-string { font-family: 'Consolas', 'Monaco', monospace; font-size: 0.85rem; word-break: break-all; opacity: 0.9; padding-right: 50px; display: block; color: var(--accent); line-height: 1.6; }
        
        .copy-trigger { position: absolute; right: 20px; top: 22px; background: none; border: none; color: var(--accent); cursor: pointer; transition: 0.2s; }
        .copy-trigger:hover { transform: scale(1.2); filter: brightness(1.4); }

        .visual-toggle { margin-top: 30px; background: transparent; color: var(--muted); border: 1px solid var(--muted); padding: 8px 20px; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.7rem; text-transform: uppercase; transition: 0.3s; }
        .visual-toggle:hover { border-color: var(--accent); color: var(--accent); }

        .global-footer { 
            margin-top: auto; 
            width: 100%; 
            padding: 35px 0; 
            text-align: center; 
            background: rgba(0,0,0,0.3); 
            border-top: 2px solid var(--border); 
            color: var(--text); 
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.8px;
        }
    </style>
</head>
<body>

    <div class="app-container">
        <div class="branding">
            <h1>CYBER-VAULT</h1>
            <p>Security Audit Module</p>
        </div>

        <div class="input-group">
            <span class="input-label">Target Data String</span>
            <input type="text" id="passIn" class="cyber-input" placeholder="Input string for real-time analysis..." autocomplete="off">
        </div>
        
        <div class="stat-bar">
            <span>METRIC: <span id="stat" style="color:var(--accent)">N/A</span></span>
            <span id="perc">0%</span>
        </div>
        <div class="progress-track"><div id="fill" class="progress-bar"></div></div>

        <div class="hash-vault">
            <span class="vault-label">SHA-256 Checksum</span>
            <span id="hVal" class="hash-string">Awaiting secure stream...</span>
            <button class="copy-trigger" onclick="copyToClipboard()" title="Copy to Clipboard">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            </button>
        </div>
        
        <center><button class="visual-toggle" onclick="document.body.classList.toggle('gray-mode')">Toggle Visual Mode</button></center>
    </div>

    <footer class="global-footer">
        Version 9.9.9 | Engineered by Nosrat Jahan | BSc in CSE | 2026
    </footer>

    <script>
        const inputSource = document.getElementById('passIn');
        
        // Instant Audit on Input
        inputSource.addEventListener('input', () => {
            const rawData = inputSource.value;
            if(!rawData) {
                clearResults();
                return;
            }

            fetch('/audit-stream', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({data: rawData})
            })
            .then(response => response.json())
            .then(res => {
                document.getElementById('stat').innerText = res.metric;
                document.getElementById('perc').innerText = res.percent + "%";
                document.getElementById('hVal').innerText = res.hash;
                document.getElementById('fill').style.width = res.percent + "%";
            });
        });

        function clearResults() {
            document.getElementById('stat').innerText = "N/A";
            document.getElementById('perc').innerText = "0%";
            document.getElementById('hVal').innerText = "Awaiting secure stream...";
            document.getElementById('fill').style.width = "0%";
        }

        function copyToClipboard() {
            const hashText = document.getElementById('hVal').innerText;
            if(hashText.includes('Awaiting')) return;
            navigator.clipboard.writeText(hashText);
            alert("Security checksum copied to clipboard.");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(UI_TEMPLATE)

@app.route("/audit-stream", methods=['POST'])
def process_audit():
    request_data = request.get_json()
    input_str = request_data.get('data', '')
    metric, percent = perform_security_audit(input_str)
    hash_obj = hashlib.sha256(input_str.encode()).hexdigest()
    return jsonify({"metric": metric, "percent": percent, "hash": hash_obj})

if __name__ == "__main__":
    host_url = "http://127.0.0.1:8080"
    print(f"\\n[!] DEPLOYING CYBER-VAULT v9.9.9")
    print(f"[!] MODULE ACCESSIBLE AT: {host_url}\\n")
    webbrowser.open(host_url)
    app.run(port=8080, debug=False)
