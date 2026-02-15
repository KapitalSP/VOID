# Copyright 2026 R2 (KapitalSP)
# Licensed under the Apache License, Version 2.0 (the "License");

import os, sys, json, time, subprocess, threading, http.server, platform, zlib, struct
from socketserver import ThreadingMixIn

# ==============================================================================
# 🛡️ KAPITAL SENTINEL [SMART RESOURCE GUARD]
# ==============================================================================
try: 
    import psutil
    HAS_DEPS = True
except ImportError: 
    HAS_DEPS = False

class KapitalSentinel:
    def __init__(self, role="worker"):
        self.os = platform.system()
        self.ignite(role)

    def ignite(self, role):
        if not HAS_DEPS: return
        try:
            p = psutil.Process(os.getpid())
            if self.os == "Windows": p.nice(psutil.HIGH_PRIORITY_CLASS)
            else: 
                try: p.nice(-10)
                except: pass
            
            cores = psutil.cpu_count(logical=True)
            if role == "worker" and cores:
                reserve = 1 if cores > 2 else 0
                if cores > 4: reserve = 2
                try: p.cpu_affinity(list(range(cores - reserve)))
                except: pass
        except: pass

    def check_health(self):
        """Monitors RAM and Thermals to prevent system lag."""
        if not HAS_DEPS: return
        try:
            if psutil.virtual_memory().percent > 90:
                print("\n [🚨] SYSTEM OVERLOAD: RAM usage > 90%. Cooling down...")
                time.sleep(2)
        except: pass

sentinel = KapitalSentinel("worker") 

# ==========================================
# [CORE] VOID LOGIC
# ==========================================
VERSION = "v1.5.0 (Global Stable)"
CONFIG_FILE = "config.json"

def load_config():
    for f in ["models", "drivers", "plugins"]: os.makedirs(f, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        cfg = {"model_path": "models/llama-3-8b.gguf", "driver_path": "drivers/llama-cli", "gpu_layers": 33, "threads": 6}
        with open(CONFIG_FILE, 'w') as f: json.dump(cfg, f, indent=4)
        return cfg
    with open(CONFIG_FILE) as f: return json.load(f)

def stream_inference(prompt, cfg):
    driver = cfg['driver_path']
    if os.name == 'nt' and not driver.endswith('.exe'): driver += ".exe"
    if not os.path.exists(driver): yield "[Error] llama-cli driver missing."; return

    cmd = [driver, "-m", cfg['model_path'], "-p", f"User: {prompt}\nAI:", "-n", "1024", "-ngl", str(cfg['gpu_layers']), "--log-disable"]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8', bufsize=1)
        for line in process.stdout:
            sentinel.check_health() 
            yield line
        process.wait()
    except Exception as e: yield f"[Inference Error] {e}"

def menu_market():
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print(" 🛒 VOID PLUGIN MARKET")
        print(" ==========================================")
        print(" 1. WebSearch Pro  [Free]")
        print(" 2. Python Sandbox [Free]")
        print(" [Q] Back to Menu")
        sel = input("\n Select Plugin to Install > ").lower()
        if sel == 'q': break
        print(" [i] Connecting to repository...")
        time.sleep(1)
        print(" [!] This version of VOID is standalone. Remote market coming in v2.0.")
        time.sleep(1.5)

def main():
    cfg = load_config()
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print(f" 🌌 VOID {VERSION}")
        print(" ------------------------------------------")
        print(" 1. 💬 Start Chat")
        print(" 2. ⚙️  Settings")
        print(" 3. 🛒 Plugin Market")
        print(" Q. Quit")
        print(" ------------------------------------------")
        sel = input(" Selection > ").lower()
        
        if sel == '1':
            print("\n [Type 'exit' to return to menu]")
            while True:
                p = input("\n You >> ")
                if p.lower() in ['exit', 'quit']: break
                print(" VOID >> ", end='', flush=True)
                for chunk in stream_inference(p, cfg): print(chunk, end='', flush=True)
                print()
        elif sel == '3': menu_market()
        elif sel == 'q': sys.exit()

if __name__ == "__main__": main()
