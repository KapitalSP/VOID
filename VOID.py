# Copyright (c) 2026 KapitalSP
# Licensed under the Apache License, Version 2.0
#
# VOID: The Universal AI Chassis (v1.6.0 - Master Edition)
# Features: Thread-Safe Memory, Residual Logging, Pre-flight Sweep, Matrix UI

import os
import sys
import io
import time
import platform
import threading
import glob

# ==========================================
# 🛡️ [PATCH] Prevent Windows Encoding Crash
# ==========================================
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ==========================================
# 🧹 [PATCH] Pre-flight Sweep (Cleanup)
# ==========================================
def pre_flight_sweep():
    """Clears out orphaned temp files left from power outages or hard crashes."""
    temp_files = glob.glob(".temp_p_*.txt")
    for f in temp_files:
        try: os.remove(f)
        except: pass

pre_flight_sweep()

# 1. Engine Transplant (BASIC Engine)
try:
    from basic_engine import BasicEngine
except ImportError:
    print("\n[CRITICAL ERROR] basic_engine.py not found in the current directory.")
    sys.exit(1)

# 2. Resource Guard (Kapital Sentinel)
try: 
    import psutil
    HAS_DEPS = True
except ImportError: 
    HAS_DEPS = False

class KapitalSentinel:
    """Smart Resource Guard: CPU Affinity & Health Monitoring"""
    def __init__(self, role="worker"):
        self.os = platform.system()
        self.ignite(role)

    def ignite(self, role):
        if not HAS_DEPS: return
        try:
            p = psutil.Process(os.getpid())
            if self.os == "Windows": 
                p.nice(psutil.HIGH_PRIORITY_CLASS)
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
        """Monitors RAM to prevent system freeze during inference."""
        if not HAS_DEPS: return
        try:
            if psutil.virtual_memory().percent > 90:
                print("\033[91m\n [🚨 SYSTEM OVERLOAD] RAM usage > 90%. Cooling down...\033[0m", end="")
                time.sleep(2)
        except: pass

# ==========================================
# 🧠 [CORE] Hybrid Memory Module (VoidMemory)
# ==========================================
class VoidMemory:
    """Thread-Safe, Overflow-Proof Hybrid Memory Module"""
    def __init__(self, system_prompt, max_context_chars=1500, log_dir="logs"):
        # Secure pathing and automatic folder creation
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"void_blackbox_{int(time.time())}.log")
        
        self.system_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>"
        self.short_term = []
        # Tightly set to 1500 characters to prevent token inflation
        self.max_chars = max_context_chars 
        self.current_chars = 0
        self.memory_lock = threading.Lock()

    def add_residual(self, role, text):
        formatted_turn = f"<|start_header_id|>{role}<|end_header_id|>\n\n{text}<|eot_id|>"
        turn_length = len(formatted_turn)

        with self.memory_lock:
            self.short_term.append(formatted_turn)
            self.current_chars += turn_length
            
            while self.current_chars > self.max_chars and len(self.short_term) > 1:
                removed_turn = self.short_term.pop(0)
                self.current_chars -= len(removed_turn)

            try:
                # Append residual data at O(1) speed (Zero Bottleneck)
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{role.upper()}]: {text}\n")
            except Exception:
                pass

    def build_prompt(self):
        with self.memory_lock:
            history = "".join(self.short_term)
            return f"{self.system_prompt}\n{history}\n<|start_header_id|>assistant<|end_header_id|>\n\n"

# ==========================================
# 💻 [UI] Matrix CLI Renderer
# ==========================================
VERSION = "v1.6.0 (Master Edition)"
sentinel = KapitalSentinel("worker") 

C_GREEN = "\033[92m"
C_DIM = "\033[2m"
C_ALERT = "\033[91m"
C_RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def matrix_print(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def start_chat(engine):
    clear_screen()
    print(f"{C_GREEN}=========================================={C_RESET}")
    matrix_print(f"{C_GREEN} INITIALIZING NEURAL LINK WITH MEMORY... [OK]{C_RESET}", 0.02)
    print(f"{C_GREEN} TYPE 'exit' TO SEVER CONNECTION.{C_RESET}")
    print(f"{C_GREEN}=========================================={C_RESET}\n")
    
    system_prompt = "You are VOID, a highly efficient industrial AI assistant powered by KapitalSP."
    memory = VoidMemory(system_prompt=system_prompt)
    
    while True:
        try:
            user_input = input(f"{C_GREEN}[USER] >> {C_RESET}")
            if user_input.lower() in ['exit', 'quit']: 
                matrix_print(f"{C_DIM} Severing connection...{C_RESET}")
                time.sleep(0.5)
                break
            if not user_input.strip(): continue

            # 1. Record residual & Assemble context
            memory.add_residual("user", user_input)
            full_context = memory.build_prompt()

            print(f"{C_GREEN}[VOID] >> {C_RESET}", end='', flush=True)
            
            ai_response = ""
            
            # 2. Engine output & Real-time filtering
            for chunk in engine.generate(full_context):
                sentinel.check_health()
                
                # [PATCH] Clean UI Artifacts
                clean_chunk = chunk.replace("<|eot_id|>", "").replace("<|start_header_id|>", "")
                if clean_chunk:
                    sys.stdout.write(f"{C_GREEN}{clean_chunk}{C_RESET}")
                    sys.stdout.flush()
                    ai_response += clean_chunk
                    
            print("\n")
            
            # 3. Pass completed response to memory
            if ai_response.strip():
                memory.add_residual("assistant", ai_response.strip())
                
        except KeyboardInterrupt:
            # [PATCH] Graceful Defense against Panic Switch (Ctrl+C)
            print(f"{C_RESET}\n\n[!] Forced interrupt detected. Protecting runtime and severing connection.")
            time.sleep(1)
            break

def main():
    clear_screen()
    matrix_print(f"{C_GREEN} Waking up BASIC Engine...{C_RESET}", 0.03)
    engine = BasicEngine()
    
    while True:
        clear_screen()
        print(f"{C_GREEN}=========================================={C_RESET}")
        print(f"{C_GREEN} 🌌 VOID {VERSION}{C_RESET}")
        print(f"{C_GREEN}=========================================={C_RESET}")
        print(f"{C_GREEN} [1] 💬 ESTABLISH CONNECTION (CHAT){C_RESET}")
        print(f"{C_GREEN} [2] ⚙️  SYSTEM SETTINGS (LOCKED){C_RESET}")
        print(f"{C_GREEN} [3] 🛒 PLUGIN MARKET (LOCKED){C_RESET}")
        print(f"{C_GREEN} [Q] SYSTEM SHUTDOWN{C_RESET}")
        print(f"{C_GREEN}------------------------------------------{C_RESET}")
        
        sel = input(f"{C_GREEN} COMMAND >> {C_RESET}").lower()
        
        if sel == '1': start_chat(engine)
        elif sel == 'q':
            matrix_print(f"{C_GREEN} SYSTEM SHUTTING DOWN...{C_RESET}", 0.05)
            sys.exit()

if __name__ == "__main__":
    main()
