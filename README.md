<div align="center">

```
+--------------------------------------------+
|              DevSetup  v1                |
|   Windows Developer Environment Manager   |
+--------------------------------------------+
```

# DevSetup

### Your dev environment. Set up once. Never again.

Stop Googling installers. Stop fighting broken PATH at 2AM.
DevSetup installs your full stack — languages, editors, libraries — in one command, on any fresh Windows machine.

```powershell
devset setup python --pip ai_ml
```

```
  [>]  Stack   :  PYTHON
  [>]  About   :  Python development environment
  [>]  Tools   :  Python 3.12, VS Code, Git
  [>]  pip     :  ai_ml
  -----------------------------------------------
  [1/3] Python 3.12
  [OK]  Python 3.12 already installed
  [OK]  Verified Python 3.12 (Python 3.12.4)
  [2/3] VS Code
  [OK]  VS Code already installed
  [OK]  Verified VS Code (1.89.1)
  [3/3] Git
  [OK]  Git already installed
  [OK]  Verified Git (git version 2.45.1)
  [>]  pip install [ai_ml]  (13 packages)
  [OK]  Python libraries installed
  [>]  Doctor check: Python toolchain
  [OK]  Python launcher found
  [OK]  pip is available
  -----------------------------------------------
  [OK]  Setup completed for PYTHON.
```

