# 🚀 DevSetup CLI

> **One command to set up your entire developer environment on Windows.**

DevSetup automatically installs programming languages, editors, databases, and tools — so you don't have to do it manually one by one.

---

## 📦 Download & Install (EXE — Easiest Way)

The pre-built executable is located at:

```
dist\devsetup.exe      (7.5 MB)
```

### Step-by-step:

1. **Find the EXE** → It's in the `dist/` folder of this project
2. **Open a terminal** → Right-click on Desktop → "Open in Terminal" (or search for PowerShell)
3. **Navigate to the folder** and run:

```powershell
.\devsetup.exe --help
```

4. **That's it!** On first run, DevSetup copies itself to `C:\DevSetup\` and adds itself to your PATH
5. **Open a new terminal** and now you can just type:

```powershell
devsetup --help
```

> 💡 **No admin rights needed!** DevSetup only modifies your user PATH, not the system PATH.

---

## 🏁 Quick Start (For Beginners)

### "I want to start coding in Python"

```powershell
devsetup setup python
```

This installs **Python 3.12**, **VS Code**, and **Git** — everything you need to start!

### "I want Python + AI/ML libraries"

```powershell
devsetup setup python --pip ai_ml
```

### "I want to build websites (fullstack)"

```powershell
devsetup setup fullstack --pip web --npm fullstack
```

### "I'm brand new, just give me the essentials"

```powershell
devsetup setup starter
```

This installs Python, Node.js, Git, VS Code, Docker, PowerShell 7, and Windows Terminal.

### "I want to see what would happen without installing anything"

```powershell
devsetup setup python --dry-run
```

---

## 📋 All Commands

| Command | What it does |
|---------|-------------|
| `devsetup setup <stack>` | Install a full developer stack |
| `devsetup setup <stack> --pip <set>` | Also install Python libraries |
| `devsetup setup <stack> --npm <set>` | Also install Node.js packages |
| `devsetup setup <stack> --dry-run` | Preview what would be installed (nothing changes) |
| `devsetup list` | Show all available stacks |
| `devsetup explain <stack>` | Explain what a stack includes and when to use it |
| `devsetup list-reqs` | Show all available pip/npm library sets |
| `devsetup doctor` | Check if your tools are healthy and working |
| `devsetup doctor --check r` | Check a specific tool only |
| `devsetup doctor --fix-deps --yes` | Auto-fix problems (like missing PATH entries) |
| `devsetup add-path "C:\MyTool\bin"` | Manually add a folder to your PATH |
| `devsetup --version` | Show version |

---

## 🧰 Available Stacks (50 stacks)

### 🔤 Programming Languages

| Stack | Description | Tools Installed |
|-------|-------------|----------------|
| `python` | Python development environment | Python 3.12, VS Code, Git |
| `node` | Node.js development environment | Node.js, VS Code, Git |
| `deno` | Deno development environment | Deno, VS Code, Git |
| `bun` | Bun development environment | Bun, VS Code, Git |
| `java` | Java development environment | Java JDK 21, Maven, VS Code, Git |
| `go` | Go development environment | Go, VS Code, Git |
| `rust` | Rust development environment | Rust, VS Code, Git |
| `cpp` | C/C++ development environment | MinGW (C/C++), CMake, VS Code, Git |
| `zig` | Zig development environment | Zig, VS Code, Git |
| `dotnet` | .NET / C# development environment | .NET SDK 8, VS Code, Git |
| `ruby` | Ruby development environment | Ruby 3.2, VS Code, Git |
| `kotlin` | Kotlin development environment | Kotlin, Java JDK 21, Android Studio, Git |
| `scala` | Scala development environment | Scala (via sbt), Java JDK 21, VS Code, Git |
| `julia` | Julia development environment | Julia, VS Code, Git |
| `r` | R / statistics environment | R, VS Code, Git |
| `elixir` | Elixir development environment | Elixir, Erlang/OTP, VS Code, Git |
| `lua` | Lua development environment | Lua, VS Code, Git |
| `perl` | Perl development environment | Perl, VS Code, Git |
| `swift` | Swift development environment | Swift, VS Code, Git |
| `php_cli` | PHP (command line) | PHP, Composer, VS Code, Git |
| `php_web` | PHP (web with XAMPP) | XAMPP, VS Code, Git, Postman |

