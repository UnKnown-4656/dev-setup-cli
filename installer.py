"""Tool and library installer classes."""
import shutil
import subprocess
import sys
from pathlib import Path

from colours import ok, fail, step, dim
from pathutil import ensure_paths_for


class InstallError(RuntimeError):
    """Raised when an installation operation cannot be completed."""


def _run_command(cmd: list[str], *, hint: str = "") -> bool:
    """Run a command and convert runtime errors into user-friendly output."""
    try:
        subprocess.run(cmd, check=True)
        return True
    except FileNotFoundError:
        fail(f"Command not found: {cmd[0]}")
        if hint:
            dim(f"  Hint: {hint}")
        return False
    except subprocess.CalledProcessError as exc:
        fail(f"Command failed (exit={exc.returncode}): {' '.join(cmd)}")
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

    def is_installed(self) -> bool:
        return shutil.which(self.check_cmd) is not None

    def install(self):
        step(f"Installing {self.name}")
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
            return
        ok(f"{self.name} installed")

        if self.path_key:
            added = ensure_paths_for(self.path_key)
            for a in added:
                dim(f"  PATH ← {a}")

    def ensure(self):
        if self.is_installed():
            ok(f"{self.name} already installed")
            if self.path_key:
                added = ensure_paths_for(self.path_key)
                for a in added:
                    dim(f"  PATH ← {a}")
        else:
            self.install()


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
    }

    NPM: dict[str, list[str]] = {
        "basic":      ["lodash", "axios", "dotenv", "chalk", "uuid"],
        "react":      ["react", "react-dom", "react-router-dom", "axios",
                       "@tanstack/react-query", "zustand", "tailwindcss"],
        "express":    ["express", "cors", "helmet", "morgan", "dotenv",
                       "express-validator", "compression"],
        "fullstack":  ["next", "react", "react-dom", "axios", "prisma",
                       "@prisma/client", "zod", "tailwindcss", "typescript"],
        "api":        ["express", "fastify", "cors", "helmet", "jsonwebtoken",
                       "bcryptjs", "dotenv", "zod"],
        "db":         ["prisma", "@prisma/client", "mongoose", "sequelize",
                       "pg", "mysql2", "ioredis"],
        "testing":    ["jest", "vitest", "@testing-library/react",
                       "supertest", "faker", "playwright"],
        "cli":        ["commander", "inquirer", "chalk", "ora",
                       "boxen", "figlet", "cli-progress"],
        "realtime":   ["socket.io", "ws", "socket.io-client", "ioredis", "bullmq"],
        "desktop":    ["electron", "electron-builder", "@electron/remote",
                       "electron-store", "electron-updater"],
    }

    def pip(self, req: str) -> bool:
        if req not in self.PIP:
            fail(f"Unknown pip set: '{req}'")
            self._list_pip()
            return False
        pkgs = self.PIP[req]
        step(f"pip install [{req}]  ({len(pkgs)} packages)")
        return _run_command(
            [sys.executable, "-m", "pip", "install", "--upgrade", "--quiet"] + pkgs,
            hint="Verify internet connection and Python/pip availability.",
        )

    def npm(self, req: str, *, scope: str = "global", project_dir: str | None = None) -> bool:
        if req not in self.NPM:
            fail(f"Unknown npm set: '{req}'")
            self._list_npm()
            return False
        pkgs = self.NPM[req]
        base_cmd = ["npm", "install"]
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
