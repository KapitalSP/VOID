VOID

VOID is a chassis for running AI engines — not an engine itself.

VOID provides a minimal, transparent structure for running local GGUF models or switching to remote APIs using a single, consistent interface. It is designed to stay out of the way and expose control rather than hide it.

What is VOID?

VOID is a zero-friction execution chassis for AI inference.

It does not train models, does not modify inference logic, and does not attempt to optimize performance by itself. Instead, it focuses on:

Detecting available engines automatically

Providing a stable execution structure

Allowing local and remote inference to coexist

Avoiding heavy abstractions and hidden behavior

Think of VOID as the frame that holds the engine — not the engine.

Why VOID Exists

Most AI tooling today assumes one of two extremes:

Beginner-friendly tools that hide all internals

Large frameworks that require deep integration

VOID exists for users who want neither.

It is built for people who:

Understand what an engine is

Want direct control over execution

Prefer simple, inspectable code

Intend to build their own systems on top

VOID does not try to be convenient for everyone. It tries to be honest for the right users.

Who Is This For?

VOID is not designed for AI beginners.

This project assumes you already:

Know what GGUF models are

Understand local inference vs API-based inference

Are comfortable configuring engines and models manually

If you can already assemble your own AI stack, VOID gives you a clean base to do it faster and more transparently.

What VOID Is NOT

VOID is not:

an AI model

an inference engine

a performance optimizer

a replacement for llama.cpp or hosted APIs

VOID does not improve model quality. VOID does not magically speed things up.

If something is slow in VOID, it would be slow elsewhere too.

Performance Notes

VOID itself does not optimize inference speed or model performance.

All performance characteristics depend on:

the selected engine (e.g. llama.cpp or a remote API)

the chosen model architecture and size

the underlying hardware

VOID’s role is to:

expose engine parameters clearly

avoid hidden abstraction layers

allow direct performance control

VOID does not promise performance. It promises transparency.

Core Features

Local GGUF inference via llama.cpp

Remote API mode (OpenAI-compatible)

Runtime switching between local and remote modes

Minimal dependency footprint

Simple HTTP API for integration

Mobile-friendly (Termux / Android)

Architecture Overview

Engine layer: external (llama.cpp, API providers)

Model layer: user-supplied (GGUF or remote)

VOID layer: execution chassis and interface

VOID intentionally avoids merging these layers.

Basic Usage

Place a GGUF model in the models/ directory

Place the engine binary in drivers/ or ensure it is in PATH

Run the server

Access the UI or call the HTTP API

Remote mode can be enabled by updating the configuration.

Design Philosophy

Simple code over clever code

Explicit control over automation

No silent behavior

No unnecessary abstractions

VOID is meant to be modified. If you want to change it, you probably should.

Final Notes

VOID is a chassis.

Engines evolve. Models change. Hardware improves.

VOID stays still — so the rest can move freely.
Place .gguf model files in /models

Place llama-cli binary in /drivers

Run VOID

Use local inference immediately

Remote Mode

Set your API key

Switch mode via /config

Use standard API-based inference

The interface stays the same.
Only the engine changes.

Design Philosophy

Engines evolve
→ The chassis must remain stable.

Personal computing upper bound ≈ 100B
→ Designed to be practical for individuals, not data centers.

Loose but scalable
→ Stable by default, modifiable for those who want to push limits.

VOID is intentionally relaxed in structure —
so others can “overbuild” it if they want.

BASIC vs VOID

BASIC

Server-grade

Large-scale

Heavy and rigid

Not publicly released

VOID

Personal / local-first

Hybrid execution

Lightweight and open

Built to be shared

VOID is a derivative of BASIC,
refactored into a usable public chassis.

Market & Community

VOID is not meant to stay isolated.

The long-term idea is:

shared presets

plugins

configurations

markets built around the chassis

Even if VOID itself doesn’t make money,
ecosystems always do.

Quick Start
git clone https://github.com/KapitalSP/VOID
cd VOID
python void.py


One Sentence Summary

VOID is not an AI.
It’s the structure that lets you build one.