### 🌐 Web & App Development

| Stack | Description | Tools Installed |
|-------|-------------|----------------|
| `frontend` | Frontend / React / SPA | Node.js, VS Code, Git |
| `backend` | Backend API | Node.js, Python, Docker, PostgreSQL, Git, Postman, VS Code |
| `fullstack` | Frontend + Backend + Infra | Node.js, Python, Docker, PostgreSQL, Git, Postman, VS Code |
| `mobile` | Mobile app (Flutter) | Flutter, Android Studio, Git, VS Code |
| `android` | Android app | Android Studio, Java JDK 21, Git, VS Code |
| `desktop` | Desktop app (Electron / .NET) | Node.js, .NET SDK 8, VS Code, Git |
| `web3` | Blockchain / Web3 | Node.js, Python, Git, VS Code |
| `api_dev` | API design & testing | Node.js, Python, Postman, Docker, Git, VS Code |
| `scripting` | Quick scripts & automation | Python, Node.js, Git, VS Code |

### ☁️ Cloud & DevOps

| Stack | Description | Tools Installed |
|-------|-------------|----------------|
| `devops` | DevOps / CI-CD | Docker, Terraform, kubectl, Helm, Git, VS Code, Nginx |
| `cloud` | General cloud engineering | Python, Node.js, Docker, Terraform, AWS CLI, Git, VS Code |
| `cloud_aws` | AWS focused | Python, AWS CLI, Docker, Terraform, Git, VS Code |
| `cloud_azure` | Azure focused | Python, Azure CLI, Docker, Terraform, .NET SDK 8, Git, VS Code |
| `cloud_gcp` | Google Cloud focused | Python, Google Cloud CLI, Docker, Terraform, Git, VS Code |
| `k8s` | Kubernetes | Docker, kubectl, Helm, Minikube, Git, VS Code |
| `sre` | Site reliability | Docker, Terraform, Nginx, Python, Git, VS Code |

### 📊 Data & AI

| Stack | Description | Tools Installed |
|-------|-------------|----------------|
| `data_engineer` | Data pipelines | Python, PostgreSQL, Docker, DBeaver, Git, VS Code |
| `data_science` | Data analysis | Python, R, DBeaver, Git, VS Code |
| `ml_engineer` | Machine learning | Python, Docker, DBeaver, Git, VS Code |
| `nlp` | Natural language processing | Python, Git, VS Code |

### 🗄️ Database

| Stack | Description | Tools Installed |
|-------|-------------|----------------|
| `db` | Multi-database stack | DBeaver, PostgreSQL, MySQL, Redis, Docker, Git |
| `mongo` | MongoDB stack | MongoDB Shell, DBeaver, Docker, Git, VS Code |

### 🎮 Games & Specialty

| Stack | Description | Tools Installed |
|-------|-------------|----------------|
| `game_cpp` | C++ game development | MinGW (C/C++), CMake, VS Code, Git |
| `game_godot` | Godot game engine | Godot Engine, VS Code, Git |
| `security` | Security / penetration testing | Python, Git, Docker, VS Code |
| `embedded` | Embedded / IoT | Python, MinGW (C/C++), CMake, Git, VS Code |
| `java_full` | Java full stack | Java JDK 21, Maven, Gradle, PostgreSQL, DBeaver, Docker, Git, VS Code |

### ⭐ Convenience

| Stack | Description | Tools Installed |
|-------|-------------|----------------|
| `starter` | **Best for beginners** — essential tools | Python, Node.js, Git, VS Code, Docker, PowerShell 7, Windows Terminal |
| `automation` | Task automation | Python, Git, VS Code |

---

## 📚 Library / Package Sets

You can install Python or Node.js libraries alongside your stack using `--pip` and `--npm` flags.

