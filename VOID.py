import os, sys, subprocess, platform, json, socket, webbrowser, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==============================================================================
# 🌑 VOID v18.0: GLOBAL EDITION
# Stability: 100% (Scope Fixed, Thread Safe)
# Feature: Auto-Install, Auto-Browser, One-Click, Self-Healing
# ==============================================================================

PORT = 8080
ROOT = os.path.dirname(os.path.abspath(__file__))

# [Control Panel]
# 0 = Safe Mode (CPU), 999 = Max Power (GPU)
MOBILE_MAX_LAYERS = 450 
PC_MAX_LAYERS = 999

class VoidBootloader:
    def __init__(self):
        self.is_mobile = 'android' in os.environ.get('PREFIX', '') or 'termux' in str(os.environ)
        self.models_dir = os.path.join(ROOT, 'models')
        
        # Adjust path for Mobile (Termux)
        if self.is_mobile:
            self.models_dir = os.path.join(os.environ.get('HOME', '.'), 'models')

    def log(self, msg):
        print(f" [VOID] {msg}")

    def ignite(self):
        """[Auto-Fix] System Diagnostic & Self-Repair"""
        os.system('cls' if os.name=='nt' else 'clear')
        self.log("System Check Initiated...")
        
        # 1. Auto-Install Engine on Android
        if self.is_mobile:
            try:
                subprocess.run(['llama-cli', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                self.log("Engine Missing. Installing 'llama-cpp'...")
                os.system("pkg install -y llama-cpp")
                self.log("Engine Installed.")

        # 2. Create Directory Structure
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir, exist_ok=True)
            self.log(f"Created Storage: {self.models_dir}")

        # 3. Secure Resources
        driver = self._get_driver()
        model = self._get_model()
        
        return driver, model

    def _get_driver(self):
        # Mobile uses system package
        if self.is_mobile: return "llama-cli"
        
        # PC scans the 'drivers' folder
        d_dir = os.path.join(ROOT, 'drivers')
        bin_name = "llama-cli.exe" if os.name == 'nt' else "llama-cli"
        if sys.platform == 'darwin': bin_name = "llama-cli-mac"
        elif sys.platform == 'linux': bin_name = "llama-cli-linux"
        
        driver_path = os.path.join(d_dir, bin_name)
        
        # Grant Execution Permissions (Mac/Linux)
        if os.name != 'nt' and os.path.exists(driver_path):
            try: os.chmod(driver_path, 0o755)
            except: pass
            
        return driver_path

    def _get_model(self):
        try:
            # Select the first .gguf file found
            f = [x for x in os.listdir(self.models_dir) if x.endswith('.gguf')][0]
            return os.path.join(self.models_dir, f)
        except: return None

# [Execute Bootloader] - Initialize Global Resources
boot = VoidBootloader()
GLOBAL_DRIVER, GLOBAL_MODEL = boot.ignite()

class VoidEngine:
    def infer(self, prompt):
        if not GLOBAL_MODEL: 
            return "[Error] No Model Found. Please put a .gguf file in the models folder."
        if not GLOBAL_DRIVER:
            return "[Error] Driver Binary Missing."

        layers = str(MOBILE_MAX_LAYERS if boot.is_mobile else PC_MAX_LAYERS)
        
        cmd = [
            GLOBAL_DRIVER, "-m", GLOBAL_MODEL,
            "-p", f"System: VOID.\nUser: {prompt}\nAssistant:",
            "-n", "512", "--log-disable", "-c", "2048",
            "-ngl", layers
        ]

        # PC Exclusive: Distributed Processing
        if not boot.is_mobile:
            cmd.extend(["-sm", "row"])
            if platform.system() == 'Linux': cmd.extend(["--numa", "dist"])

        try:
            kw = {'capture_output': True, 'text': True, 'encoding': 'utf-8', 'errors': 'replace'} if os.name=='nt' else {'capture_output': True, 'text': True}
            res = subprocess.run(cmd, **kw)
            raw = res.stdout
            if not raw: return "..."
            return raw.split("Assistant:")[-1].strip() if "Assistant:" in raw else raw.strip()
        except Exception as e: return f"[Crash] {e}"

engine = VoidEngine()

class AutoHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass # Suppress server logs

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_ui().encode('utf-8'))
        else: self.send_error(404)

    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            reply = engine.infer(data.get('prompt', ''))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': reply}).encode('utf-8'))
        except: self.send_error(500)

    def get_ui(self):
        # [UI] Integrated HTML/CSS/JS (Dark Mode)
        status = "Ready" if GLOBAL_MODEL else "NO MODEL"
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <title>VOID</title>
            <style>
                body {{ background-color: #000; color: #ccc; font-family: -apple-system, sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }}
                #header {{ padding: 15px; text-align: center; border-bottom: 1px solid #222; font-weight: bold; color: #fff; }}
                #chat {{ flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }}
                .msg {{ padding: 12px; border-radius: 15px; max-width: 85%; word-break: break-word; line-height: 1.5; }}
                .user {{ align_self: flex-end; background: #222; color: #fff; }}
                .ai {{ align_self: flex-start; border: 1px solid #333; color: #ccc; }}
                #inp-box {{ padding: 15px; border-top: 1px solid #222; display: flex; gap: 10px; }}
                input {{ flex: 1; background: #111; border: none; color: #fff; padding: 12px; border-radius: 20px; outline: none; }}
                button {{ background: #fff; color: #000; border: none; width: 45px; border-radius: 50%; font-weight: bold; }}
                .loading {{ opacity: 0.5; }}
            </style>
        </head>
        <body>
            <div id="header">VOID v18.0 // {status}</div>
            <div id="chat"><div class="msg ai">System Online.</div></div>
            <div id="inp-box">
                <input type="text" id="inp" placeholder="Command..." autocomplete="off">
                <button onclick="send()">^</button>
            </div>
            <script>
                const inp = document.getElementById('inp');
                const chat = document.getElementById('chat');
                inp.addEventListener('keypress', (e) => {{ if(e.key==='Enter') send(); }});
                
                async function send() {{
                    const t = inp.value.trim(); if(!t) return;
                    add(t, 'user'); inp.value='';
                    document.body.classList.add('loading');
                    try {{
                        const r = await fetch('/', {{method:'POST', body: JSON.stringify({{prompt:t}}) }});
                        const d = await r.json();
                        add(d.reply, 'ai');
                    }} catch(e) {{ add("Error", 'ai'); }}
                    document.body.classList.remove('loading');
                }}
                
                function add(t, c) {{
                    const d = document.createElement('div'); d.className='msg '+c; d.innerText=t;
                    chat.appendChild(d); chat.scrollTop=chat.scrollHeight;
                }}
            </script>
        </body>
        </html>
        """

def get_ip():
    try: s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.connect(("8.8.8.8",80));ip=s.getsockname()[0];s.close();return ip
    except: return "127.0.0.1"

def open_browser(url):
    """Wait for server boot, then launch browser"""
    time.sleep(1.5)
    if boot.is_mobile:
        try: os.system(f"termux-open-url {url}")
        except: pass
    else:
        try: webbrowser.open(url)
        except: pass

if __name__ == "__main__":
    ip = get_ip()
    url = f"http://{ip}:{PORT}"
    
    print(f" [VOID] Server Active at {url}")
    if not GLOBAL_MODEL:
        print(" [!] WARNING: No Model Found.")

    # Launch browser in separate thread (Non-blocking)
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    try: HTTPServer(('0.0.0.0', PORT), AutoHandler).serve_forever()
    except KeyboardInterrupt: pass
