## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

> **"Free to use, Free to modify. Just keep the credit."**

VOID: The Universal AI Chassis
"VOID is not an AI.
It’s the structure that lets you build one."

VOID is a zero-dependency, single-file execution chassis for AI inference.

It is designed to provide a minimal, transparent structure for running local GGUF models or switching to remote APIs using a consistent interface. VOID stays still — so the rest can move freely.

🚀 Quick Start
VOID is a single-file application that automatically bootstraps its own environment.
# 1. Get the chassis
git clone https://github.com/KapitalSP/VOID
cd VOID

# 2. Ignite (No pip install required)
python void.py

💻 Cross-Platform Compatibility
VOID is written in Pure Python Standard Library, making it inherently OS-agnostic.
The chassis automatically detects the host environment and adapts its logic accordingly.
OS,     VOID Behavior,                                     User Responsibility
Windows,"Auto-detects .exe extensions, handles \ paths.",Drop llama-cli.exe in drivers/
Linux / macOS, "Uses standard POSIX paths, compatible with Shell.",Drop llama-cli binary in drivers/
Android (Termux),Runs natively on mobile Python. Zero overhead.,Drop arm64 binary in drivers/
The Code stays the same. You only need to provide the correct binary for your OS.

What is VOID?
VOID is a zero-friction execution chassis for AI inference.

It does not train models, does not modify inference logic, and does not attempt to optimize performance by itself. Instead, it focuses on:

Detecting available engines automatically.

Providing a stable execution structure via a simple TUI and API.

Allowing local and remote inference to coexist.

Avoiding heavy abstractions and hidden behavior.

Think of VOID as the frame that holds the engine — not the engine.

Why VOID Exists
Most AI tooling today assumes one of two extremes:

Beginner-friendly tools that hide all internals.

Large frameworks that require deep integration.

VOID exists for users who want neither. It is built for people who:

Understand what an engine is.

Want direct control over execution.

Prefer simple, inspectable code (100% Python).

Intend to build their own systems on top.

VOID does not try to be convenient for everyone. It tries to be honest for the right users.

Core Features
Single-File Architecture: Just void.py. No complex installation.

Local GGUF inference: Via llama.cpp or compatible binaries.

Remote API mode: OpenAI-compatible endpoint support.

Runtime Switching: Hot-swap between Local and Remote modes via TUI.

Simple HTTP API: Background server for external integration.

Architecture Overview
Engine layer: External binaries (llama.cpp, API providers).

Model layer: User-supplied files (GGUF or remote keys).

VOID layer: Execution chassis and interface.

VOID intentionally avoids merging these layers.

Design Philosophy
Simple code over clever code.

Explicit control over automation.

No silent behavior.

No unnecessary abstractions.

Engines evolve. Models change. Hardware improves.
VOID stays still — so the rest can move freely.

Performance Notes
VOID itself does not optimize inference speed.
If something is slow in VOID, it would be slow elsewhere too.

All performance characteristics depend on:

The selected engine (e.g., llama-cli).

The chosen model architecture and size.

The underlying hardware.

VOID’s role is to expose engine parameters clearly (e.g., GPU Layers, Threads) and avoid hidden abstraction layers.
VOID does not promise performance. It promises transparency.

📜 BASIC vs. VOID
VOID is built upon the architecture of BASIC.
It inherits the core stability of BASIC but is re-engineered for personal use.
Feature,BASIC (The Foundation),VOID (The Adaptation)
Role,Server Infrastructure,Personal Chassis
Architecture,Multi-process / Cluster-ready,Single-process / Local-first
UX,Raw & Headless Automation,Interactive TUI / Hybrid
Status,Industrial / Heavy,Consumer / Lightweight

"VOID is BASIC, stripped down to fit on your desk."

Market & Community
VOID is not meant to stay isolated. The structure is intentionally relaxed so others can "overbuild" it.

The long-term idea is:

Shared presets (config.json).

Plugins (via the built-in Market menu).

Configurations for specific hardware.

Even if VOID itself doesn’t make money, ecosystems always do.

One Sentence Summary
VOID is not an AI.
It’s the structure that lets you build one.

