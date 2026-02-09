import os, sys, subprocess, platform, json, socket, time, threading, shutil, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==============================================================================
# 🌑 VOID v22.0 [HYBRID CHASSIS]
# Features: Local GGUF + Remote API Switcher, OpenAI Standard, Market Sync
# ==============================================================================

PORT = 8080
ROOT = os.path.dirname(os.path.abspath(__file__))
IS_MOBILE = 'android' in os.environ.get('PREFIX', '') or 'termux' in str(os.environ)

# [Configuration] - Can be modified via UI or config.json later
CONFIG = {
    "mode": "local", # Options: "local" or "remote"
    "api_key": "your-api-key-here",
    "api_url": "https://api.openai.com/v1/chat/completions",
    "model_name": "gpt-3.5-turbo" # Used for remote mode
}

class HybridCore:
    def __init__(self):
        self.init_folders()
        self.bin, self.model = self.scan()

    def init_folders(self):
        """Create folder structure (Auto-Bootstrap)"""
        for d in ['drivers', 'models', 'plugins']:
            os.makedirs(os.path.join(ROOT, d), exist_ok=True)

    def scan(self):
        # 1. Android (Termux) Auto-Setup
        if IS_MOBILE:
            try: subprocess.run(['llama-cli', '-v'], stdout=subprocess.DEVNULL)
            except: 
                print(" [VOID] Installing dependencies for Android...")
                os.system("pkg install -y llama-cpp")
            return "llama-cli", self._find_model()
        
        # 2. PC Engine Detection
        sys_os = platform.system()
        fname = "llama-cli.exe" if sys_os == 'Windows' else "llama-cli-mac" if sys_os == 'Darwin' else "llama-cli-linux"
        path = os.path.join(ROOT, 'drivers', fname)
        
        if os.path.exists(path):
            if sys_os != 'Windows': os.chmod(path, 0o755) # Grant execution permission
            return path, self._find_model()
            
        # Check System PATH
        if shutil.which("llama-cli"): 
            return "llama-cli", self._find_model()

        print(f"\n [!] ENGINE MISSING: Please place '{fname}' in /drivers")
        print(f" [!] Download from: https://github.com/ggerganov/llama.cpp/releases\n")
        return None, self._find_model()

    def _find_model(self):
        """Search for the first available .gguf file in /models"""
        m_path = os.path.join(ROOT, 'models')
        try: 
            return os.path.join(m_path, [f for f in os.listdir(m_path) if f.endswith('.gguf')][0])
        except: 
            return None

    def generate(self, prompt):
        # [Mode Switching Logic]
        if CONFIG["mode"] == "remote":
            return self._generate_remote(prompt)
        else:
            return self._generate_local(prompt)

    def _generate_local(self, prompt):
        if not self.bin or not self.model: 
            return "Error: Local Engine or Model file is missing."
        
        # Core command for llama-cli
        cmd = [self.bin, "-m", self.model, "-p", f"User: {prompt}\nAssistant:", "-n", "512", "--log-disable", "-ngl", "999"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            return res.stdout.split("Assistant:")[-1].strip()
        except Exception as e: 
            return f"Local Engine Error: {e}"

    def _generate_remote(self, prompt):
        data = json.dumps({
            "model": CONFIG["model_name"],
            "messages": [{"role": "user", "content": prompt}]
        }).encode()
        
        req = urllib.request.Request(CONFIG["api_url"], data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {CONFIG["api_key"]}')
        
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                res = json.loads(r.read().decode())
                return res['choices'][0]['message']['content']
        except Exception as e: 
            return f"Remote API Error: {e} (Please check your API Key or Network)"

core = HybridCore()

class VoidHandler(BaseHTTPRequestHandler):
    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(content_len).decode())

        if self.path == '/chat':
            reply = core.generate(body.get('prompt', ''))
            self._send_json({"reply": reply})
            
        elif self.path == '/config': # Configuration Update API
            CONFIG.update(body)
            self._send_json({"status": "updated", "current_mode": CONFIG["mode"]})
            
        else: 
            self.send_error(404)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_ui().encode())

    def get_ui(self):
        return f"""<!DOCTYPE html><html><head><title>VOID HYBRID</title><meta name="viewport" content="width=device-width,initial-scale=1">
        <style>
            body{{background:#000;color:#0f0;font-family:monospace;padding:20px;line-height:1.6}} 
            button{{background:#0f0;border:none;cursor:pointer;padding:8px 15px;margin:5px;font-weight:bold;transition:0.3s}}
            button:hover{{background:#fff}}
            #log{{border:1px solid #333;height:400px;overflow-y:auto;padding:15px;margin:15px 0;background:#050505}}
            input{{width:75%;background:#111;color:#0f0;border:1px solid #0f0;padding:12px;outline:none}}
        </style>
        </head><body>
        <h2>🌑 VOID HYBRID CHASSIS v22.0</h2>
        <div style="border:1px solid #333; padding:10px; display:inline-block">
            <strong>ENGINE MODE:</strong> 
            <button onclick="setMode('local')">LOCAL (GGUF)</button>
            <button onclick="setMode('remote')">REMOTE (API)</button>
        </div>
        <div id="log"></div>
        <div style="display:flex; gap:10px">
            <input id="i" onkeypress="if(event.key=='Enter')send()" placeholder="Type your command here...">
            <button onclick="send()" style="width:20%">SEND</button>
        </div>
        <script>
            async function setMode(m){{ 
                await fetch('/config', {{method:'POST', body:JSON.stringify({{mode:m}})}}); 
                alert('System Mode Switched to: ' + m.toUpperCase()); 
            }}
            async function send(){{
                const i=document.getElementById('i'), l=document.getElementById('log'), v=i.value.trim(); 
                if(!v)return;
                l.innerHTML += '<div style="color:#aaa">> '+v+'</div>'; 
                i.value='';
                l.scrollTop=l.scrollHeight;
                
                try {{
                    const r = await fetch('/chat', {{method:'POST', body:JSON.stringify({{prompt:v}})}});
                    const d = await r.json(); 
                    l.innerHTML += '<div style="margin-bottom:10px">AI: '+d.reply+'</div>';
                }} catch(e) {{
                    l.innerHTML += '<div style="color:red">ERROR: Connection Failed</div>';
                }}
                l.scrollTop=l.scrollHeight;
            }}
        </script></body></html>"""

if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    print(f" [🌑] VOID HYBRID ONLINE | http://{ip}:{PORT}")
    print(f" [⚙️] Mode: {CONFIG['mode'].upper()} | Standard OpenAI API Compatible")
    
    try:
        HTTPServer(('0.0.0.0', PORT), VoidHandler).serve_forever()
    except KeyboardInterrupt:
        print("\n [!] Shutting down VOID Chassis...")
