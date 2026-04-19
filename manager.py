"""SetupManager — orchestrates stack installs and library installs."""
import sys

from colours import ok, fail, sep, head, BANNER, B, CY, G, DM, R, YL, RD, warn
from doctor import Doctor
from installer import LibraryInstaller, check_winget_available, RESULT_PASS, RESULT_WARN, RESULT_FAIL
from logger import log_event, log_structured
from stacks import build_stack_catalog


class SetupManager:
    LEGACY_STACK_HINTS = {
        "ai_ml": ("python", "ai_ml"),
        "llm": ("python", "llm"),
        "php": ("php_cli", None),
    }

    def __init__(self):
        self.catalog = build_stack_catalog()
        self.stacks = {name: meta.tools for name, meta in self.catalog.items()}
        self.libs   = LibraryInstaller()

    # ── setup ─────────────────────────────────────────────────────────────────

    def run_setup(
        self,
        stack: str,
        pip_req=None,
        npm_req=None,
        npm_scope: str = "global",
        project_dir: str | None = None,
        run_doctor: bool = True,
        fix_deps: bool = False,
        assume_yes: bool = False,
        dry_run: bool = False,
        verify: bool = False,
    ):
        if stack in self.LEGACY_STACK_HINTS:
            target_stack, suggested_pip = self.LEGACY_STACK_HINTS[stack]
            if suggested_pip:
                fail(
                    f"'{stack}' is a Python requirement set, not a tool stack.\n"
                    f"  Use: devset setup {target_stack} --pip {suggested_pip}"
                )
            else:
                fail(
                    f"'{stack}' was replaced.\n"
                    f"  Use: devset setup {target_stack}"
                )
            return

        if stack not in self.stacks:
            fail(f"Unknown stack: '{stack}'")
            self.list_stacks()
            sys.exit(1)
        if not dry_run and not check_winget_available():
            return

        meta = self.catalog[stack]
        tools = meta.tools

        print(BANNER)
        head(f"Stack  :  {stack.upper()}")
        print(f"  {B}About  :{R}  {meta.description}")
        print(f"  {B}Tools  :{R}  {', '.join(t.name for t in tools)}")
        if pip_req: print(f"  {B}pip    :{R}  {pip_req}")
        if npm_req:
            print(f"  {B}npm    :{R}  {npm_req}  ({npm_scope})")
            if project_dir:
                print(f"  {B}dir    :{R}  {project_dir}")
        if dry_run:
            print(f"  {B}mode   :{R}  dry-run (no changes applied)")
        sep()

        # ── 3-level result tracking ──────────────────────────────────────
        passed: list[str] = []
        warned: list[str] = []
        failed: list[str] = []
        installed: list[str] = []
        skipped: list[str] = []

        for idx, tool in enumerate(tools, start=1):
            print(f"  {DM}[{idx}/{len(tools)}] {tool.name}{R}")
            result = tool.ensure(dry_run=dry_run)

            # Classify result
            if result.status == RESULT_PASS:
                passed.append(tool.name)
            elif result.status == RESULT_WARN:
                warned.append(tool.name)
            else:
                failed.append(tool.name)

            # Track install/skip status
            if tool.last_status in {"installed", "planned_install"}:
                installed.append(tool.name)
            elif tool.last_status == "already_installed":
                skipped.append(tool.name)

        # ── Only STOP on true installation failures (RESULT_FAIL) ────────
        if failed:
            sep()
            fail("Setup stopped: one or more tools failed to install")
            print(f"  {RD}Failed tools: {', '.join(failed)}{R}")
            print(f"  {DM}See devsetup-log.txt for details.{R}\n")
            log_event(f"SETUP_ABORT stack={stack} failed={','.join(failed)}")
            return

        # ── Warnings do NOT stop setup — continue with pip/npm ───────────
        if pip_req:
            if self.libs.pip(pip_req, dry_run=dry_run):
                ok("Python libraries installed")
                log_event(f"PIP_SET_OK {pip_req}")
            else:
                fail("Python library install had errors")
                log_event(f"PIP_SET_FAIL {pip_req}")
        if npm_req:
            if self.libs.npm(npm_req, scope=npm_scope, project_dir=project_dir, dry_run=dry_run):
                ok("Node packages installed")
                log_event(f"NPM_SET_OK {npm_req} scope={npm_scope}")
            else:
                fail("Node package install had errors")
                log_event(f"NPM_SET_FAIL {npm_req} scope={npm_scope}")

        if run_doctor or verify:
            from doctor import _SPECIALIZED_CHECK_MAP
            # Auto-derive which specialized checks to run from the stack tools
            check_keys = {"path"}
            for tool in tools:
                if tool.path_key in _SPECIALIZED_CHECK_MAP:
                    check_keys.add(_SPECIALIZED_CHECK_MAP[tool.path_key])
            if stack in {"cpp", "game_cpp", "embedded"}:
                check_keys.add("cpp")

            doc = Doctor(auto_fix=fix_deps, assume_yes=assume_yes)
            # Pass tools so doctor auto-checks ALL tools (even without specialized checks)
            doc.run(check_keys, tools=tools)

        # ── Final summary with 3-level results ───────────────────────────
        sep()
        print(f"\n  {G}{B}[OK] Setup completed for {stack.upper()}.{R}")

        # Show per-tool result breakdown
        if passed:
            print(f"  {G}✔ PASS  :{R}  {', '.join(passed)}")
        if warned:
            print(f"  {YL}⚠ WARN  :{R}  {', '.join(warned)}")
            print(f"  {DM}  (Installed but not fully verified — likely PATH or version-check issue){R}")
        # failed tools already caused early return above, but just in case:
        if failed:
            print(f"  {RD}❌ FAIL  :{R}  {', '.join(failed)}")

        print(f"  {DM}Installed: {', '.join(installed) if installed else 'none'}{R}")
        print(f"  {DM}Skipped  : {', '.join(skipped) if skipped else 'none'}{R}")

        if warned:
            print()
            warn("Some tools have warnings. To resolve:")
            print(f"  {DM}  1. Open a new terminal (to pick up PATH changes){R}")
            print(f"  {DM}  2. Run: devset doctor  (to re-verify){R}")
            print(f"  {DM}  3. Or run: refreshenv  (if using Chocolatey){R}")
        else:
            print(f"  {DM}Open a new terminal to use updated PATH changes.{R}")

        print()
        log_event(f"SETUP_OK stack={stack}")
        log_structured(
            "setup_summary",
            stack=stack,
            dry_run=dry_run,
            passed_count=len(passed),
            warned_count=len(warned),
            failed_count=len(failed),
            installed_count=len(installed),
            skipped_count=len(skipped),
        )

    # ── list ──────────────────────────────────────────────────────────────────

    def list_stacks(self):
        print(BANNER)
        print(f"  {B}Available stacks:{R}\n")
        for name, meta in self.catalog.items():
            names = ", ".join(t.name for t in meta.tools)
            print(f"    {CY}{name:<14}{R}  {DM}{meta.description}{R}")
            print(f"    {DM}{' '*16}{names}{R}")
        print(f"\n  {B}Usage:{R}  devset setup <stack>  [--pip <set>]  [--npm <set>]")
        print(f"  {B}Tip  :{R}  devset list-reqs\n")

    def list_reqs(self):
        self.libs.list_all()

    def run_doctor(self, checks: set[str] | None = None, *, fix_deps: bool = False, assume_yes: bool = False):
        doc = Doctor(auto_fix=fix_deps, assume_yes=assume_yes)
        doc.run(checks)

    def explain_stack(self, stack: str):
        if stack not in self.catalog:
            fail(f"Unknown stack: '{stack}'")
            return
        meta = self.catalog[stack]
        print(BANNER)
        head(f"Stack  :  {meta.name}")
        print(f"  {B}What   :{R}  {meta.description}")
        print(f"  {B}Use    :{R}  {meta.use_case}")
        print(f"  {B}Tools  :{R}  {', '.join(t.name for t in meta.tools)}")
        if meta.suggested_pip:
            print(f"  {B}pip    :{R}  {', '.join(meta.suggested_pip)}")
        if meta.suggested_npm:
            print(f"  {B}npm    :{R}  {', '.join(meta.suggested_npm)}")
        print()
