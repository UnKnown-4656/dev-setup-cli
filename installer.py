"""Tool and library installer classes."""
import shutil
import subprocess
import sys
from pathlib import Path

from colours import ok, fail, step, dim, warn
from logger import log_event, log_structured
from pathutil import ensure_paths_for


# ── 3-level result system ─────────────────────────────────────────────────────
# PASS  = tool installed and verified
# WARN  = tool installed but verification issues (PATH, version parse, etc.)
# FAIL  = actual installation failure

RESULT_PASS = "pass"
RESULT_WARN = "warn"
RESULT_FAIL = "fail"


class InstallError(RuntimeError):
    """Raised when an installation operation cannot be completed."""


class InstallResult:
    """Captures the outcome of an install/ensure operation with 3 levels."""

    def __init__(self, status: str, tool_name: str, message: str = ""):
        self.status = status      # RESULT_PASS | RESULT_WARN | RESULT_FAIL
        self.tool_name = tool_name
        self.message = message

    @property
    def is_fatal(self) -> bool:
        """Only true installation failures are fatal."""
        return self.status == RESULT_FAIL

    @property
    def is_ok(self) -> bool:
        return self.status in {RESULT_PASS, RESULT_WARN}

    def __repr__(self):
        icons = {RESULT_PASS: "✔", RESULT_WARN: "⚠", RESULT_FAIL: "❌"}
        return f"{icons.get(self.status, '?')} {self.tool_name}: {self.message}"


