"""Post-install health checks and dependency remediation helpers."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from colours import B, CY, DM, R, fail, ok, step, warn
from pathutil import get_user_path, ensure_paths_for, _resolve_r_paths


# Mapping from tool path_key → specialized doctor check name.
# Tools NOT listed here get a generic check automatically.
_SPECIALIZED_CHECK_MAP = {
    "rust":   "rust",
    "python": "python",
    "node":   "node",
    "git":    "git",
    "cmake":  "cpp",
    "r":      "r",
}


class Doctor:
    """Checks developer toolchain health and optionally applies fixes."""

    def __init__(self, *, auto_fix: bool = False, assume_yes: bool = False):
        self.auto_fix = auto_fix
        self.assume_yes = assume_yes
        self.ok_count = 0
        self.warn_count = 0
        self.fail_count = 0

    def _record(self, status: str, message: str):
        if status == "ok":
            self.ok_count += 1
            ok(message)
        elif status == "warn":
            self.warn_count += 1
            warn(message)
        else:
            self.fail_count += 1
            fail(message)

    def _run(self, cmd: list[str]) -> tuple[bool, str]:
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=15)
            out = (p.stdout or p.stderr or "").strip()
            return True, out
        except Exception as exc:
            return False, str(exc)

    def _ask_to_fix(self, prompt: str) -> bool:
        if self.auto_fix or self.assume_yes:
            return True
        if not sys.stdin or not sys.stdin.isatty():
            self._record("warn", "Non-interactive session detected; skipping auto-fix prompt")
            return False
        try:
            choice = input(f"  {CY}[?]{R} {prompt} [Y/n]: ").strip().lower()
        except EOFError:
            return False
        return choice in {"", "y", "yes"}

    def _install_vs_build_tools(self) -> bool:
        step("Installing Microsoft Visual Studio 2022 Build Tools")
        cmd = [
            "winget", "install", "-e",
            "--id", "Microsoft.VisualStudio.2022.BuildTools",
            "--accept-package-agreements",
            "--accept-source-agreements",
        ]
        if self.assume_yes:
            cmd.append("--silent")
        ok_run, output = self._run(cmd)
        if ok_run:
            self._record("ok", "Visual Studio Build Tools installation started/completed")
            if output:
                print(f"  {DM}{output[:200]}{'...' if len(output) > 200 else ''}{R}")
            return True
        self._record("warn", "Could not install Visual Studio Build Tools automatically")
        print(f"  {DM}Hint: run manually -> winget install -e --id Microsoft.VisualStudio.2022.BuildTools{R}")
        return False

    # ── Specialized checks ────────────────────────────────────────────────────

    def _check_rust(self):
        step("Doctor check: Rust toolchain")
        rustc = shutil.which("rustc")
        cargo = shutil.which("cargo")
        link = shutil.which("link")

        if rustc:
            self._record("ok", f"rustc found at {rustc}")
        else:
            self._record("fail", "rustc not found in PATH")

        if cargo:
            self._record("ok", f"cargo found at {cargo}")
        else:
            self._record("warn", "cargo not found in PATH")

        if link:
            self._record("ok", f"MSVC linker (link.exe) found at {link}")
            return

        self._record("warn", "MSVC linker (link.exe) not found; native Rust builds may fail")
        print(f"  {DM}Rust is installed, but C/C++ build tools are missing.{R}")
        if self._ask_to_fix("Install Visual Studio Build Tools now?"):
            self._install_vs_build_tools()

    def _check_python(self):
        step("Doctor check: Python toolchain")
        py = shutil.which("python") or shutil.which("py")
        if py:
            self._record("ok", f"Python launcher found: {py}")
        else:
            self._record("fail", "Python executable not found in PATH")
            return

        ok_run, output = self._run([sys.executable, "-m", "pip", "--version"])
        if ok_run:
            self._record("ok", f"pip is available ({output})")
        else:
            self._record("warn", "pip check failed; package installs may fail")

    def _check_node(self):
        step("Doctor check: Node toolchain")
        node = shutil.which("node")
        npm = shutil.which("npm")

        if node:
            self._record("ok", f"node found at {node}")
        else:
            self._record("warn", "node not found in PATH")
        if npm:
            self._record("ok", f"npm found at {npm}")
        else:
            self._record("warn", "npm not found in PATH")

    def _check_git(self):
        step("Doctor check: Git toolchain")
        git = shutil.which("git")
        if not git:
            self._record("warn", "git not found in PATH")
            return
        ok_run, output = self._run(["git", "--version"])
        if ok_run:
            self._record("ok", output or f"git found at {git}")
        else:
            self._record("warn", "git found but version check failed")

    def _check_cpp(self):
        step("Doctor check: C/C++ toolchain")
        gcc = shutil.which("gcc")
        gpp = shutil.which("g++")
        cl = shutil.which("cl")
        link = shutil.which("link")

        if gcc or gpp or cl:
            found = gcc or gpp or cl
            self._record("ok", f"C/C++ compiler found at {found}")
        else:
            self._record("warn", "No C/C++ compiler found (gcc/g++/cl)")
        if link:
            self._record("ok", "MSVC linker is available")
        else:
            self._record("warn", "MSVC linker (link.exe) is not available")

    def _check_r(self):
        step("Doctor check: R toolchain")
        rscript = shutil.which("Rscript")
        r_exe = shutil.which("R")

        if rscript:
            self._record("ok", f"Rscript found at {rscript}")
            ok_run, output = self._run(["Rscript", "--version"])
            if ok_run:
                version_line = (output.splitlines()[0] if output else "").strip()
                self._record("ok", f"R version: {version_line}")
            else:
                self._record("warn", "Rscript found but version check failed")
            return

        if r_exe:
            self._record("ok", f"R found at {r_exe} (but Rscript not in PATH)")
        else:
            self._record("warn", "R / Rscript not found in PATH")

        # Try to find R installation on disk
        r_paths = _resolve_r_paths()
        if r_paths:
            print(f"  {DM}R installation detected at: {r_paths[0]}{R}")
            print(f"  {DM}But it is NOT in your PATH — that's why it's not detected.{R}")
            if self._ask_to_fix("Add R to your PATH now?"):
                added = ensure_paths_for("r")
                if added:
                    for a in added:
                        self._record("ok", f"PATH ← {a}")
                    warn("PATH updated. Open a new terminal or run: refreshenv")
                else:
                    self._record("ok", "R paths already in PATH (restart terminal to apply)")
            else:
                print(f"  {DM}To fix manually, add to PATH:{R}")
                for p in r_paths:
                    print(f"  {DM}  {p}{R}")
        else:
            self._record("fail", "R is not installed on this system")
            print(f"  {DM}Install R: winget install -e --id RProject.R{R}")
            print(f"  {DM}Or download from: https://cran.r-project.org/bin/windows/{R}")

    def _check_path(self):
        step("Doctor check: PATH integrity")
        path_val = get_user_path()
        if not path_val:
            self._record("warn", "User PATH is empty")
            return
        entries = [e.strip() for e in path_val.split(";") if e.strip()]
        lower = [e.lower() for e in entries]
        duplicates = len(lower) - len(set(lower))
        if duplicates:
            self._record("warn", f"User PATH has {duplicates} duplicate entries")
        else:
            self._record("ok", "User PATH has no duplicate entries")

    # ── Generic tool check (works for ANY tool) ───────────────────────────────

    def _check_generic_tool(self, tool_name: str, check_cmd: str):
        """Generic health check for any tool: is it in PATH? Can it respond?"""
        step(f"Doctor check: {tool_name}")
        location = shutil.which(check_cmd)

        if not location:
            self._record("warn", f"{tool_name} ({check_cmd}) not found in PATH")
            return

        self._record("ok", f"{tool_name} found at {location}")

        # Try to get version (lenient — first line only)
        for args in ([check_cmd, "--version"], [check_cmd, "-v"], [check_cmd, "-V"]):
            ok_run, output = self._run(args)
            if ok_run and output:
                version_line = output.splitlines()[0].strip()
                self._record("ok", f"{tool_name} version: {version_line}")
                return

        # No version output is fine — tool exists and that's what matters
        self._record("ok", f"{tool_name} is available (version check skipped)")

    # ── Main runner ───────────────────────────────────────────────────────────

    # Recognized specialized check names
    _SPECIALIZED_NAMES = {"rust", "python", "node", "git", "cpp", "r", "path"}

    def run(self, checks: set[str] | None = None, *, tools=None):
        """Run health checks.

        Args:
            checks: Set of named checks to run. Defaults to all known checks.
            tools:  Optional list of Installer objects from a stack. Any tool
                    that doesn't map to a specialized check gets a generic
                    PATH + version check automatically. This means doctor
                    works for EVERY stack without manual mapping.
        """
        checks = checks or {"rust", "python", "node", "git", "cpp", "r", "path"}
        print(f"\n  {B}Running DevSet doctor...{R}\n")

        # Run specialized checks
        if "rust" in checks:
            self._check_rust()
        if "python" in checks:
            self._check_python()
        if "node" in checks:
            self._check_node()
        if "git" in checks:
            self._check_git()
        if "cpp" in checks:
            self._check_cpp()
        if "r" in checks:
            self._check_r()
        if "path" in checks:
            self._check_path()

        # Auto-check any stack tools that DON'T have specialized checks
        if tools:
            already_checked_cmds: set[str] = set()
            for tool in tools:
                # Skip if this tool's command was already covered
                if tool.check_cmd in already_checked_cmds:
                    continue
                already_checked_cmds.add(tool.check_cmd)

                # Skip if this tool maps to a specialized check we already ran
                if tool.path_key in _SPECIALIZED_CHECK_MAP:
                    mapped_check = _SPECIALIZED_CHECK_MAP[tool.path_key]
                    if mapped_check in checks:
                        continue

                # Run a generic check for this tool
                self._check_generic_tool(tool.name, tool.check_cmd)

        print(f"\n  {B}Doctor summary:{R} {CY}{self.ok_count} ok{R}, {CY}{self.warn_count} warnings{R}, {CY}{self.fail_count} failures{R}\n")
