# DevSetup CLI

`DevSetup` is a Windows-first developer environment bootstrap CLI.
It installs curated toolchains, manages user-level PATH updates, and optionally installs Python and Node package sets.

## Key Features

- Installs role-based tool stacks using `winget`
- Updates user PATH safely through `HKEY_CURRENT_USER\Environment`
- Supports Python package sets via `--pip <set>`
- Supports Node package sets via `--npm <set>` with `global` or `project` scope
- Provides clear discovery commands (`list`, `list-reqs`)

## Security and Runtime Behavior

- No system PATH modifications
- No automatic privilege escalation
- No destructive system operations
- Non-install commands remain non-admin by design

## Command Reference

- `setup <stack>`: install stack tools and optional package sets
- `list`: show available stacks
- `list-reqs`: show available `pip` and `npm` package sets
- `add-path <directory>`: add a directory to user PATH

## Quick Start

```powershell
python .\devsetup.py list
python .\devsetup.py setup python
python .\devsetup.py setup fullstack --pip web --npm fullstack
```

## Stack Model

Stacks are intentionally tool-focused. Package ecosystems are handled separately through `--pip` and `--npm`.

### PHP Profiles

- `php_cli`: CLI-focused PHP development (`PHP + Composer`)
- `php_web`: local web development profile (`XAMPP`)

### Requirement Sets (Not Stacks)

- `ai_ml` and `llm` are Python package sets, not stack names
- Example: `python .\devsetup.py setup python --pip ai_ml`

## Package Set Usage

```powershell
# Python package set
python .\devsetup.py setup python --pip ai_ml

# npm package set, global scope
python .\devsetup.py setup node --npm react --npm-scope global

# npm package set, project scope
python .\devsetup.py setup node --npm express --npm-scope project --project-dir "D:\work\api"
```

`--npm-scope` values:

- `global` (default): installs with `npm install -g`
- `project`: requires `--project-dir` containing `package.json`

## Development and Build

Validate syntax:

```powershell
python -m py_compile devsetup.py manager.py installer.py stacks.py pathutil.py colours.py
```

Build executable:

```powershell
pyinstaller devsetup.spec --noconfirm --clean
```

