"""Stack definitions — maps stack name → list of Installer objects."""
from installer import Installer


def _T(name, cmd, wid, pk=""):
    return Installer(name, cmd, wid, pk)


def build_stacks() -> dict[str, list[Installer]]:
    # ── Tool registry ─────────────────────────────────────────────────────────
    python    = _T("Python 3.12",      "python",    "Python.Python.3.12",                "python")
    vscode    = _T("VS Code",          "code",      "Microsoft.VisualStudioCode")
    node      = _T("Node.js",          "node",      "OpenJS.NodeJS",                     "node")
    git       = _T("Git",              "git",       "Git.Git",                           "git")
    docker    = _T("Docker Desktop",   "docker",    "Docker.DockerDesktop")
    java      = _T("Java JDK 21",      "java",      "EclipseAdoptium.Temurin.21.JDK",   "java")
    go        = _T("Go",               "go",        "GoLang.Go",                         "go")
    rust      = _T("Rust",             "rustc",     "Rustlang.Rustup",                   "rust")
    cpp       = _T("MinGW (C/C++)",    "g++",       "MSYS2.MSYS2")
    php       = _T("PHP (CLI)",        "php",       "PHP.PHP",                           "php")
    composer  = _T("Composer",         "composer",  "Composer.Composer")
    xampp     = _T("XAMPP",            "xampp-control", "ApacheFriends.Xampp",           "xampp")
    ruby      = _T("Ruby 3.2",         "ruby",      "RubyInstallerTeam.Ruby.3.2",        "ruby")
    android   = _T("Android Studio",   "studio",    "Google.AndroidStudio")
    postman   = _T("Postman",          "postman",   "Postman.Postman")
    dbeaver   = _T("DBeaver",          "dbeaver",   "dbeaver.dbeaver")
    dotnet    = _T(".NET SDK 8",       "dotnet",    "Microsoft.DotNet.SDK.8",            "dotnet")
    kotlin    = _T("Kotlin",           "kotlinc",   "JetBrains.Kotlin")
    flutter   = _T("Flutter",          "flutter",   "Google.FlutterSDK",                "flutter")
    postgres  = _T("PostgreSQL",       "psql",      "PostgreSQL.PostgreSQL")
    redis_s   = _T("Redis",            "redis-cli", "Redis.Redis")
    nginx     = _T("Nginx",            "nginx",     "nginx.nginx")
    cmake     = _T("CMake",            "cmake",     "Kitware.CMake",                     "cmake")
    julia     = _T("Julia",            "julia",     "Julialang.Julia",                   "julia")
    r_lang    = _T("R",                "Rscript",   "RProject.R",                        "r")
    terraform = _T("Terraform",        "terraform", "Hashicorp.Terraform",               "terraform")

    return {
        # ── Core language stacks (minimal + practical) ───────────────────────
        "python":         [python, vscode, git],
        "node":           [node, vscode, git],
        "java":           [java, vscode, git],
        "go":             [go, vscode, git],
        "rust":           [rust, vscode, git],
        "cpp":            [cpp, cmake, vscode, git],
        "php_cli":        [php, composer, vscode, git],
        "php_web":        [xampp, vscode, git, postman],
        "ruby":           [ruby, vscode, git],
        "dotnet":         [dotnet, vscode, git],
        "kotlin":         [kotlin, java, android, git],
        "julia":          [julia, vscode, git],
        "r":              [r_lang, vscode, git],
        # ── Product/application stacks ────────────────────────────────────────
        "frontend":       [node, vscode, git],
        "backend":        [node, python, docker, postgres, git, postman, vscode],
        "fullstack":      [node, python, docker, postgres, git, postman, vscode],
        "mobile":         [flutter, android, git, vscode],
        "android":        [android, java, git, vscode],
        "desktop":        [node, dotnet, vscode, git],
        # ── Infrastructure / ops stacks ───────────────────────────────────────
        "devops":         [docker, terraform, git, vscode, nginx],
        "cloud":          [python, node, docker, terraform, git, vscode],
        "sre":            [docker, terraform, nginx, python, git, vscode],
        # ── Data / compute stacks ─────────────────────────────────────────────
        "data_engineer":  [python, postgres, docker, dbeaver, git, vscode],
        "data_science":   [python, dbeaver, git, vscode],
        "ml_engineer":    [python, docker, dbeaver, git, vscode],
        # ── Domain-focused stacks ─────────────────────────────────────────────
        "db":             [dbeaver, postgres, redis_s, docker, git],
        "api_dev":        [node, python, postman, docker, git, vscode],
        "automation":     [python, git, vscode],
        "game_cpp":       [cpp, cmake, vscode, git],
    }
