#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import signal

# ==========================================
# [PART 1] THE VESSEL (Storage & Resource Management)
# ==========================================
class VoidContainer:
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.inventory = {"models": [], "drivers": []}
        self.socket = {"engine": None, "driver": None}

    def materialize(self):
        """[OS Independent] Create structure and scan for matter."""
        print(f" [System] OS: {platform.system()} | Arch: {platform.machine()}")
        
        for category in self.inventory:
            path = os.path.join(self.root, category)
            os.makedirs(path, exist_ok=True)
            # Scan & Sort (Deterministic loading)
            files = [
                f for f in os.listdir(path) 
                if not f.startswith(".") and os.path.isfile(os.path.join(path, f))
            ]
            self.inventory[category] = sorted(files) # Sort alphabetically

    def mount(self, category, index=0):
        """[Hot-Swap] Plug component into the socket."""
        if not self.inventory[category]:
            return False
        
        filename = self.inventory[category][index]
        full_path = os.path.join(self.root, category, filename)
        
        # [Safety Patch 1] Auto-grant execution permissions on Linux/Mac
        if category == "drivers" and platform.system() != "Windows":
            try:
                os.chmod(full_path, 0o755)
                print(f" [Security] Permission granted for: {filename}")
            except Exception:
                pass # Ignore if fails, let the OS handle it

        key = "engine" if category == "models" else "driver"
        self.socket[key] = full_path
        return filename

# ==========================================
# [PART 2] THE FLUX (Execution & Data Stream)
# ==========================================
class VoidStream:
    def __init__(self, vessel_ref):
        self.vessel = vessel_ref

    def flow(self, prompt):
        """[Subprocess] Standard I/O Bridge with Zombie Protection"""
        driver = self.vessel.socket["driver"]
        engine = self.vessel.socket["engine"]

        if not driver or not engine:
            yield " [!] Void is empty. Please fill /models and /drivers."
            return

        # Common arguments for llama.cpp compatible binaries
        cmd = [driver, "-m", engine, "-p", prompt, "-n", "512", "--log-disable"]

        process = None
        try:
            # Execute Process
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                encoding='utf-8', 
                errors='replace'
            )
            
            # Real-time Streaming
            for line in process.stdout:
                yield line
                
        except PermissionError:
            yield " [!] Error: Permission Denied. Check driver file permissions."
        except FileNotFoundError:
            yield " [!] Error: Driver file disappeared."
        except Exception as e:
            yield f" [Error] Entropy Break: {e}"
        finally:
            # [Safety Patch 2] Kill the zombie process if loop breaks (Ctrl+C)
            if process and process.poll() is None:
                process.terminate()
                process.wait()

# ==========================================
# [PART 3] MAIN INTERFACE (User Entry Point)
# ==========================================
def main():
    # Handle Ctrl+C cleanly at system level
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    print("\n [ P R O J E C T   V O I D ]")
    print(" The Architecture of Emptiness.\n")
    
    # 1. Materialize
    void = VoidContainer()
    void.materialize()

    # 2. Auto-Mount
    if void.mount("models", 0):
        print(f" [+] Engine Mounted: {os.path.basename(void.socket['engine'])}")
    else:
        print(f" [!] Empty: No engine found in /models")

    if void.mount("drivers", 0):
        print(f" [+] Driver Mounted: {os.path.basename(void.socket['driver'])}")
    else:
        print(f" [!] Empty: No driver found in /drivers")

    # 3. Open Stream
    stream = VoidStream(void)
    print("\n Type 'exit' to disconnect.\n")

    while True:
        try:
            user_input = input(" VOID > ").strip()
            if not user_input: continue
            if user_input.lower() in ['exit', 'quit']: break
            
            print("") 
            for fragment in stream.flow(user_input):
                print(fragment, end="", flush=True)
            print("\n")

        except KeyboardInterrupt:
            print("\n [!] Disconnected.")
            break

if __name__ == "__main__":
    main()

