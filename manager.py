"""SetupManager — orchestrates stack installs and library installs."""
import sys

from colours import ok, fail, sep, head, BANNER, B, CY, G, DM, R
from installer import LibraryInstaller
from stacks import build_stacks


class SetupManager:
    LEGACY_STACK_HINTS = {
        "ai_ml": ("python", "ai_ml"),
        "llm": ("python", "llm"),
        "php": ("php_cli", None),
    }

    def __init__(self):
        self.stacks = build_stacks()
        self.libs   = LibraryInstaller()

    # ── setup ─────────────────────────────────────────────────────────────────

    def run_setup(self, stack: str, pip_req=None, npm_req=None, npm_scope: str = "global", project_dir: str | None = None):
        if stack in self.LEGACY_STACK_HINTS:
            target_stack, suggested_pip = self.LEGACY_STACK_HINTS[stack]
            if suggested_pip:
                fail(
                    f"'{stack}' is a Python requirement set, not a tool stack.\n"
                    f"  Use: devsetup setup {target_stack} --pip {suggested_pip}"
                )
            else:
                fail(
                    f"'{stack}' was replaced.\n"
                    f"  Use: devsetup setup {target_stack}"
                )
            return

        if stack not in self.stacks:
            fail(f"Unknown stack: '{stack}'")
            self.list_stacks()
            sys.exit(1)

        tools = self.stacks[stack]

        print(BANNER)
        head(f"Stack  :  {stack.upper()}")
        print(f"  {B}Tools  :{R}  {', '.join(t.name for t in tools)}")
        if pip_req: print(f"  {B}pip    :{R}  {pip_req}")
        if npm_req:
            print(f"  {B}npm    :{R}  {npm_req}  ({npm_scope})")
            if project_dir:
                print(f"  {B}dir    :{R}  {project_dir}")
        sep()

        for tool in tools:
            tool.ensure()

        if pip_req:
            if self.libs.pip(pip_req):
                ok("Python libraries installed")
            else:
                fail("Python library install had errors")
        if npm_req:
            if self.libs.npm(npm_req, scope=npm_scope, project_dir=project_dir):
                ok("Node packages installed")
            else:
                fail("Node package install had errors")

        sep()
        print(f"\n  {G}{B}[OK] Setup completed for {stack.upper()}.{R}")
        print(f"  {DM}Open a new terminal to use updated PATH changes.{R}\n")

    # ── list ──────────────────────────────────────────────────────────────────

    def list_stacks(self):
        print(BANNER)
        print(f"  {B}Available stacks:{R}\n")
        for name, tools in self.stacks.items():
            names = ", ".join(t.name for t in tools)
            print(f"    {CY}{name:<14}{R}  {DM}{names}{R}")
        print(f"\n  {B}Usage:{R}  devsetup setup <stack>  [--pip <set>]  [--npm <set>]")
        print(f"  {B}Tip  :{R}  devsetup list-reqs\n")

    def list_reqs(self):
        self.libs.list_all()
