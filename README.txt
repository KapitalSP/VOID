VOID: The Hybrid AI Chassis (v22.0)
VOID is a lightweight, zero-dependency AI infrastructure designed to run anywhere—from high-end PCs to Android phones. It features a unique Hybrid Switching system that lets you toggle between local hardware and cloud intelligence with a single click.

✨ Key Features
Hybrid Engine: Seamlessly switch between Local GGUF (via llama.cpp) and Remote API (OpenAI compatible).

Zero Dependency: Runs on pure Python 3. No pip install required.

Auto-Bootstrap: Automatically generates /drivers, /models, and /plugins folders on first run.

Cross-Platform: Native support for Windows, Linux, macOS, and Android (Termux).

OpenAI Compatible: Acts as a standard API gateway for other AI tools and clients.

📂 Project Structure
Just run void.py, and the chassis will build itself:
VOID/
├── drivers/    <- Place llama-cli / llama-cli.exe here
├── models/     <- Place your .gguf model files here
├── plugins/    <- Place community-made .py plugins here
└── void.py     <- The core engine

🚀 Quick Start
1. Initial Setup
Run the script once to generate the directory structure.
python void.py

2. Fueling the Engine
For Local Mode: Download a .gguf model and place it in the /models folder.

For Remote Mode: Open void.py and enter your API Key in the CONFIG section.

3. Ignition
Run the script again and open the provided URL (default: http://localhost:8080) in your browser.
python void.py

🔧 ConfigurationYou can easily modify the behavior in the CONFIG object:KeyDescriptionDefaultmodeSwitch between local or remote"local"api_urlEndpoint for remote intelligenceOpenAI Standardmodel_nameModel ID for Remote API"gpt-3.5-turbo"

🏺 The Workshop (Market)
VOID is designed to be extensible. Our community-driven Market allows you to download specialized plugins to enhance your chassis.

Contribute: Submit a Pull Request to the central repository to share your own plugins.

Security: Every plugin in the market is reviewed by our global maintainer team.

🛡️ License
Distributed under the MIT License. See LICENSE for more information.

💡 Pro Tip for Developers
You can use VOID as a Headless API Server. Just point your favorite AI client (like Chatbox or TypingMind) to http://YOUR_IP:8080/v1 and enjoy the hybrid power without the UI.
