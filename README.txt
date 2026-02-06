# Project VOID

> **The Architecture of Emptiness.**
> A minimalistic, OS-agnostic chassis for Local AI.

## Philosophy
* **Zero Dependencies:** No `pip install`. No libraries. Pure Python.
* **Universal Socket:** Works with any binary driver (llama.cpp, etc.) and GGUF models.
* **Anti-Fragile:** Separated architecture (Vessel & Flux).

## usage

1.  **Materialize**
    * Run `void.py`. It will automatically create `/models` and `/drivers` folders.

2.  **Fill the Void**
    * Drop your **Model file** (.gguf) into `/models`.
    * Drop your **Driver executable** (llama-cli.exe or binary) into `/drivers`.

3.  **Enter the Void**
    * Run `void.py` again.
    * Start chatting.

---
*Built for the builders.*