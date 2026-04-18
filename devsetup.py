"""
DevSetup v3.1
One-command developer environment installer for Windows.

First run  -> copies itself to C:\\DevSetup and adds to PATH (no UAC on future runs)
Every run  -> normal CLI, no extra prompts
"""

import argparse
import os
import shutil
import sys
import subprocess

# ── Self-registration ─────────────────────────────────────────────────────────
# Runs once: copies the exe to C:\DevSetup\ and adds it to USER path.
# User PATH writes need NO admin rights — so no UAC on subsequent runs.

INSTALL_DIR = r"C:\DevSetup"
INSTALL_EXE = os.path.join(INSTALL_DIR, "devsetup.exe")
FALLBACK_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "DevSetup")
FALLBACK_EXE = os.path.join(FALLBACK_DIR, "devsetup.exe")


def _is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def _already_installed() -> bool:
    if not _is_frozen():
        return True   # running as .py in dev, skip
    current_exe = os.path.abspath(sys.executable).lower()
    return current_exe in {INSTALL_EXE.lower(), FALLBACK_EXE.lower()}


def _relaunch_installed(target_exe: str) -> None:
    """Relaunch the installed executable and exit current process."""
    try:
        subprocess.Popen([target_exe] + sys.argv[1:])
    except Exception:
        # If relaunch fails, keep current process alive so command still runs.
        return
    sys.exit(0)


def self_install():
    """
    Copy exe to C:\\DevSetup and add to user PATH — silently, once.
    No UAC required because we only touch HKEY_CURRENT_USER\\Environment.
    """
    if _already_installed():
        return

    from pathutil import add_to_path
    from colours import ok, warn
    target_exe = None

    try:
        os.makedirs(INSTALL_DIR, exist_ok=True)
        shutil.copy2(sys.executable, INSTALL_EXE)
        ok(f"DevSetup installed -> {INSTALL_EXE}")
        target_exe = INSTALL_EXE
    except PermissionError:
        # C:\ may need elevation — fall back to user's AppData
        try:
            os.makedirs(FALLBACK_DIR, exist_ok=True)
            shutil.copy2(sys.executable, FALLBACK_EXE)
            add_to_path(FALLBACK_DIR)
            ok(f"DevSetup installed -> {FALLBACK_EXE}")
            target_exe = FALLBACK_EXE
        except Exception as e:
            warn(f"Could not self-install: {e}")
            return
    except Exception as e:
        warn(f"Could not copy exe: {e}")
        return

    if target_exe == INSTALL_EXE:
        added = add_to_path(INSTALL_DIR)
        if added:
            ok(f"PATH <- {INSTALL_DIR}  (devsetup now works from any terminal)")
    elif target_exe == FALLBACK_EXE:
        added = add_to_path(FALLBACK_DIR)
        if added:
            ok(f"PATH <- {FALLBACK_DIR}  (devsetup now works from any terminal)")

    # If launched from a non-installed path, hand over to installed EXE once.
    if target_exe and os.path.abspath(sys.executable).lower() != target_exe.lower():
        _relaunch_installed(target_exe)
    # No broadcast needed — pathutil.add_to_path already broadcasts


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="devsetup",
        description="DevSetup v3.1 - Windows developer environment manager",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  devsetup setup python\n"
            "  devsetup setup python  --pip ai_ml\n"
            "  devsetup setup node    --npm react\n"
            "  devsetup setup fullstack --pip web --npm fullstack\n"
            "  devsetup list\n"
            "  devsetup list-reqs\n"
            '  devsetup add-path "C:\\MyTool\\bin"\n'
        ),
    )
    p.add_argument("--version", action="version", version="DevSetup v3.1")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("setup",     help="Install a dev stack")
    s.add_argument("stack",         help="Stack name (run 'list' to see all)")
    s.add_argument("--pip",         metavar="SET", help="Python library set to install")
    s.add_argument("--npm",         metavar="SET", help="Node package set to install")
    s.add_argument(
        "--npm-scope",
        choices=["global", "project"],
        default="global",
        help="Install npm libraries globally (default) or into a project",
    )
    s.add_argument(
        "--project-dir",
        metavar="DIR",
        help="Project directory when using --npm-scope project (must contain package.json)",
    )

    sub.add_parser("list",          help="Show all available stacks")
    sub.add_parser("list-reqs",     help="Show all pip / npm library sets")

    ap = sub.add_parser("add-path", help="Add a directory to user PATH permanently")
    ap.add_argument("directory",    help="Full path to add, e.g. C:\\MyTool\\bin")

    return p


def main():
    # 1. Self-register on first launch (no UAC needed)
    self_install()

    # 2. Parse args early so we know the command
    args = build_parser().parse_args()

    # 3. Route to manager
    from manager import SetupManager
    from pathutil import add_to_path, ensure_paths_for
    from colours  import ok, BANNER

    mgr = SetupManager()

    if args.command == "setup":
        if args.npm_scope == "project" and not args.project_dir:
            from colours import fail
            fail("When using --npm-scope project, you must pass --project-dir")
            sys.exit(2)
        mgr.run_setup(
            args.stack,
            pip_req=args.pip,
            npm_req=args.npm,
            npm_scope=args.npm_scope,
            project_dir=args.project_dir,
        )

    elif args.command == "list":
        mgr.list_stacks()

    elif args.command == "list-reqs":
        mgr.list_reqs()

    elif args.command == "add-path":
        d = args.directory.strip().strip('"')
        if add_to_path(d):
            ok(f"Added to PATH: {d}")
        else:
            ok(f"Already in PATH: {d}")


if __name__ == "__main__":
    main()
