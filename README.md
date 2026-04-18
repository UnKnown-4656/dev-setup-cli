# DevSetup CLI

DevSetup is a Windows-focused CLI to set up developer environments quickly.
It installs tools with `winget`, updates your user PATH, and can install optional Python/Node package sets.

## Easy Install (EXE)

Download the latest executable from Releases:

- [Download `devsetup.exe` (latest release)](https://github.com/UnKnown-4656/dev-setup-cli/releases/latest)

Install steps:

1. Download `devsetup.exe` from the release page.
2. Run it once in a terminal:

```powershell
.\devsetup.exe --help
```

3. The app self-registers and adds itself to your user PATH.
4. Open a new terminal and run:

```powershell
devsetup --help
```

Note: If no release is published yet, use the source build steps in this README.

## Highlights

- Install curated tool stacks with one command
- Add required tool paths to your user PATH automatically
- Install Python package sets with `--pip`
- Install Node package sets with `--npm`
- Discover available stacks and requirement sets from the CLI

## Important Behavior (Clear Version)

- DevSetup updates **user PATH** only (`HKEY_CURRENT_USER\Environment`)
- DevSetup does **not** edit **system PATH** (`HKEY_LOCAL_MACHINE`)
- DevSetup does **not** force automatic UAC/admin relaunch
- Commands like `list`, `list-reqs`, and `add-path` are normal non-admin operations

This means tools can still work immediately for your account (after opening a new terminal), without making machine-wide PATH changes.

## Command Reference

- `devsetup setup <stack>`: install stack tools
- `devsetup list`: show all available stacks
- `devsetup list-reqs`: show all `pip` and `npm` package sets
- `devsetup add-path <directory>`: add directory to user PATH

## Quick Start

```powershell
python .\devsetup.py list
python .\devsetup.py setup python
python .\devsetup.py setup fullstack --pip web --npm fullstack
```

## Stack Design

Stacks are tool-focused. Language libraries are managed separately with `--pip` and `--npm`.

### PHP Profiles

- `php_cli`: PHP CLI + Composer workflow
- `php_web`: XAMPP-based local web workflow

### Requirement Sets (Not Stack Names)

`ai_ml` and `llm` are Python package sets, not stacks.

Use:

```powershell
python .\devsetup.py setup python --pip ai_ml
python .\devsetup.py setup python --pip llm
```

## Package Set Examples

```powershell
# Python set
python .\devsetup.py setup python --pip ai_ml

# npm set (global)
python .\devsetup.py setup node --npm react --npm-scope global

# npm set (project)
python .\devsetup.py setup node --npm express --npm-scope project --project-dir "D:\work\api"
```

`--npm-scope` options:

- `global` (default): runs `npm install -g`
- `project`: requires `--project-dir` containing `package.json`

## Build and Validation

Run syntax checks:

```powershell
python -m py_compile devsetup.py manager.py installer.py stacks.py pathutil.py colours.py
```

Build executable:

```powershell
pyinstaller devsetup.spec --noconfirm --clean
```