### Python (`--pip`) — 22 sets

| Set | What's included |
|-----|----------------|
| `basic` | pandas, requests, numpy, pillow, pyautogui, python-dotenv, rich |
| `ai_ml` | numpy, pandas, scikit-learn, matplotlib, seaborn, jupyter, torch, transformers... |
| `llm` | openai, anthropic, langchain, chromadb, tiktoken, sentence-transformers, groq |
| `nlp` | spacy, nltk, textblob, gensim, transformers, wordcloud |
| `web` | flask, django, fastapi, uvicorn, sqlalchemy, alembic, pydantic, httpx |
| `api` | fastapi, uvicorn, httpx, requests, pydantic, authlib, passlib, bcrypt |
| `data` | pandas, numpy, matplotlib, seaborn, plotly, openpyxl, pyarrow, polars, scipy |
| `visualization` | matplotlib, seaborn, plotly, dash, bokeh, altair, streamlit, gradio |
| `db` | sqlalchemy, alembic, pymysql, psycopg2-binary, pymongo, redis |
| `scraping` | requests, beautifulsoup4, selenium, playwright, scrapy, lxml |
| `automation` | pyautogui, keyboard, schedule, watchdog, paramiko, fabric |
| `cli` | click, typer, rich, prompt-toolkit, tqdm, tabulate, questionary |
| `testing` | pytest, pytest-cov, pytest-asyncio, faker, hypothesis |
| `security` | cryptography, paramiko, bcrypt, pyjwt, certifi |
| `devops` | boto3, azure-identity, google-cloud-storage, docker |
| `cv` | opencv-python, pillow, scikit-image, torchvision, timm |
| `finance` | yfinance, pandas-ta, ccxt, alpaca-trade-api, quantlib |
| `bot` | discord.py, python-telegram-bot, slack-sdk, tweepy, praw |
| `geospatial` | geopandas, folium, shapely, rasterio, pyproj, leafmap |
| `async_tools` | aiohttp, aiofiles, celery, dramatiq, arq |
| `audio` | librosa, pydub, soundfile, speechrecognition, whisper |
| `game` | pygame, pyglet, arcade, panda3d, ursina, pymunk |

### Node.js (`--npm`) — 18 sets

| Set | What's included |
|-----|----------------|
| `basic` | lodash, axios, dotenv, chalk, uuid |
| `react` | react, react-dom, react-router-dom, @tanstack/react-query, zustand, tailwindcss |
| `vue` | vue, vue-router, pinia, @vueuse/core, vite, tailwindcss |
| `svelte` | svelte, @sveltejs/kit, tailwindcss, vite |
| `nextjs` | next, react, react-dom, next-auth, tailwindcss, typescript, zod |
| `express` | express, cors, helmet, morgan, dotenv, compression |
| `fullstack` | next, react, react-dom, prisma, @prisma/client, zod, tailwindcss, typescript |
| `api` | express, fastify, cors, helmet, jsonwebtoken, bcryptjs, zod |
| `graphql` | @apollo/server, graphql, @graphql-tools/schema, dataloader |
| `db` | prisma, @prisma/client, mongoose, sequelize, pg, mysql2, ioredis |
| `testing` | jest, vitest, @testing-library/react, supertest, playwright |
| `cli` | commander, inquirer, chalk, ora, boxen, figlet |
| `realtime` | socket.io, ws, socket.io-client, ioredis, bullmq |
| `desktop` | electron, electron-builder, @electron/remote |
| `auth` | next-auth, passport, jsonwebtoken, bcryptjs, jose |
| `web3` | ethers, hardhat, @openzeppelin/contracts, web3 |
| `ui` | @radix-ui/react-dialog, class-variance-authority, lucide-react, framer-motion |
| `monorepo` | turbo, tsup, typescript, eslint, prettier, changesets |

### Usage Examples

