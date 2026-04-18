"""
PATH management via Windows registry.
User PATH (HKEY_CURRENT_USER) requires NO admin rights.
System PATH (HKEY_LOCAL_MACHINE) requires admin — we never touch it.
"""
import ctypes
import os

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
    "r":         [r"%ProgramFiles%\R\bin"],
    "terraform": [r"%ProgramFiles%\HashiCorp\Terraform"],
    "devsetup":  [r"C:\DevSetup"],
}


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
        return False
    return set_user_path(current.rstrip(";") + ";" + directory)


def ensure_paths_for(tool_key: str) -> list[str]:
    """Add all known paths for a tool. Returns list of newly-added dirs."""
    dirs   = TOOL_PATHS.get(tool_key, [])
    added  = []
    current = get_user_path()
    for d in dirs:
        if not in_path(current, d):
            current = current.rstrip(";") + ";" + d
            added.append(d)
    if added:
        set_user_path(current)
    return added
