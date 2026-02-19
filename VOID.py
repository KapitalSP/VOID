# Copyright (c) 2026 KapitalSP
# Licensed under the Apache License, Version 2.0
#
# VOID: The Universal AI Chassis (v2.0 - Absolute Edition)
# Features: Zero-Defect Auto-Provisioning, Thread-Safe Memory, Sentinel Guard

import os
import sys
import io
import time
import platform
import threading
import glob
import urllib.request
import urllib.error
import hashlib
import socket

# ==========================================
# 🛡️ [PATCH 1] Global System Defense Configuration
# ==========================================
# Prevent Windows special character encoding crash
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Prevent infinite download freezing (15-second timeout)
socket.setdefaulttimeout(15.0)

# ==========================================
# 🧹 [PATCH 2] Pre-flight Sweep
# ==========================================
def pre_flight_sweep():
    """Wipes out orphaned temp files left by power outages or forced shutdowns."""
    temp_files = glob.glob(".temp_p_*.txt")
    for f in temp_files:
        try: os.remove(f)
        except: pass

pre_flight_sweep()

# ==========================================
# ⚙️ [CORE] Module Import & Sentinel Ignition
# ==========================================
try:
    from basic_engine import BasicEngine
except ImportError:
    print("\n[CRITICAL ERROR] basic_engine.py not found in the current directory.")
    sys.exit(1)

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
        if not HAS_DEPS: return
        try:
            if psutil.virtual_memory().percent > 90:
                print("\033[91m\n [🚨 SYSTEM OVERLOAD] RAM usage > 90%. Cooling down...\033[0m", end="")
                time.sleep(2)
        except: pass

# ==========================================
# 🚀 [FORGE] Zero-Defect Auto-Provisioning
# ==========================================
class KapitalForge:
    """Hardware Profiler & Safe Auto-Provisioning System"""
    def __init__(self, models_dir="models"):
        self.models_dir = os.path.abspath(models_dir)
        os.makedirs(self.models_dir, exist_ok=True)

    def check_disk_space(self, required_gb=6.0):
        if not HAS_DEPS: return True # Bypass if psutil is missing
        free_gb = psutil.disk_usage(self.models_dir).free / (1024**3)
        return free_gb > required_gb

    def _progress_hook(self, count, block_size, total_size):
        if total_size > 0:
            percent = min(int(count * block_size * 100 / total_size), 100)
            sys.stdout.write(f"\r \033[92m[⏬] Downloading Neural Weights... {percent}%\033[0m")
            sys.stdout.flush()

    def verify_checksum(self, file_path, expected_hash):
        print("\n \033[2m[🔍] Verifying neural weight integrity (SHA256)...\033[0m")
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Process in 4MB chunks to prevent RAM overflow
                for byte_block in iter(lambda: f.read(4096 * 1024), b""): 
                    sha256_hash.update(byte_block)
            
            calculated_hash = sha256_hash.hexdigest()
            if calculated_hash == expected_hash:
                print(" \033[92m[✅] Integrity Verified. Zero data corruption.\033[0m")
                return True
            else:
                print(f" \033[91m[❌ CRITICAL] Hash mismatch! Expected: {expected_hash[:8]}... Got: {calculated_hash[:8]}...\033[0m")
                return False
        except Exception as e:
            print(f" \033[91m[❌] Verification failed: {e}\033[0m")
            return False

    def auto_install(self):
        existing_models = [f for f in os.listdir(self.models_dir) if f.endswith(".gguf")]
        if existing_models:
            return True 

        print("\n \033[92m[🔍] Initiating System Scan for Model Provisioning...\033[0m")
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3) if HAS_DEPS else 8.0
        
        # ⚠️ [ACTION REQUIRED] Replace URL and expected_hash with your actual server deployment values.
        if total_ram_gb < 7.0:
            filename = "Llama-3-8B-Q3.gguf"
            url = "https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q3_K_M.gguf"
            expected_hash = "DUMMY_HASH_PLEASE_REPLACE_FOR_Q3"
        else:
            filename = "Llama-3-8B-Q4.gguf"
            url = "https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
            expected_hash = "DUMMY_HASH_PLEASE_REPLACE_FOR_Q4"

        print(f" \033[92m[OK] RAM: {total_ram_gb:.1f} GB. Selected: {filename}\033[0m")

        if not self.check_disk_space(required_gb=6.0):
            print(" \033[91m[❌ CRITICAL] Not enough disk space. Minimum 6GB required.\033[0m")
            return False

        file_path = os.path.join(self.models_dir, filename)
        try:
            urllib.request.urlretrieve(url, file_path, reporthook=self._progress_hook)
            
            # Post-download integrity check
            if expected_hash.startswith("DUMMY"):
                print("\n \033[93m[⚠️ WARNING] Dummy hash detected. Skipping integrity check. (Not Recommended)\033[0m")
                return True
            elif not self.verify_checksum(file_path, expected_hash):
                os.remove(file_path) # Ruthlessly delete corrupted data
                return False
                
            print("\n \033[92m[✅] Provisioning Complete. Engine is ready.\033[0m")
            return True
        except Exception as e:
            print(f"\n \033[91m[❌ CRITICAL] Download Failed: {e}\033[0m")
            if os.path.exists(file_path): os.remove(file_path)
            return False

