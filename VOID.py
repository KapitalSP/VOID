"""
PROJECT VOID : The Zero-Dependency AI Chassis
Version: 1.0.0 (Official Release)
Author: R2 & Gemini
License: MIT License
"""

import os
import sys
import json
import time
import subprocess
import threading
import urllib.request
import http.server
from socketserver import ThreadingMixIn

# ==========================================
# [CORE] CONFIGURATION & CONSTANTS
# ==========================================
VERSION = "v1.0.0 (Official)"
CONFIG_FILE = "config.json"

# Default Configuration
DEFAULT_CONFIG = {
    "api_key": "sk-placeholder",
    "model_path": "models/llama-3-8b.gguf",
    "driver_path": "drivers/llama-cli",   # Path to local inference engine
    "gpu_layers": 33,                     # -ngl (GPU offload)
    "ctx_size": 4096,                     # -c (Context window)
    "threads": 8,                         # -t (CPU threads)
    "mode": "hybrid",                     # 'local' or 'api'
    "system_prompt": "You are VOID, an advanced AI chassis."
}

# Global State
config = {}
server_status = "Stopped"

# ==========================================
# [MODULE 1] SYSTEM UTILS & BOOTSTRAP
# ==========================================
def cls():
    """Clear console screen cross-platform."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config():
    """Load config.json or create it with defaults."""
    global config
    
    # Auto-Bootstrap: Create necessary directories
    for folder in ["models", "drivers", "plugins", "logs"]:
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(CONFIG_FILE):
        config = DEFAULT_CONFIG.copy()
        save_config()
    else:
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            print("[System] Config file corrupted. Resetting.")
            config = DEFAULT_CONFIG.copy()
            save_config()

def save_config():
    """Save current memory state to config.json."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

# ==========================================
# [MODULE 2] INFERENCE ENGINE (Streaming)
# ==========================================
def stream_inference(prompt):
    """
    Generator function that yields output token by token.
    Crucial for large models (100B+) to avoid timeouts.
    """
    if config['mode'] == 'local':
        # [LOCAL MODE] - Subprocess Streaming
        driver = config['driver_path']
        
        # Check if driver exists (auto-append .exe for Windows)
        if os.name == 'nt' and not driver.endswith('.exe'):
            driver += ".exe"
            
        if not os.path.exists(driver):
            yield f"[Error] Driver not found: {driver}\nPlease put 'llama-cli' in drivers/ folder."
            return

        # Command for llama.cpp (compatible with most GGUF runners)
        cmd = [
            driver,
            "-m", config['model_path'],
            "-p", f"{config['system_prompt']} User: {prompt} Assistant:",
            "-n", "1024",
            "-ngl", str(config['gpu_layers']),
            "-c", str(config['ctx_size']),
            "-t", str(config['threads']),
            "--temp", "0.7"
        ]
        
        try:
            # Start process with piped stdout
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, # Hide system logs
                text=True,
                encoding='utf-8',
                bufsize=1
            )
            
            # Read output character by character/line
            for line in process.stdout:
                yield line
                
            process.wait()
            
        except Exception as e:
            yield f"[Local Inference Error] {e}"

    else:
        # [API MODE] - Simulation
        response = f"[API Mode] Echo: {prompt}"
        for char in response:
            time.sleep(0.05) # Simulate typing
            yield char

# ==========================================
# [MODULE 3] API SERVER (Background Daemon)
# ==========================================
class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class VoidHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Silence server logs

    def do_POST(self):
        # OpenAI Compatible Endpoint
        if self.path == '/v1/chat/completions':
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len).decode('utf-8')
            data = json.loads(post_body)
            
            user_msg = "Hello"
            if "messages" in data:
                user_msg = data["messages"][-1]["content"]

            # Collect full response for API (Non-streaming for HTTP simplicity in v1.0)
            full_response = ""
            for chunk in stream_inference(user_msg):
                full_response += chunk

            response = {
                "id": "chatcmpl-void-v1",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": config['model_path'],
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": full_response},
                    "finish_reason": "stop"
                }]
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404)

