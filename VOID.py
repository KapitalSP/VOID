import os, sys, subprocess, platform, json, socket, webbrowser, time, threading, importlib.util
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==============================================================================
# 🌑 VOID v19.0: EXTENSIBLE
# Feature: Dynamic Plugin Loader (Hot-Swap)
# ==============================================================================

PORT = 8080
ROOT = os.path.dirname(os.path.abspath(__file__))
IS_MOBILE = 'android' in os.environ.get('PREFIX', '') or 'termux' in str(os.environ)
LAYERS = 999

class PluginManager:
    def __init__(self):
        self.pdir = os.path.join(ROOT, 'plugins')
        if not os.path.exists(self.pdir): os.makedirs(self.pdir, exist_ok=True)
        self.hooks = {'on_input': [], 'on_output': [], 'on_boot': []}
        self.load()

    def load(self):
        # Scan /plugins folder and import .py files dynamically
        print(" [VOID] Scanning Plugins...")
        for f in os.listdir(self.pdir):
            if f.endswith('.py') and not f.startswith('_'):
                try:
                    path = os.path.join(self.pdir, f)
                    spec = importlib.util.spec_from_file_location(f[:-3], path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    
                    # Register Hooks
                    if hasattr(mod, 'on_input'): self.hooks['on_input'].append(mod.on_input)
                    if hasattr(mod, 'on_output'): self.hooks['on_output'].append(mod.on_output)
                    if hasattr(mod, 'on_boot'): self.hooks['on_boot'].append(mod.on_boot)
                    print(f"  + Loaded: {f}")
                except Exception as e: print(f"  ! Error loading {f}: {e}")

    def run_hook(self, name, data):
        for func in self.hooks.get(name, []):
            try: data = func(data)
            except: pass
        return data

plugins = PluginManager()

class Core:
    def __init__(self):
        self.mdir = os.path.join(ROOT, 'models')
        if IS_MOBILE: self.mdir = os.path.join(os.environ.get('HOME','.'), 'models')
        self.init_env()
        self.bin, self.model = self.scan()
        plugins.run_hook('on_boot', None)

    def init_env(self):
        if IS_MOBILE:
            try: subprocess.run(['llama-cli','-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except: os.system("pkg install -y llama-cpp")
        if not os.path.exists(self.mdir): os.makedirs(self.mdir, exist_ok=True)

    def scan(self):
        if IS_MOBILE: drv = "llama-cli"
        else:
            sys_os = platform.system()
            b = "llama-cli.exe" if sys_os=='Windows' else "llama-cli-mac" if sys_os=='Darwin' else "llama-cli-linux"
            drv = os.path.join(ROOT, 'drivers', b)
            if sys_os!='Windows' and os.path.exists(drv): os.chmod(drv, 0o755)
        
        try: m = os.path.join(self.mdir, [f for f in os.listdir(self.mdir) if f.endswith('.gguf')][0])
        except: m = None
        return drv, m

    def run(self, prompt):
        if not self.model: return "Error: No Model."
        
        # [HOOK] Modify Prompt via Plugins
        prompt = plugins.run_hook('on_input', prompt)

        cmd = [self.bin, "-m", self.model, "-p", f"System: VOID.\nUser: {prompt}\nAssistant:", "-n", "512", "--log-disable", "-c", "2048", "-ngl", str(LAYERS)]
        if not IS_MOBILE: 
            cmd.extend(["-sm", "row"])
            if platform.system()=='Linux': cmd.extend(["--numa", "dist"])

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            output = res.stdout.split("Assistant:")[-1].strip() if "Assistant:" in res.stdout else res.stdout.strip()
            
            # [HOOK] Modify Output via Plugins
            output = plugins.run_hook('on_output', output)
            return output
        except Exception as e: return f"Crash: {e}"

core = Core()

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def do_GET(self):
        if self.path=='/':
            self.send_response(200); self.send_header('Content-type','text/html; charset=utf-8'); self.end_headers()
            self.wfile.write(self.html().encode('utf-8'))
        else: self.send_error(404)
    def do_POST(self):
        l = int(self.headers.get('Content-Length', 0))
        d = json.loads(self.rfile.read(l).decode())
        msg = core.run(d.get('prompt',''))
        self.send_response(200); self.send_header('Content-type','application/json'); self.end_headers()
        self.wfile.write(json.dumps({'reply':msg}).encode())
    def html(self):
        stat = "Active" if core.model else "NO MODEL"
        return f"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{background:#111;color:#ccc;font-family:monospace;margin:0;display:flex;flex-direction:column;height:100vh}}#h{{padding:15px;text-align:center;border-bottom:1px solid #333}}#c{{flex:1;overflow-y:auto;padding:20px}}#i{{display:flex;padding:10px;border-top:1px solid #333}}input{{flex:1;background:#222;border:none;color:#fff;padding:10px;outline:none}}</style></head><body><div id="h">VOID // {stat}</div><div id="c"></div><div id="i"><input id="t" autofocus onkeypress="if(event.key=='Enter')s()"><button onclick="s()">RUN</button></div><script>const t=document.getElementById('t'),c=document.getElementById('c');async function s(){{const v=t.value.trim();if(!v)return;a(v,'u');t.value='';try{{const r=await fetch('/',{{method:'POST',body:JSON.stringify({{prompt:v}})}});const d=await r.json();a(d.reply,'b')}}catch{{a('Err','b')}}}}function a(m,w){{const d=document.createElement('div');d.innerText=(w=='u'?'USER: ':'AI: ')+m;d.style.marginBottom='10px';c.appendChild(d);c.scrollTop=c.scrollHeight}}</script></body></html>"""

def get_ip():
    try: s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.connect(("1.1.1.1",1));return s.getsockname()[0]
    except: return "127.0.0.1"

if __name__ == "__main__":
    url = f"http://{get_ip()}:{PORT}"
    print(f" [VOID] System Ready: {url}")
    threading.Thread(target=lambda: (time.sleep(1), webbrowser.open(url) if not IS_MOBILE else os.system(f"termux-open-url {url}")), daemon=True).start()
    try: HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
    except: pass