# ==========================================
# 🧠 [MEMORY] Hybrid Memory Module
# ==========================================
class VoidMemory:
    def __init__(self, system_prompt, max_context_chars=1500, log_dir="logs"):
        if not os.path.exists(log_dir): os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"void_blackbox_{int(time.time())}.log")
        self.system_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>"
        self.short_term = []
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
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{role.upper()}]: {text}\n")
            except Exception: pass

    def build_prompt(self):
        with self.memory_lock:
            history = "".join(self.short_term)
            return f"{self.system_prompt}\n{history}\n<|start_header_id|>assistant<|end_header_id|>\n\n"

# ==========================================
# 💻 [UI] Matrix CLI Renderer
# ==========================================
VERSION = "v2.0 (Absolute Edition)"
sentinel = KapitalSentinel("worker") 

C_GREEN = "\033[92m"
C_DIM = "\033[2m"
C_ALERT = "\033[91m"
C_RESET = "\033[0m"

def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')

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

            memory.add_residual("user", user_input)
            full_context = memory.build_prompt()

            print(f"{C_GREEN}[VOID] >> {C_RESET}", end='', flush=True)
            ai_response = ""
            
            for chunk in engine.generate(full_context):
                sentinel.check_health()
                clean_chunk = chunk.replace("<|eot_id|>", "").replace("<|start_header_id|>", "")
                if clean_chunk:
                    sys.stdout.write(f"{C_GREEN}{clean_chunk}{C_RESET}")
                    sys.stdout.flush()
                    ai_response += clean_chunk
                    
            print("\n")
            if ai_response.strip():
                memory.add_residual("assistant", ai_response.strip())
                
        except KeyboardInterrupt:
            print(f"{C_RESET}\n\n[!] Forced interrupt detected. Protecting runtime and severing connection.")
            time.sleep(1)
            break

def main():
    clear_screen()
    matrix_print(f"{C_GREEN} Waking up Kapital Forge (Auto-Provisioning)...{C_RESET}", 0.03)
    
    # 🛡️ Initiate secure provisioning
    forge = KapitalForge()
    if not forge.auto_install():
        print(f"{C_ALERT}\n [CRITICAL ERROR] Provisioning failed. System halting.{C_RESET}")
        sys.exit(1)

    time.sleep(1)
    clear_screen()
    matrix_print(f"{C_GREEN} Igniting BASIC Engine...{C_RESET}", 0.03)
    engine = BasicEngine()
    
    while True:
        clear_screen()
        print(f"{C_GREEN}=========================================={C_RESET}")
        print(f"{C_GREEN} 🌌 VOID {VERSION}{C_RESET}")
        print(f"{C_GREEN}=========================================={C_RESET}")
        print(f"{C_GREEN} [1] 💬 ESTABLISH CONNECTION (CHAT){C_RESET}")
        print(f"{C_GREEN} [2] ⚙️  SYSTEM SETTINGS (LOCKED){C_RESET}")
        print(f"{C_GREEN} [Q] SYSTEM SHUTDOWN{C_RESET}")
        print(f"{C_GREEN}------------------------------------------{C_RESET}")
        
        sel = input(f"{C_GREEN} COMMAND >> {C_RESET}").lower()
        if sel == '1': start_chat(engine)
        elif sel == 'q':
            matrix_print(f"{C_GREEN} SYSTEM SHUTTING DOWN...{C_RESET}", 0.05)
            sys.exit()

if __name__ == "__main__":
    main()
