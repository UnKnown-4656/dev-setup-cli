"""Terminal colour helpers — auto-enables ANSI on Windows."""
import ctypes

def enable_ansi():
    try:
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    except Exception:
        pass

enable_ansi()

R  = "\033[0m"
B  = "\033[1m"
G  = "\033[92m"
RD = "\033[91m"
CY = "\033[96m"
YL = "\033[93m"
DM = "\033[2m"
MG = "\033[95m"

def ok(msg):    print(f"  {G}[OK]{R}  {msg}")
def fail(msg):  print(f"  {RD}[X]{R}   {msg}")
def step(msg):  print(f"\n  {CY}[>]{R}  {B}{msg}{R}")
def warn(msg):  print(f"  {YL}[!]{R}  {msg}")
def dim(msg):   print(f"  {DM}{msg}{R}")
def head(msg):  print(f"\n  {MG}{B}{msg}{R}")
def sep():      print(f"  {DM}{'-'*46}{R}")

BANNER = f"""
{CY}{B}+--------------------------------------------+
|              DevSetup  v1                   |
|     Windows Developer Environment Manager   |
+--------------------------------------------+{R}
"""
