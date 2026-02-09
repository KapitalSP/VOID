VOID — Hybrid AI Chassis

VOID is not an AI model.
VOID is not an AI engine.

VOID is a chassis —
a structural runtime designed to mount, switch, and operate AI engines.

Why VOID Exists

The AI ecosystem is dominated by large engine providers.
They build powerful engines — but the surrounding structure is often:

closed

inflexible

tightly coupled to vendors

On the other hand, local AI offers:

full control

privacy

engine freedom

…but lacks a clean, reusable execution structure.

VOID exists to fill that gap.

A hybrid AI chassis that connects local GGUF models and remote APIs
under a single, minimal runtime.

Engines can change.
The chassis should not.

Who VOID Is For

VOID is not beginner-friendly by design.

This project assumes you already:

have run local LLMs before

understand CLI or API-based inference

are capable of assembling your own AI stack

If you’re at that level, VOID becomes a solid structural base
to build your own AI system on top of.

If not, VOID will feel difficult —
and that is intentional.

Core Features

Hybrid Mode

Switch between local GGUF inference and remote API inference

OpenAI-compatible API

/chat endpoint compatible with standard Chat Completion workflows

Local Engine Support

llama-cli + .gguf models

Minimal & Lightweight

Pure Python

No heavy dependencies

Easy to inspect, modify, extend

Usage Overview
Local Mode

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