def start_server():
    global server_status
    try:
        server = ThreadedHTTPServer(('0.0.0.0', 8000), VoidHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        server_status = "Online (Port 8000)"
    except Exception as e:
        server_status = f"Failed: {e}"

# ==========================================
# [MODULE 4] TUI MENUS
# ==========================================
def menu_chat():
    cls()
    print(f"💬 VOID CHAT [{config['mode'].upper()}]")
    print("="*60)
    print("Type 'exit' to return. (Streaming Enabled)")
    
    while True:
        prompt = input("\nYou >> ")
        if prompt.lower() == 'exit': break
        
        print("VOID >> ", end='', flush=True)
        
        # Real-time Streaming Output
        full_text = ""
        for chunk in stream_inference(prompt):
            print(chunk, end='', flush=True)
            full_text += chunk
        print() # Newline at end

def menu_settings():
    while True:
        cls()
        print(f"⚙️  SETTINGS MANAGER")
        print("="*60)
        print(f"1. Model Path   : {config['model_path']}")
        print(f"2. Driver Path  : {config['driver_path']}")
        print(f"3. GPU Layers   : {config['gpu_layers']}")
        print(f"4. Threads      : {config['threads']}")
        print(f"5. Mode         : {config['mode']}")
        print("-" * 60)
        print("Select number to edit, or 'q' to return.")
        
        sel = input("\nSelect >> ").strip().lower()
        if sel == 'q': break

        if sel == '1': config['model_path'] = input("New Path >> ")
        elif sel == '2': config['driver_path'] = input("New Driver Path >> ")
        elif sel == '3': config['gpu_layers'] = int(input("GPU Layers (int) >> "))
        elif sel == '4': config['threads'] = int(input("CPU Threads (int) >> "))
        elif sel == '5': config['mode'] = input("Mode (local/api) >> ")
        
        save_config()

def menu_market():
    # In v1.0, this is a placeholder for the decentralized plugin system
    plugins = [
        {"name": "WebSearch", "desc": "Live Internet Access", "file": "search.py"},
        {"name": "CodeInterpreter", "desc": "Python Execution Box", "file": "sandbox.py"},
    ]
    
    while True:
        cls()
        print(f"🛒 PLUGIN MARKET")
        print("="*60)
        for i, p in enumerate(plugins):
            status = "[INSTALLED]" if os.path.exists(f"plugins/{p['file']}") else "[ ]"
            print(f"{i+1}. {status} {p['name']} : {p['desc']}")
        
        print("\n[Q] Return to Main Menu")
        sel = input("Select >> ").strip().lower()
        if sel == 'q': break
        
        print("\n[System] Connecting to repository...")
        time.sleep(1)
        print("[System] Download feature will be enabled in v1.1 update.")
        time.sleep(1)

# ==========================================
# [MAIN] ENTRY POINT
# ==========================================
def main():
    load_config()
    start_server()
    
    while True:
        cls()
        print(f"""
██    ██  ██████  ██  ██████  
██    ██ ██    ██ ██  ██   ██ 
██    ██ ██    ██ ██  ██   ██ 
 ██  ██  ██    ██ ██  ██   ██ 
  ████    ██████  ██  ██████  {VERSION}

[ Server: {server_status} ] [ Mode: {config['mode'].upper()} ]
============================================================
1. 💬 Chat (Streaming)
2. ⚙️  Settings
3. 🛒 Plugin Market
4. 🔌 Server Logs
Q. Quit
============================================================
""")
        choice = input("Menu >> ").strip().lower()
        
        if choice == '1': menu_chat()
        elif choice == '2': menu_settings()
        elif choice == '3': menu_market()
        elif choice == '4': input("\nServer is running quietly. Press Enter to return.")
        elif choice == 'q':
            print("Shutting down system...")
            sys.exit(0)

if __name__ == "__main__":
    main()