def _run_command(cmd: list[str], *, hint: str = "") -> bool:
    """Run a command and convert runtime errors into user-friendly output."""
    log_event(f"RUN {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        log_event(f"SUCCESS {' '.join(cmd)}")
        return True
    except FileNotFoundError:
        fail(f"Command not found: {cmd[0]}")
        log_event(f"FAILED command-not-found {' '.join(cmd)}")
        if hint:
            dim(f"  Hint: {hint}")
        return False
    except subprocess.CalledProcessError as exc:
        fail(f"Command failed (exit={exc.returncode}): {' '.join(cmd)}")
        log_event(f"FAILED exit={exc.returncode} {' '.join(cmd)}")
        if hint:
            dim(f"  Hint: {hint}")
        return False


class Installer:
    """Represents one installable tool (via winget)."""

    def __init__(self, name: str, check_cmd: str, winget_id: str, path_key: str = ""):
        self.name      = name
        self.check_cmd = check_cmd
        self.winget_id = winget_id
        self.path_key  = path_key
        self.last_status = "unknown"
        self.last_path_added: list[str] = []
        self.last_result: InstallResult | None = None

    def is_installed(self) -> bool:
        return shutil.which(self.check_cmd) is not None

    def _verify_tool(self, *, dry_run: bool = False) -> str:
        """Verify a tool is callable after install.

        Returns one of: RESULT_PASS, RESULT_WARN, RESULT_FAIL
        - PASS: tool found and version check succeeded
        - WARN: tool installed but version check couldn't be parsed (not fatal)
        - FAIL: tool not found in PATH at all
        """
        if dry_run:
            dim(f"  [dry-run] verify {self.check_cmd} --version")
            return RESULT_PASS

        checker = shutil.which(self.check_cmd)
        if not checker:
            # Tool is not in PATH — this is a WARN (not FAIL) because the
            # install may have succeeded but PATH hasn't been refreshed yet.
            warn(f"{self.name} was not found in PATH after installation")
            dim(f"  This is likely a PATH issue — open a new terminal or run: refreshenv")
            log_event(f"VERIFY_WARN {self.name} missing in PATH (probable PATH issue)")
            return RESULT_WARN

        # Try version commands — use lenient parsing (first line only)
        for args in ([self.check_cmd, "--version"], [self.check_cmd, "-v"], [self.check_cmd]):
            try:
                proc = subprocess.run(
                    args, check=True, capture_output=True, text=True, timeout=15
                )
                raw_output = (proc.stdout or proc.stderr or "").strip()
                # Only take the first line to avoid multi-line version outputs
                # (VS Code, R, etc. return multiple lines)
                version_line = raw_output.splitlines()[0] if raw_output else ""
                ok(f"Verified {self.name} ({version_line})")
                log_event(f"VERIFY_OK {self.name} via {' '.join(args)} -> {version_line}")
                return RESULT_PASS
            except subprocess.TimeoutExpired:
                log_event(f"VERIFY_TIMEOUT {self.name} via {' '.join(args)}")
                continue
            except Exception:
                continue

        # Command exists but all version checks failed — NOT fatal
        warn(f"{self.name} command exists but version check could not be parsed")
        dim(f"  The tool appears to be installed. Version output may be non-standard.")
        log_event(f"VERIFY_WARN {self.name} version-check-unparseable")
        return RESULT_WARN

    def _do_path_setup(self, *, dry_run: bool = False):
        """Handle PATH entries for this tool, with refresh awareness."""
        if not self.path_key:
            return
        if dry_run:
            dim(f"  [dry-run] would ensure PATH entries for {self.path_key}")
            return

        added = ensure_paths_for(self.path_key)
        self.last_path_added = added
        for a in added:
            dim(f"  PATH ← {a}")
        if added:
            # FIX 4: PATH refresh awareness
            print()
            warn("PATH updated successfully.")
            dim("  Open a new terminal or run:  refreshenv  (if using Chocolatey)")
            dim("  PATH changes require a new terminal session to take effect.")
            log_event(f"PATH_ADDED {self.name}: {';'.join(added)}")

    def install(self, *, dry_run: bool = False) -> InstallResult:
        step(f"Installing {self.name}")
        if dry_run:
            dim(f"  [dry-run] winget install -e --id {self.winget_id}")
            self.last_status = "planned_install"
            result = InstallResult(RESULT_PASS, self.name, "planned (dry-run)")
            self.last_result = result
            return result

        success = _run_command(
            [
                "winget", "install", "-e",
                "--id", self.winget_id,
                "--accept-package-agreements",
                "--accept-source-agreements",
                "--silent",
            ],
            hint=f"Try manually: winget install -e --id {self.winget_id}",
        )
        if not success:
            log_event(f"INSTALL_FAIL {self.name}")
            self.last_status = "failed"
            result = InstallResult(RESULT_FAIL, self.name, "winget install failed")
            self.last_result = result
            return result

        ok(f"{self.name} installed")
        log_event(f"INSTALL_OK {self.name}")
        self.last_status = "installed"

        self._do_path_setup()

        verify_status = self._verify_tool()
        if verify_status == RESULT_PASS:
            result = InstallResult(RESULT_PASS, self.name, "installed and verified")
        else:
            # Install succeeded but verification has issues — this is WARN, not FAIL
            result = InstallResult(RESULT_WARN, self.name, "installed but verification incomplete")
        self.last_result = result
        return result

    def ensure(self, *, dry_run: bool = False) -> InstallResult:
        if self.is_installed():
            ok(f"{self.name} already installed")
            log_event(f"ALREADY_INSTALLED {self.name}")
            self.last_status = "already_installed"
            self._do_path_setup(dry_run=dry_run)
            verify_status = self._verify_tool(dry_run=dry_run)
            if verify_status == RESULT_PASS:
                result = InstallResult(RESULT_PASS, self.name, "already installed and verified")
            else:
                result = InstallResult(RESULT_WARN, self.name, "already installed, verification issue")
            self.last_result = result
            return result
        else:
            return self.install(dry_run=dry_run)


def check_winget_available() -> bool:
    """Verify winget exists before running install workflows."""
    winget = shutil.which("winget")
    if winget:
        return True
    fail("winget is not available on this system.")
    warn("Install 'App Installer' from Microsoft Store, then retry.")
    dim("Manual fallback: https://aka.ms/getwinget")
    log_structured("preflight", check="winget", result="failed")
    return False


# ─────────────────────────────────────────────────────────────────────────────

class LibraryInstaller:

    PIP: dict[str, list[str]] = {
        "basic":      ["pandas", "requests", "numpy", "pillow", "pyautogui",
                       "python-dotenv", "rich"],
        "ai_ml":      ["numpy", "pandas", "scikit-learn", "matplotlib", "seaborn",
                       "jupyter", "torch", "torchvision", "transformers", "datasets",
                       "accelerate", "tokenizers", "tqdm"],
        "llm":        ["openai", "anthropic", "langchain", "langchain-community",
                       "chromadb", "faiss-cpu", "tiktoken",
                       "sentence-transformers", "groq"],
        "web":        ["flask", "django", "fastapi", "uvicorn", "jinja2",
                       "sqlalchemy", "alembic", "pydantic", "httpx", "aiohttp",
                       "gunicorn", "python-multipart"],
        "scraping":   ["requests", "beautifulsoup4", "selenium", "playwright",
                       "scrapy", "lxml", "httpx", "fake-useragent"],
        "data":       ["pandas", "numpy", "matplotlib", "seaborn", "plotly",
                       "openpyxl", "pyarrow", "dask", "polars", "scipy"],
        "automation": ["pyautogui", "keyboard", "schedule", "watchdog",
                       "paramiko", "fabric", "invoke"],
        "api":        ["fastapi", "uvicorn", "httpx", "requests", "pydantic",
                       "python-dotenv", "authlib", "python-jose", "passlib", "bcrypt"],
        "db":         ["sqlalchemy", "alembic", "pymysql", "psycopg2-binary",
                       "pymongo", "redis", "motor", "aiosqlite"],
        "cli":        ["click", "typer", "rich", "prompt-toolkit", "colorama",
                       "tqdm", "tabulate", "questionary"],
        "testing":    ["pytest", "pytest-cov", "pytest-asyncio", "faker",
                       "hypothesis", "responses", "freezegun"],
        "security":   ["cryptography", "paramiko", "bcrypt", "pyjwt", "certifi"],
        "devops":     ["boto3", "azure-identity", "google-cloud-storage",
                       "paramiko", "docker"],
        "cv":         ["opencv-python", "pillow", "scikit-image",
                       "albumentations", "torchvision", "timm"],
        "nlp":        ["spacy", "nltk", "textblob", "gensim",
                       "sentence-transformers", "transformers", "datasets",
                       "tokenizers", "wordcloud"],
        "finance":    ["yfinance", "pandas-ta", "ta", "ccxt", "alpaca-trade-api",
                       "quantlib", "pandas", "numpy", "matplotlib", "scipy"],
        "bot":        ["discord.py", "python-telegram-bot", "slack-sdk",
                       "tweepy", "praw", "aiohttp"],
        "visualization": ["matplotlib", "seaborn", "plotly", "dash", "bokeh",
                       "altair", "streamlit", "gradio"],
        "geospatial": ["geopandas", "folium", "shapely", "rasterio",
                       "pyproj", "leafmap", "geopy"],
        "async_tools":["aiohttp", "asyncio", "aiofiles", "aiomysql",
                       "aioredis", "celery", "dramatiq", "arq"],
        "audio":      ["librosa", "pydub", "soundfile", "pyaudio",
                       "speechrecognition", "whisper", "torchaudio"],
        "game":       ["pygame", "pyglet", "arcade", "panda3d",
                       "ursina", "pymunk"],
    }

    NPM: dict[str, list[str]] = {
        "basic":      ["lodash", "axios", "dotenv", "chalk", "uuid"],
        "react":      ["react", "react-dom", "react-router-dom", "axios",
                       "@tanstack/react-query", "zustand", "tailwindcss"],
        "vue":        ["vue", "vue-router", "pinia", "axios",
                       "@vueuse/core", "vite", "tailwindcss"],
        "svelte":     ["svelte", "@sveltejs/kit", "@sveltejs/adapter-auto",
                       "tailwindcss", "vite"],
        "nextjs":     ["next", "react", "react-dom", "@next/font",
                       "next-auth", "tailwindcss", "typescript", "zod"],
        "express":    ["express", "cors", "helmet", "morgan", "dotenv",
                       "express-validator", "compression"],
        "fullstack":  ["next", "react", "react-dom", "axios", "prisma",
                       "@prisma/client", "zod", "tailwindcss", "typescript"],
        "api":        ["express", "fastify", "cors", "helmet", "jsonwebtoken",
                       "bcryptjs", "dotenv", "zod"],
        "graphql":    ["@apollo/server", "graphql", "@graphql-tools/schema",
                       "type-graphql", "dataloader", "graphql-tag"],
        "db":         ["prisma", "@prisma/client", "mongoose", "sequelize",
                       "pg", "mysql2", "ioredis"],
        "testing":    ["jest", "vitest", "@testing-library/react",
                       "supertest", "faker", "playwright"],
        "cli":        ["commander", "inquirer", "chalk", "ora",
                       "boxen", "figlet", "cli-progress"],
        "realtime":   ["socket.io", "ws", "socket.io-client", "ioredis", "bullmq"],
        "desktop":    ["electron", "electron-builder", "@electron/remote",
                       "electron-store", "electron-updater"],
        "auth":       ["next-auth", "passport", "jsonwebtoken", "bcryptjs",
                       "@auth/core", "jose"],
        "web3":       ["ethers", "hardhat", "@nomicfoundation/hardhat-toolbox",
                       "web3", "@openzeppelin/contracts", "dotenv"],
        "ui":         ["@radix-ui/react-dialog", "@radix-ui/react-dropdown-menu",
                       "class-variance-authority", "clsx", "tailwind-merge",
                       "lucide-react", "framer-motion"],
        "monorepo":   ["turbo", "tsup", "typescript", "eslint",
                       "prettier", "changesets"],
    }

    def pip(self, req: str, *, dry_run: bool = False) -> bool:
        if req not in self.PIP:
            fail(f"Unknown pip set: '{req}'")
            self._list_pip()
            return False
        pkgs = self.PIP[req]
        step(f"pip install [{req}]  ({len(pkgs)} packages)")
        if dry_run:
            dim(f"  [dry-run] {sys.executable} -m pip install --upgrade --quiet {' '.join(pkgs)}")
            return True
        return _run_command(
            ["python", "-m", "pip", "install", "--upgrade", "--quiet"] + pkgs,
            hint="Verify internet connection and Python/pip availability.",
        )

    def npm(self, req: str, *, scope: str = "global", project_dir: str | None = None, dry_run: bool = False) -> bool:
        if req not in self.NPM:
            fail(f"Unknown npm set: '{req}'")
            self._list_npm()
            return False
        pkgs = self.NPM[req]
        base_cmd = ["npm.cmd", "install"]
        if scope == "global":
            base_cmd.append("-g")
        elif scope == "project":
            if not project_dir:
                fail("Project npm scope requires --project-dir")
                return False
            package_json = Path(project_dir) / "package.json"
            if not package_json.exists():
                fail(f"package.json not found in: {project_dir}")
                return False
        else:
            fail(f"Unknown npm scope: {scope}")
            return False

        step(f"npm install [{req}] [{scope}]  ({len(pkgs)} packages)")
        cmd = base_cmd + pkgs
        if scope == "project":
            cmd.extend(["--prefix", project_dir])
        if dry_run:
            dim(f"  [dry-run] {' '.join(cmd)}")
            return True

        return _run_command(
            cmd,
            hint="For project installs, ensure package.json exists and npm is installed.",
        )

    def _list_pip(self):
        from colours import CY, B, DM, R
        print(f"\n  {B}Python (pip) sets:{R}")
        for name, pkgs in self.PIP.items():
            print(f"    {CY}{name:<14}{R}  {DM}{len(pkgs):>2} pkgs:{R} {', '.join(pkgs[:4])} ...")

    def _list_npm(self):
        from colours import CY, B, DM, R
        print(f"\n  {B}Node (npm) sets:{R}")
        for name, pkgs in self.NPM.items():
            print(f"    {CY}{name:<14}{R}  {DM}{len(pkgs):>2} pkgs:{R} {', '.join(pkgs[:4])} ...")

    def list_all(self):
        self._list_pip()
        self._list_npm()
        print("\n  npm scopes: global (default) or project\n")