```powershell
# Python with AI/ML libraries
devsetup setup python --pip ai_ml

# Node.js with React packages (installed globally)
devsetup setup node --npm react

# Node.js with Vue packages (installed into a project folder)
devsetup setup node --npm vue --npm-scope project --project-dir "D:\my-app"

# Fullstack with both Python and Node libraries
devsetup setup fullstack --pip web --npm fullstack

# Data science with visualization libraries
devsetup setup data_science --pip visualization
```

---

## 🩺 Doctor (Health Checks)

The `doctor` command checks if your tools are installed correctly and working.

```powershell
# Check everything
devsetup doctor

# Check only R
devsetup doctor --check r

# Check Python and Git
devsetup doctor --check python git

# Auto-fix problems (like PATH issues)
devsetup doctor --fix-deps --yes

# Available checks: rust, python, node, git, cpp, r, path, all
```

### How doctor works:

- **Specialized checks** for Rust, Python, Node, Git, C++, R (deep checks with fix suggestions)
- **Generic checks** for all other tools (automatically checks any tool in your stack)
- **3-level results:**

| Icon | Level | Meaning |
|------|-------|---------|
| ✔ `PASS` | Everything is working | No action needed |
| ⚠ `WARN` | Installed but has issues | Usually a PATH issue — open a new terminal |
| ❌ `FAIL` | Not installed | Needs installation |

> 💡 Doctor runs automatically after every `devsetup setup` — it checks all tools in your stack.

---

## 🔧 How PATH Works

When you install a tool, DevSetup adds it to your **user PATH** so you can use it from any terminal.

**Important:**
- PATH changes take effect in a **new terminal window** (not the current one)
- DevSetup only modifies **your user PATH** (`HKEY_CURRENT_USER\Environment`)
- DevSetup **never** modifies system PATH — no admin/UAC required
- If you use Chocolatey, you can run `refreshenv` to apply PATH changes immediately

---

## 🔨 Building from Source

If you want to modify DevSetup or build the EXE yourself:

### Requirements

- Python 3.10 or newer
- pip (comes with Python)

### Run from source (no build needed)

```powershell
python devsetup.py setup python
python devsetup.py list
python devsetup.py doctor
```

### Build the EXE

```powershell
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller devsetup.spec --noconfirm --clean
```

The built EXE will be at: `dist\devsetup.exe`

### Verify source code

```powershell
python -m py_compile devsetup.py manager.py installer.py stacks.py pathutil.py colours.py doctor.py logger.py
```

---

## 📁 Project Structure

```
devsetup_source/
├── devsetup.py      # CLI entry point and self-installer
├── manager.py       # Orchestrates stack installs
├── installer.py     # Tool installer (winget) + library installer (pip/npm)
├── stacks.py        # All 50 stack definitions
├── doctor.py        # Health checks and auto-fix
├── pathutil.py      # Windows PATH management (registry)
├── colours.py       # Terminal color helpers
├── logger.py        # Logging (text + JSON)
├── devsetup.spec    # PyInstaller build config
├── dist/
│   └── devsetup.exe # Pre-built executable (7.5 MB)
└── README.md        # This file
```

---

## 📝 Log Files

DevSetup writes logs to help troubleshoot issues:

- **Text log:** `%APPDATA%\DevSetup\devsetup-log.txt`
- **JSON log:** `%APPDATA%\DevSetup\devsetup-log.jsonl`

---

## ❓ FAQ

**Q: Do I need admin rights?**
No. DevSetup only modifies your user PATH, not the system PATH.

**Q: Why does a tool say "not found" after installing?**
Open a **new terminal window**. PATH changes only take effect in new sessions.

**Q: How do I update a tool?**
Just run `devsetup setup <stack>` again. If the tool is already installed, it will be skipped.

**Q: What is winget?**
Winget is Microsoft's built-in package manager for Windows 10/11. It comes pre-installed on recent Windows versions. If you don't have it, install "App Installer" from the Microsoft Store.

**Q: Can I use this on Linux/Mac?**
No, DevSetup is Windows-only (it uses winget and Windows registry for PATH).

---

Made with ❤️ for developers who don't want to waste time on setup.
