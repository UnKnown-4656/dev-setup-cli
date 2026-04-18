"""
PATH management via Windows registry.
User PATH (HKEY_CURRENT_USER) requires NO admin rights.
System PATH (HKEY_LOCAL_MACHINE) requires admin — we never touch it.
"""
import ctypes
import os
import re
from pathlib import Path
from logger import log_event

try:
    import winreg
    _HAS_WINREG = True
except ImportError:
    _HAS_WINREG = False   # Linux dev/build


# ── Well-known install locations for each tool ────────────────────────────────

TOOL_PATHS: dict[str, list[str]] = {
    "python": [
        r"%LOCALAPPDATA%\Programs\Python\Python312",
        r"%LOCALAPPDATA%\Programs\Python\Python312\Scripts",
        r"%LOCALAPPDATA%\Programs\Python\Launcher",
    ],
    "node":      [r"%ProgramFiles%\nodejs"],
    "deno":      [r"%USERPROFILE%\.deno\bin"],
    "bun":       [r"%USERPROFILE%\.bun\bin"],
    "git":       [r"%ProgramFiles%\Git\cmd",
                  r"%ProgramFiles%\Git\usr\bin"],
    "go":        [r"%ProgramFiles%\Go\bin",
                  r"%USERPROFILE%\go\bin"],
    "rust":      [r"%USERPROFILE%\.cargo\bin"],
    "java":      [r"%ProgramFiles%\Eclipse Adoptium\jdk-21\bin"],
    "dotnet":    [r"%ProgramFiles%\dotnet"],
    "flutter":   [r"%LOCALAPPDATA%\flutter\bin"],
    "ruby":      [r"%ProgramFiles%\Ruby32\bin"],
    "php":       [r"%ProgramFiles%\PHP"],
    "xampp":     [r"C:\xampp",
                  r"C:\xampp\php",
                  r"C:\xampp\mysql\bin"],
    "cmake":     [r"%ProgramFiles%\CMake\bin"],
    "julia":     [r"%ProgramFiles%\Julia\bin"],
    "r":         [],   # Resolved dynamically by _resolve_r_paths()
    "terraform": [r"%ProgramFiles%\HashiCorp\Terraform"],
    "zig":       [r"%LOCALAPPDATA%\zig"],
    "elixir":    [r"%ProgramFiles%\Elixir\bin"],
    "erlang":    [r"%ProgramFiles%\Erlang OTP\bin"],
    "scala":     [r"%ProgramFiles%\sbt\bin"],
    "perl":      [r"C:\Strawberry\perl\bin",
                  r"C:\Strawberry\c\bin"],
    "gradle":    [r"%ProgramFiles%\Gradle\bin"],
    "maven":     [r"%ProgramFiles%\Apache\Maven\bin"],
    "mysql":     [r"%ProgramFiles%\MySQL\MySQL Server 8.0\bin"],
    "mongodb":   [r"%ProgramFiles%\mongosh"],
    "neovim":    [r"%ProgramFiles%\Neovim\bin"],
    "devsetup":  [r"C:\DevSetup"],
}


def _resolve_r_paths() -> list[str]:
    """Scan `C:\\Program Files\\R\\` for versioned folders, pick the highest,
    and return `bin\\x64` (64-bit, default) and `bin` as fallback paths.

    R on Windows installs to:
        C:\\Program Files\\R\\R-4.3.2\\bin\\x64
    NOT to:
        C:\\Program Files\\R\\bin      (this path does NOT exist)
    """
    r_root = Path(os.path.expandvars(r"%ProgramFiles%\R"))
    if not r_root.is_dir():
        log_event("R_PATH_SCAN no R root directory found")
        return []

    # Find all R-x.x.x version folders
    version_dirs: list[tuple[tuple[int, ...], Path]] = []
    for child in r_root.iterdir():
        if child.is_dir() and child.name.upper().startswith("R-"):
            # Extract version numbers from folder name like R-4.3.2
            match = re.search(r"R-(\d+(?:\.\d+)*)", child.name, re.IGNORECASE)
            if match:
                parts = tuple(int(x) for x in match.group(1).split("."))
                version_dirs.append((parts, child))

    if not version_dirs:
        log_event("R_PATH_SCAN no versioned R folders found")
        return []

    # Sort by version tuple (highest last) and pick the latest
    version_dirs.sort(key=lambda x: x[0])
    _, latest = version_dirs[-1]

    paths = []
    # Prefer bin\x64 (64-bit executables — standard on modern Windows)
    x64_bin = latest / "bin" / "x64"
    if x64_bin.is_dir():
        paths.append(str(x64_bin))
    # Also add bin\ as fallback
    plain_bin = latest / "bin"
    if plain_bin.is_dir():
        paths.append(str(plain_bin))

    log_event(f"R_PATH_SCAN resolved: {'; '.join(paths)}")
    return paths


def _broadcast():
    """Tell running processes (Explorer, cmd, PS) that ENV changed — no reboot."""
    try:
        HWND_BROADCAST   = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        res = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0,
            "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(res)
        )
    except Exception:
        pass


def get_user_path() -> str:
    if not _HAS_WINREG:
        return os.environ.get("PATH", "")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Environment", 0, winreg.KEY_READ) as k:
            val, _ = winreg.QueryValueEx(k, "Path")
            return val or ""
    except Exception:
        return os.environ.get("PATH", "")


def set_user_path(new_path: str) -> bool:
    if not _HAS_WINREG:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Environment", 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        _broadcast()
        return True
    except Exception:
        return False


def in_path(current: str, entry: str) -> bool:
    exp = os.path.expandvars(entry).lower()
    return exp in current.lower() or entry.lower() in current.lower()


def add_to_path(directory: str) -> bool:
    """Add directory to user PATH. Returns True if actually added."""
    current = get_user_path()
    if in_path(current, directory):
        log_event(f"PATH_SKIPPED already-present {directory}")
        return False
    changed = set_user_path(current.rstrip(";") + ";" + directory)
    if changed:
        log_event(f"PATH_ADDED {directory}")
    else:
        log_event(f"PATH_ADD_FAIL {directory}")
    return changed


def ensure_paths_for(tool_key: str) -> list[str]:
    """Add all known paths for a tool. Returns list of newly-added dirs."""
    # For R, dynamically resolve the actual versioned install path
    if tool_key == "r":
        dirs = _resolve_r_paths()
    else:
        dirs = TOOL_PATHS.get(tool_key, [])

    added  = []
    current = get_user_path()
    for d in dirs:
        if not in_path(current, d):
            current = current.rstrip(";") + ";" + d
            added.append(d)
    if added:
        changed = set_user_path(current)
        if changed:
            log_event(f"PATH_BATCH_ADDED {tool_key}: {';'.join(added)}")
        else:
            log_event(f"PATH_BATCH_FAIL {tool_key}")
    return added