[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-0078D4?style=flat-square&logo=windows)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Version](https://img.shields.io/badge/version-3.2-brightgreen?style=flat-square)](https://github.com)
[![Stacks](https://img.shields.io/badge/stacks-50-orange?style=flat-square)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](LICENSE)
[![Issues](https://img.shields.io/github/issues/YOUR_USERNAME/devsetup?style=flat-square)](https://github.com/YOUR_USERNAME/devsetup/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/YOUR_USERNAME/devsetup/pulls)

> ⭐ If this saved you time, consider starring the repo — it helps others find it.

</div>

---

## The Problem

Setting up a Windows dev environment in 2024 still looks like this:

1. Google "how to install Python on Windows"
2. Download installer. Run it. Click through wizard. Forget to check "Add to PATH".
3. Open terminal. `python` not found.
4. Google the PATH fix. Apply it. Restart terminal.
5. Repeat steps 1–4 for Node, Git, VS Code, Docker...
6. Two hours later — you haven't written a single line of code.

DevSetup replaces all of that with one command.

---

## Why DevSetup?

| Feature | DevSetup | Manual | Chocolatey | Scoop |
|---------|:--------:|:------:|:----------:|:-----:|
| One-command full stack | ✅ | ❌ | ❌ | ❌ |
| pip + npm libraries bundled | ✅ | ❌ | ❌ | ❌ |
| Auto PATH management | ✅ | ❌ | ❌ | ⚠️ |
| Post-install health check | ✅ | ❌ | ❌ | ❌ |
| No admin rights needed | ✅ | ❌ | ❌ | ✅ |
| Dry-run / preview mode | ✅ | ❌ | ❌ | ❌ |
| 50 developer stacks | ✅ | ❌ | ⚠️ | ⚠️ |
| Beginner friendly | ✅ | ❌ | ⚠️ | ⚠️ |

Chocolatey and Scoop install individual packages. DevSetup installs **complete environments** — the right tools together, PATH configured, health verified, ready to code.

---

## Who Is This For?

- **Beginners** who don't know where to start and just want things to work
- **Students** juggling multiple stacks (Python today, Node tomorrow, Rust next week)
- **Developers** on a fresh machine who want everything back in minutes
- **Anyone** who has ever spent an afternoon fighting an installer

---

## Real-World Performance

Tested on a fresh Windows 11 machine (stable internet, NVMe SSD):

| Stack | Time | Includes |
|-------|------|----------|
| `python` | ~2m 40s | Python 3.12, VS Code, Git + doctor check |
| `node` | ~3m 10s | Node.js, VS Code, Git + doctor check |
| `go` | ~2m 50s | Go, VS Code, Git + doctor check |
| `cpp` (MinGW) | ~4m 30s | MinGW, CMake, VS Code, Git — linker included |
| `rust` | ~25–40m | Rust + Visual Studio Build Tools (~3–5 GB) |
| `fullstack` | ~18–25m | Node, Python, Docker, PostgreSQL, Postman |
| `starter` | ~12–15m | Python, Node, Git, VS Code, Docker, Windows Terminal |

All times include verification and doctor checks. Rust is slow because it needs the external MSVC linker — see [Setup Time Guide](#-setup-time-guide) for details.

---

## Install

No Python required — the EXE is standalone.

```powershell
# Step 1 — run it once from wherever you downloaded it
.\dist\devsetup.exe --help

# Step 2 — on first run, it installs itself automatically
#   [OK]  DevSetup installed -> C:\DevSetup\devset.exe
#   [OK]  PATH <- C:\DevSetup
#   [!]   Restart terminal to apply PATH changes

# Step 3 — open a new terminal, use from anywhere
devset --help
```

> Installs to `C:\DevSetup\` and adds itself to your **user** PATH — no UAC, no admin rights.
> Falls back to `%APPDATA%\DevSetup\` if `C:\` is restricted.

---

## Quick Start

```powershell
# Python + VS Code + Git
devset setup python

# Python + AI/ML libraries (numpy, pandas, torch, transformers, jupyter...)
devset setup python --pip ai_ml

# Full-stack web dev (Node + Python + Docker + PostgreSQL)
devset setup fullstack --pip web --npm fullstack

# Best starter kit for beginners
devset setup starter

# See what would happen — without installing anything
devset setup rust --dry-run
```

---

## Doctor — Your Toolchain Health Check

This is DevSetup's most powerful feature. After every install, it automatically verifies each tool, checks PATH, and flags issues with suggested fixes.

```powershell
devset doctor
```

```
  [>]  Doctor check: Python toolchain
  [OK]  Python launcher found: C:\Python312\python.exe
  [OK]  pip is available (pip 24.0)

  [>]  Doctor check: Git toolchain
  [OK]  git version 2.45.1.windows.1

  [>]  Doctor check: Rust toolchain
  [OK]  rustc found at C:\Users\user\.cargo\bin\rustc.exe
  [!]  MSVC linker (link.exe) not found — native Rust builds may fail
  [?]  Install Visual Studio Build Tools now? [Y/n]:

  [>]  Doctor check: PATH integrity
  [OK]  User PATH has no duplicate entries

  Doctor summary: 6 ok, 1 warning, 0 failures
```

Run manually anytime:

```powershell
devset doctor                      # check everything
devset doctor --check python git   # check specific tools
devset doctor --fix-deps --yes     # auto-fix without prompting
```

| Result | Meaning |
|--------|---------|
| `[OK]` | Tool installed and verified |
| `[!]`  | Installed but has issues — usually PATH, open a new terminal |
| `[X]`  | Not installed |

---

## All Commands

| Command | Description |
|---------|-------------|
| `devset setup <stack>` | Install a full developer stack |
| `devset setup <stack> --pip <set>` | Also install Python libraries |
| `devset setup <stack> --npm <set>` | Also install Node.js packages |
| `devset setup <stack> --npm-scope project --project-dir <dir>` | Install npm packages into a project |
| `devset setup <stack> --dry-run` | Preview — no changes applied |
| `devset setup <stack> --no-doctor` | Skip post-install health check |
| `devset setup <stack> --fix-deps --yes` | Auto-fix issues without prompts |
| `devset list` | Show all 50 stacks |
| `devset explain <stack>` | Stack details + recommended packages |
| `devset list-reqs` | Show all pip/npm library sets |
| `devset doctor` | Full toolchain health check |
| `devset doctor --check python git rust` | Check specific tools |
| `devset doctor --fix-deps --yes` | Auto-fix all detected problems |
| `devset add-path "C:\MyTool\bin"` | Add a folder to user PATH permanently |
| `devset --version` | Show version |

---

## Available Stacks

Run `devset list` to see all 50 stacks. Here are the most commonly used:

### ⏱ Setup Time Guide

| Speed | Stacks | Why |
|-------|--------|-----|
| 🟢 **Fast** (< 5 min) | `python`, `node`, `go`, `bun`, `deno`, `lua`, `zig`, `cpp`, `game_cpp` | Small or self-contained downloads |
| 🟡 **Medium** (5–15 min) | `dotnet`, `ruby`, `r`, `julia`, `elixir`, `perl`, `php_cli`, `java`, `scala` | Medium runtimes or companion tools (sbt, Erlang/OTP, Composer) |
| 🔴 **Slow** (15–45 min) | `rust`, `kotlin` | See notes below |
| ⚫ **Very Slow** (45+ min) | `fullstack`, `cloud`, `k8s`, `devops`, `android`, `mobile` | Multiple large tools — Docker, Android Studio, Terraform, Flutter |

> **C++ is fast.** MinGW ships `gcc`, `g++`, and `ld` (linker) as one self-contained package. No separate build tools needed.
>
> **Rust is slow on Windows.** `rustc` compiles Rust, but the Windows MSVC target requires an **external** linker (`link.exe`) from Visual Studio Build Tools — a ~3–5 GB download separate from Rust itself. DevSetup's doctor detects the missing linker and offers to install it. Budget 20–40 minutes on first setup. This is a Windows-specific issue; Rust on Linux/Mac doesn't have it.
>
> **Key difference:** C++ (MinGW) = self-contained toolchain. Rust (MSVC) = depends on external toolchain.

---

### Popular Stacks

| Stack | Tools | Time |
|-------|-------|------|
| `python` | Python 3.12, VS Code, Git | 🟢 ~3 min |
| `node` | Node.js, VS Code, Git | 🟢 ~3 min |
| `go` | Go, VS Code, Git | 🟢 ~4 min |
| `cpp` | MinGW (GCC/G++/ld), CMake, VS Code, Git | 🟢 ~5 min |
| `rust` | Rust + MSVC Build Tools, VS Code, Git | 🔴 ~20–40 min |
| `java` | Java JDK 21, Maven, VS Code, Git | 🟡 ~10 min |
| `dotnet` | .NET SDK 8, VS Code, Git | 🟡 ~8 min |
| `r` | R, VS Code, Git | 🟡 ~7 min |
| `elixir` | Elixir, Erlang/OTP, VS Code, Git | 🟡 ~12 min |
| `fullstack` | Node.js, Python, Docker, PostgreSQL, Postman, VS Code | ⚫ ~18–25 min |
| `starter` | Python, Node.js, Git, VS Code, Docker, PowerShell 7, Windows Terminal | ⚫ ~12–15 min |
| `data_science` | Python, R, DBeaver, Git, VS Code | 🟡 ~12 min |
| `ml_engineer` | Python, Docker, DBeaver, Git, VS Code | 🟡 ~15 min |
| `game_cpp` | MinGW (C/C++), CMake, VS Code, Git | 🟢 ~5 min |
| `security` | Python, Docker, Git, VS Code | 🟡 ~12 min |

Other available stacks: `bun`, `deno`, `zig`, `lua`, `perl`, `swift`, `kotlin`, `scala`, `julia`, `ruby`, `php_cli`, `php_web`, `frontend`, `backend`, `mobile`, `android`, `desktop`, `web3`, `api_dev`, `scripting`, `devops`, `cloud`, `cloud_aws`, `cloud_azure`, `cloud_gcp`, `k8s`, `sre`, `data_engineer`, `nlp`, `embedded`, `game_godot`, `java_full`, `db`, `mongo`, `automation`.

Run `devset explain <stack>` for tools, use-case, and recommended packages for any stack.

---

## Library / Package Sets

Install Python or Node libraries alongside any stack.

### Python (`--pip`) — 22 sets

| Set | Key packages |
|-----|-------------|
| `basic` | pandas, requests, numpy, pillow, pyautogui, python-dotenv, rich |
| `ai_ml` | numpy, pandas, scikit-learn, torch, torchvision, transformers, datasets, jupyter, tqdm |
| `llm` | openai, anthropic, langchain, langchain-community, chromadb, faiss-cpu, groq, sentence-transformers |
| `web` | flask, django, fastapi, uvicorn, sqlalchemy, alembic, pydantic, httpx, gunicorn |
| `data` | pandas, numpy, matplotlib, seaborn, plotly, polars, dask, scipy, pyarrow |
| `scraping` | requests, beautifulsoup4, selenium, playwright, scrapy, lxml, httpx |
| `automation` | pyautogui, keyboard, schedule, watchdog, paramiko, fabric |
| `api` | fastapi, uvicorn, httpx, pydantic, authlib, passlib, bcrypt |
| `testing` | pytest, pytest-cov, pytest-asyncio, faker, hypothesis |
| `cli` | click, typer, rich, prompt-toolkit, tqdm, tabulate |
| `cv` | opencv-python, pillow, scikit-image, albumentations, torchvision, timm |
| `nlp` | spacy, nltk, textblob, gensim, transformers, datasets, wordcloud |
| `finance` | yfinance, pandas-ta, ccxt, alpaca-trade-api, quantlib |
| `game` | pygame, pyglet, arcade, panda3d, ursina, pymunk |
| `bot` | discord.py, python-telegram-bot, slack-sdk, tweepy, praw |
| `security` | cryptography, paramiko, bcrypt, pyjwt, certifi |
| `db` | sqlalchemy, alembic, pymysql, psycopg2-binary, pymongo, redis, motor |
| `visualization` | matplotlib, seaborn, plotly, dash, bokeh, streamlit, gradio |
| `devops` | boto3, azure-identity, google-cloud-storage, docker |
| `geospatial` | geopandas, folium, shapely, rasterio, pyproj |
| `async_tools` | aiohttp, aiofiles, celery, dramatiq, arq, aiomysql |
| `audio` | librosa, pydub, soundfile, speechrecognition, whisper, torchaudio |

### Node.js (`--npm`) — 18 sets

| Set | Key packages |
|-----|-------------|
| `basic` | lodash, axios, dotenv, chalk, uuid |
| `react` | react, react-dom, react-router-dom, @tanstack/react-query, zustand, tailwindcss |
| `vue` | vue, vue-router, pinia, @vueuse/core, vite, tailwindcss |
| `svelte` | svelte, @sveltejs/kit, tailwindcss, vite |
| `nextjs` | next, react, react-dom, next-auth, tailwindcss, typescript, zod |
| `express` | express, cors, helmet, morgan, dotenv, express-validator |
| `fullstack` | next, react, prisma, @prisma/client, zod, tailwindcss, typescript |
| `api` | express, fastify, cors, helmet, jsonwebtoken, bcryptjs, zod |
| `graphql` | @apollo/server, graphql, @graphql-tools/schema, dataloader |
| `db` | prisma, @prisma/client, mongoose, sequelize, pg, mysql2, ioredis |
| `testing` | jest, vitest, @testing-library/react, supertest, playwright |
| `cli` | commander, inquirer, chalk, ora, boxen, figlet |
| `realtime` | socket.io, ws, socket.io-client, ioredis, bullmq |
| `desktop` | electron, electron-builder, @electron/remote, electron-store |
| `auth` | next-auth, passport, jsonwebtoken, bcryptjs, jose |
| `web3` | ethers, hardhat, @nomicfoundation/hardhat-toolbox, web3, @openzeppelin/contracts |
| `ui` | @radix-ui/react-dialog, class-variance-authority, lucide-react, framer-motion |
| `monorepo` | turbo, tsup, typescript, eslint, prettier, changesets |

### Examples

```powershell
# Python + AI/ML stack
devset setup python --pip ai_ml

# Node + React (global install)
devset setup node --npm react

# Node + Vue (into a project folder)
devset setup node --npm vue --npm-scope project --project-dir "D:\my-app"

# Full-stack with both Python and Node libraries
devset setup fullstack --pip web --npm fullstack

# Data science with visualization
devset setup data_science --pip visualization
```

---

## How PATH Works

- Writes to `HKEY_CURRENT_USER\Environment` — **no admin rights needed**
- Changes take effect in a **new terminal window**
- DevSetup never touches the system PATH (`HKEY_LOCAL_MACHINE`)
- To manually add a directory: `devset add-path "C:\MyTool\bin"`
- Chocolatey users: `refreshenv` applies changes to the current session immediately

---

## Build from Source

```powershell
# Run directly — no build needed
python devsetup.py setup python
python devsetup.py list
python devsetup.py doctor

# Build the EXE
pip install pyinstaller
pyinstaller devsetup.spec --noconfirm --clean
# Output -> dist\devsetup.exe

# Verify source compiles cleanly
python -m py_compile devsetup.py manager.py installer.py stacks.py pathutil.py colours.py doctor.py logger.py
```

---

## Project Structure

```
devsetup/
├── devsetup.py       CLI entry point + self-installer
├── manager.py        Orchestrates stack installs, summaries, doctor routing
├── installer.py      Installer class (winget) + LibraryInstaller (pip/npm)
├── stacks.py         All 50 stack definitions + StackMeta
├── doctor.py         Health checks (specialized + generic) + auto-fix
├── pathutil.py       Windows PATH management via registry (no admin)
├── colours.py        ANSI color helpers, terminal output functions
├── logger.py         Dual logging — text (.txt) + structured JSONL
├── devsetup.spec     PyInstaller build config
└── dist/
    └── devsetup.exe  Pre-built standalone executable (~7.5 MB)
```

Each module has a clear, single responsibility. `stacks.py` is the easiest starting point — adding a new stack requires no changes to any other file.

---

## Logs

All activity logged to `%APPDATA%\DevSetup\`:

| File | Format | Use |
|------|--------|-----|
| `devsetup-log.txt` | Human-readable with timestamps | Manual troubleshooting |
| `devsetup-log.jsonl` | Structured JSON lines with `run_id` | Parsing, automation, debugging |

Every log line includes a `run_id` so you can trace exactly which session produced each event.

---

## Contributing

Contributions are welcome — the codebase is intentionally modular so you can contribute to one piece without needing to understand everything.

**Getting started:**

```powershell
git clone https://github.com/YOUR_USERNAME/devsetup
cd devsetup
python devsetup.py list   # verify it runs
```

**Where to contribute:**

| File | What you can do |
|------|----------------|
| `stacks.py` | Add a new stack — no other files need to change |
| `doctor.py` | Improve or add health checks for a tool |
| `installer.py` | Improve install logic, error handling, recovery |
| `pathutil.py` | Improve PATH resolution for edge cases |
| Docs | Improve README, add examples, fix typos |

**Steps:**

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-change`
3. Make your change
4. Test it: `python devsetup.py setup <stack> --dry-run`
5. Submit a pull request

---

## Roadmap

- [ ] Linux support (apt/snap backend)
- [ ] macOS support (brew backend)
- [ ] Parallel tool installs for faster setup
- [ ] GUI version for non-terminal users
- [ ] `devset update` — upgrade all installed tools in a stack
- [ ] `.devsetup.json` config file per project
- [ ] Plugin system for custom stacks
- [ ] One-line install via PowerShell (e.g. `irm https://devsetup.sh | iex`)

---

## FAQ

**Do I need admin rights?**
No. DevSetup only writes to `HKEY_CURRENT_USER\Environment`. The EXE installs to `C:\DevSetup\` with a fallback to `%APPDATA%\DevSetup\` if that's restricted.

**Why does a tool say "not found" after installing?**
Open a new terminal. PATH changes only apply to new sessions. Chocolatey users can run `refreshenv`.

**Why is Rust slow but C++ fast?**
C++ (MinGW) ships with its own linker (`ld`) — fully self-contained. Rust on Windows depends on the external MSVC linker from Visual Studio Build Tools, which is a ~3–5 GB separate download.

**How do I update a tool?**
Run `devset setup <stack>` again. Already-installed tools are skipped unless you need to force reinstall.

**What is winget?**
Microsoft's built-in package manager for Windows 10/11, pre-installed on modern Windows. If missing, install "App Installer" from the Microsoft Store.

**Can I use this on Linux/Mac?**
Not yet — it's on the roadmap.

**What if an install fails?**
DevSetup stops, logs the failure, and tells you which tool failed. Run `devset doctor --fix-deps` to attempt auto-fix, or check `devsetup-log.txt` for the full error.

---
## Problem: installed but not detected
stack installed but not found in PATH
But installed at: C:\Program Files\xxxxx
## Cause:
stack is installed successfully but PATH not updated
## Solution:
`devset doctor --check <stack>`
or
`devset setup <stack> --fix-deps`


<div align="center">

Built for developers tired of fixing PATH at 2AM.

</div>
