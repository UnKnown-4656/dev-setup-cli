"""
DevSetup v3.2
One-command developer environment installer for Windows.

First run  -> copies itself to C:\\DevSetup and adds to PATH (no UAC on future runs)
Every run  -> normal CLI, no extra prompts
"""

import argparse
import os
import shutil
import sys
import subprocess
from logger import log_event

# ── Self-registration ─────────────────────────────────────────────────────────
# Runs once: copies the exe to C:\DevSetup\ and adds it to USER path.
# User PATH writes need NO admin rights — so no UAC on subsequent runs.

INSTALL_DIR = r"C:\DevSetup"
INSTALL_EXE = os.path.join(INSTALL_DIR, "devset.exe")
FALLBACK_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "DevSetup")
FALLBACK_EXE = os.path.join(FALLBACK_DIR, "devset.exe")


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
            warn("Restart terminal to apply PATH changes")
    elif target_exe == FALLBACK_EXE:
        added = add_to_path(FALLBACK_DIR)
        if added:
            ok(f"PATH <- {FALLBACK_DIR}  (devsetup now works from any terminal)")
            warn("Restart terminal to apply PATH changes")

    # If launched from a non-installed path, hand over to installed EXE once.
    if target_exe and os.path.abspath(sys.executable).lower() != target_exe.lower():
        _relaunch_installed(target_exe)
    # No broadcast needed — pathutil.add_to_path already broadcasts


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="devset",
        description="DevSetup v3.2 - Windows developer environment manager",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  devset setup python\n"
            "  devset setup python  --pip ai_ml\n"
            "  devset setup node    --npm react\n"
            "  devset setup fullstack --pip web --npm fullstack\n"
            "  devset setup rust --dry-run\n"
            "  devset explain backend\n"
            "  devset doctor --check rust path --fix-deps\n"
            "  devset list\n"
            "  devset list-reqs\n"
            '  devset add-path "C:\\MyTool\\bin"\n'
        ),
    )
    p.add_argument("--version", action="version", version="DevSetup v3.2")
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
    s.add_argument(
        "--no-doctor",
        action="store_true",
        help="Skip post-install dependency checks",
    )
    s.add_argument(
        "--fix-deps",
        action="store_true",
        help="Automatically try to fix missing dependencies during doctor checks",
    )
    s.add_argument(
        "--yes",
        action="store_true",
        help="Assume yes for dependency-fix prompts when possible",
    )
    s.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without applying changes",
    )
    s.add_argument(
        "--verify",
        action="store_true",
        help="Run strict post-setup verification checks",
    )

    sub.add_parser("list",          help="Show all available stacks")
    ex = sub.add_parser("explain",  help="Explain a stack and recommended package sets")
    ex.add_argument("stack",        help="Stack name to explain")
    sub.add_parser("list-reqs",     help="Show all pip / npm library sets")
    d = sub.add_parser("doctor",    help="Check toolchain health and missing dependencies")
    d.add_argument(
        "--check",
        choices=["rust", "python", "node", "git", "cpp", "r", "path", "all"],
        nargs="+",
        default=["all"],
        help="Select checks to run (default: all)",
    )
    d.add_argument(
        "--fix-deps",
        action="store_true",
        help="Automatically try to fix missing dependencies",
    )
    d.add_argument(
        "--fix-suggestions",
        action="store_true",
        help="Show fix suggestions only (default behavior)",
    )
    d.add_argument(
        "--yes",
        action="store_true",
        help="Assume yes for dependency-fix prompts when possible",
    )

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
    from pathutil import add_to_path
    from colours  import ok

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
            run_doctor=not args.no_doctor,
            fix_deps=args.fix_deps,
            assume_yes=args.yes,
            dry_run=args.dry_run,
            verify=args.verify,
        )

    elif args.command == "list":
        mgr.list_stacks()

    elif args.command == "explain":
        mgr.explain_stack(args.stack)

    elif args.command == "list-reqs":
        mgr.list_reqs()

    elif args.command == "doctor":
        checks = set(args.check)
        if "all" in checks:
            checks = {"rust", "python", "node", "git", "cpp", "r", "path"}
        mgr.run_doctor(checks, fix_deps=args.fix_deps, assume_yes=args.yes)

    elif args.command == "add-path":
        d = args.directory.strip().strip('"')
        if add_to_path(d):
            ok(f"Added to PATH: {d}")
            from colours import warn
            warn("Restart terminal to apply PATH changes")
            log_event(f"ADD_PATH_OK {d}")
        else:
            ok(f"Already in PATH: {d}")
            log_event(f"ADD_PATH_SKIPPED {d}")


if __name__ == "__main__":
    main()
