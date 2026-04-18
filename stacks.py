"""Stack definitions and metadata."""
from dataclasses import dataclass

from installer import Installer


@dataclass(frozen=True)
class StackMeta:
    name: str
    description: str
    use_case: str
    tools: list[Installer]
    suggested_pip: list[str]
    suggested_npm: list[str]


def _T(name, cmd, wid, pk=""):
    return Installer(name, cmd, wid, pk)


def build_stack_catalog() -> dict[str, StackMeta]:
    # ── Tool registry ─────────────────────────────────────────────────────────

    # Languages & runtimes
    python    = _T("Python 3.12",      "python",        "Python.Python.3.12",                "python")
    node      = _T("Node.js",          "node",          "OpenJS.NodeJS",                     "node")
    deno      = _T("Deno",             "deno",          "DenoLand.Deno",                     "deno")
    bun       = _T("Bun",              "bun",           "Oven-sh.Bun",                       "bun")
    java      = _T("Java JDK 21",      "java",          "EclipseAdoptium.Temurin.21.JDK",    "java")
    go        = _T("Go",               "go",            "GoLang.Go",                         "go")
    rust      = _T("Rust",             "rustc",         "Rustlang.Rustup",                   "rust")
    cpp       = _T("MinGW (C/C++)",    "g++",           "MSYS2.MSYS2")
    php       = _T("PHP (CLI)",        "php",           "PHP.PHP",                           "php")
    ruby      = _T("Ruby 3.2",         "ruby",          "RubyInstallerTeam.Ruby.3.2",        "ruby")
    dotnet    = _T(".NET SDK 8",       "dotnet",        "Microsoft.DotNet.SDK.8",            "dotnet")
    kotlin    = _T("Kotlin",           "kotlinc",       "JetBrains.Kotlin")
    julia     = _T("Julia",            "julia",         "Julialang.Julia",                   "julia")
    r_lang    = _T("R",                "Rscript",       "RProject.R",                        "r")
    lua       = _T("Lua",              "lua",           "DEVCOM.Lua")
    perl      = _T("Perl",             "perl",          "StrawberryPerl.StrawberryPerl",     "perl")
    elixir    = _T("Elixir",           "elixir",        "ElixirLang.Elixir",                 "elixir")
    erlang    = _T("Erlang/OTP",       "erl",           "ErlangOTP.ErlangOTP",               "erlang")
    scala     = _T("Scala (via sbt)",  "sbt",           "sbt.sbt",                           "scala")
    swift     = _T("Swift",            "swift",         "Swift.Toolchain")
    zig       = _T("Zig",              "zig",           "zig.zig",                           "zig")

    # Editors & IDEs
    vscode    = _T("VS Code",          "code",          "Microsoft.VisualStudioCode")
    sublime   = _T("Sublime Text",     "subl",          "SublimeHQ.SublimeText.4")
    neovim    = _T("Neovim",           "nvim",          "Neovim.Neovim",                     "neovim")

    # Version control & collaboration
    git       = _T("Git",              "git",           "Git.Git",                           "git")
    gh        = _T("GitHub CLI",       "gh",            "GitHub.cli")

    # Containers & orchestration
    docker    = _T("Docker Desktop",   "docker",        "Docker.DockerDesktop")
    kubectl   = _T("kubectl",          "kubectl",       "Kubernetes.kubectl")
    helm      = _T("Helm",             "helm",          "Helm.Helm")
    minikube  = _T("Minikube",         "minikube",      "Kubernetes.minikube")

    # Build tools
    cmake     = _T("CMake",            "cmake",         "Kitware.CMake",                     "cmake")
    gradle    = _T("Gradle",           "gradle",        "Gradle.Gradle",                     "gradle")
    maven     = _T("Maven",            "mvn",           "Apache.Maven",                      "maven")
    composer  = _T("Composer",         "composer",      "Composer.Composer")

    # Databases & caches
    postgres  = _T("PostgreSQL",       "psql",          "PostgreSQL.PostgreSQL")
    mysql     = _T("MySQL",            "mysql",         "Oracle.MySQL",                      "mysql")
    mongodb   = _T("MongoDB Shell",    "mongosh",       "MongoDB.Shell",                     "mongodb")
    redis_s   = _T("Redis",            "redis-cli",     "Redis.Redis")
    sqlite    = _T("SQLite",           "sqlite3",       "SQLite.SQLite")

    # Infra & cloud
    terraform = _T("Terraform",        "terraform",     "Hashicorp.Terraform",               "terraform")
    nginx     = _T("Nginx",            "nginx",         "nginx.nginx")
    awscli    = _T("AWS CLI",          "aws",           "Amazon.AWSCLI")
    azcli     = _T("Azure CLI",        "az",            "Microsoft.AzureCLI")
    gcloud    = _T("Google Cloud CLI", "gcloud",        "Google.CloudSDK")

    # PHP web
    xampp     = _T("XAMPP",            "xampp-control", "ApacheFriends.Xampp",                "xampp")

    # Mobile
    flutter   = _T("Flutter",          "flutter",       "Google.FlutterSDK",                 "flutter")
    android   = _T("Android Studio",   "studio",        "Google.AndroidStudio")

    # API & DB tools
    postman   = _T("Postman",          "postman",       "Postman.Postman")
    insomnia  = _T("Insomnia",         "insomnia",      "Kong.Insomnia")
    dbeaver   = _T("DBeaver",          "dbeaver",       "dbeaver.dbeaver")

    # Game engines
    godot     = _T("Godot Engine",     "godot",         "GodotEngine.GodotEngine")

    # System tools
    pwsh      = _T("PowerShell 7",     "pwsh",          "Microsoft.PowerShell")
    wt        = _T("Windows Terminal", "wt",            "Microsoft.WindowsTerminal")

    return {
        # ── Core language stacks (minimal + practical) ───────────────────────
        "python":     StackMeta("python",     "Python development environment",      "General Python app development",                 [python, vscode, git],                                        ["basic", "web", "ai_ml", "llm"],    []),
        "node":       StackMeta("node",       "Node.js development environment",     "General Node app development",                   [node, vscode, git],                                          [],                                  ["basic", "react", "express"]),
        "deno":       StackMeta("deno",       "Deno development environment",        "Modern TypeScript-first runtime",                [deno, vscode, git],                                          [],                                  []),
        "bun":        StackMeta("bun",        "Bun development environment",         "Fast all-in-one JS/TS runtime",                  [bun, vscode, git],                                           [],                                  []),
        "java":       StackMeta("java",       "Java development environment",        "Backend and JVM applications",                   [java, maven, vscode, git],                                   [],                                  []),
        "go":         StackMeta("go",         "Go development environment",          "Go services and tooling",                        [go, vscode, git],                                            [],                                  []),
        "rust":       StackMeta("rust",       "Rust development environment",        "Systems and CLI development with Rust",          [rust, vscode, git],                                          [],                                  []),
        "cpp":        StackMeta("cpp",        "C/C++ development environment",       "Native app and systems development",             [cpp, cmake, vscode, git],                                    [],                                  []),
        "zig":        StackMeta("zig",        "Zig development environment",         "Modern systems programming with Zig",            [zig, vscode, git],                                           [],                                  []),
        "php_cli":    StackMeta("php_cli",    "PHP CLI profile",                     "CLI and scripting in PHP with Composer",         [php, composer, vscode, git],                                 [],                                  []),
        "php_web":    StackMeta("php_web",    "PHP web profile",                     "Local web stack with Apache/MySQL via XAMPP",    [xampp, vscode, git, postman],                                 [],                                  []),
        "ruby":       StackMeta("ruby",       "Ruby development environment",        "Ruby scripts and app development",               [ruby, vscode, git],                                          [],                                  []),
        "dotnet":     StackMeta("dotnet",     ".NET development environment",        "C# and .NET application development",            [dotnet, vscode, git],                                        [],                                  []),
        "kotlin":     StackMeta("kotlin",     "Kotlin development environment",      "Kotlin and Android-adjacent development",        [kotlin, java, android, git],                                 [],                                  []),
        "scala":      StackMeta("scala",      "Scala development environment",       "Scala and JVM functional programming",           [scala, java, vscode, git],                                   [],                                  []),
        "julia":      StackMeta("julia",      "Julia development environment",       "Scientific and technical computing",             [julia, vscode, git],                                         [],                                  []),
        "r":          StackMeta("r",          "R development environment",           "Statistical and data analysis in R",             [r_lang, vscode, git],                                        [],                                  []),
        "elixir":     StackMeta("elixir",     "Elixir development environment",      "Elixir/Erlang fault-tolerant applications",      [elixir, erlang, vscode, git],                                [],                                  []),
        "lua":        StackMeta("lua",        "Lua development environment",         "Lua scripting and embedding",                    [lua, vscode, git],                                           [],                                  []),
        "perl":       StackMeta("perl",       "Perl development environment",        "Perl scripting and text processing",             [perl, vscode, git],                                          [],                                  []),
        "swift":      StackMeta("swift",      "Swift development environment",       "Swift development on Windows",                   [swift, vscode, git],                                         [],                                  []),
        # ── Product/application stacks ────────────────────────────────────────
        "frontend":   StackMeta("frontend",   "Frontend web stack",                  "React/Vite/SPA frontend workflows",              [node, vscode, git],                                          [],                                  ["react", "testing"]),
        "backend":    StackMeta("backend",    "Backend API stack",                   "API and backend service development",            [node, python, docker, postgres, git, postman, vscode],       ["api", "db"],                       ["api", "db"]),
        "fullstack":  StackMeta("fullstack",  "Full-stack web stack",                "Frontend + backend + local infra",               [node, python, docker, postgres, git, postman, vscode],       ["web"],                             ["fullstack"]),
        "mobile":     StackMeta("mobile",     "Mobile dev stack",                    "Flutter and Android app development",            [flutter, android, git, vscode],                              [],                                  []),
        "android":    StackMeta("android",    "Android stack",                       "Android app and SDK development",                [android, java, git, vscode],                                 [],                                  []),
        "desktop":    StackMeta("desktop",    "Desktop app stack",                   "Electron/.NET desktop workflows",                [node, dotnet, vscode, git],                                  [],                                  ["desktop"]),
        "web3":       StackMeta("web3",       "Web3 / blockchain stack",             "Solidity, Hardhat, smart contract development",  [node, python, git, vscode],                                  ["web"],                             ["web3"]),
        "scripting":  StackMeta("scripting",  "Lightweight scripting stack",         "Quick scripts and automation",                   [python, node, git, vscode],                                  ["basic", "automation"],             ["basic", "cli"]),
        # ── Infrastructure / ops stacks ───────────────────────────────────────
        "devops":     StackMeta("devops",     "DevOps stack",                        "Container and infrastructure automation",        [docker, terraform, kubectl, helm, git, vscode, nginx],       ["devops"],                          []),
        "cloud":      StackMeta("cloud",      "Cloud engineering stack",             "Cloud-first platform development",               [python, node, docker, terraform, awscli, git, vscode],       ["devops"],                          []),
        "cloud_aws":  StackMeta("cloud_aws",  "AWS cloud stack",                     "AWS-focused cloud development",                  [python, awscli, docker, terraform, git, vscode],             ["devops"],                          []),
        "cloud_azure":StackMeta("cloud_azure","Azure cloud stack",                   "Azure-focused cloud development",                [python, azcli, docker, terraform, dotnet, git, vscode],      ["devops"],                          []),
        "cloud_gcp":  StackMeta("cloud_gcp",  "GCP cloud stack",                     "Google Cloud-focused development",               [python, gcloud, docker, terraform, git, vscode],             ["devops"],                          []),
        "k8s":        StackMeta("k8s",        "Kubernetes stack",                    "Container orchestration and microservices",       [docker, kubectl, helm, minikube, git, vscode],               [],                                  []),
        "sre":        StackMeta("sre",        "Site reliability stack",              "Reliability engineering and operations",          [docker, terraform, nginx, python, git, vscode],              [],                                  []),
        # ── Data / compute stacks ─────────────────────────────────────────────
        "data_engineer": StackMeta("data_engineer", "Data engineering stack",         "Data pipelines and storage workflows",           [python, postgres, docker, dbeaver, git, vscode],             ["data", "db"],                      []),
        "data_science":  StackMeta("data_science",  "Data science stack",             "Analysis and experimentation workflows",         [python, r_lang, dbeaver, git, vscode],                       ["data", "ai_ml", "visualization"],  []),
        "ml_engineer":   StackMeta("ml_engineer",   "ML engineering stack",           "Model training and deployment workflows",        [python, docker, dbeaver, git, vscode],                       ["ai_ml", "llm"],                    []),
        "nlp":           StackMeta("nlp",           "NLP / text processing stack",    "Natural language processing workflows",          [python, git, vscode],                                        ["nlp", "ai_ml"],                    []),
        # ── Domain-focused stacks ─────────────────────────────────────────────
        "db":         StackMeta("db",         "Database stack",                      "Database and cache development environment",     [dbeaver, postgres, mysql, redis_s, docker, git],             ["db"],                              ["db"]),
        "mongo":      StackMeta("mongo",      "MongoDB stack",                       "MongoDB development environment",                [mongodb, dbeaver, docker, git, vscode],                      ["db"],                              ["db"]),
        "api_dev":    StackMeta("api_dev",    "API development stack",               "API design, implementation, and testing",        [node, python, postman, docker, git, vscode],                 ["api"],                             ["api"]),
        "automation": StackMeta("automation", "Automation stack",                    "Task automation and scripting",                  [python, git, vscode],                                        ["automation"],                      ["cli"]),
        "game_cpp":   StackMeta("game_cpp",   "C++ game stack",                      "Native game/tool development with C++",          [cpp, cmake, vscode, git],                                    [],                                  []),
        "game_godot": StackMeta("game_godot", "Godot game stack",                    "2D/3D game development with Godot",              [godot, vscode, git],                                         [],                                  []),
        "security":   StackMeta("security",   "Security / pentest stack",            "Security research and penetration testing",      [python, git, docker, vscode],                                ["security", "scraping"],            []),
        "embedded":   StackMeta("embedded",   "Embedded / IoT stack",                "Microcontroller and IoT development",            [python, cpp, cmake, git, vscode],                            ["basic"],                           []),
        # ── Convenience stacks ────────────────────────────────────────────────
        "java_full":  StackMeta("java_full",  "Java full stack",                     "Java backend with Maven + Gradle + DB tools",    [java, maven, gradle, postgres, dbeaver, docker, git, vscode],[],                                  []),
        "starter":    StackMeta("starter",    "Starter pack",                        "Essential tools for any developer",              [python, node, git, vscode, docker, pwsh, wt],                ["basic"],                           ["basic"]),
    }


def build_stacks() -> dict[str, list[Installer]]:
    """Compatibility helper for callers needing only stack tools."""
    return {name: meta.tools for name, meta in build_stack_catalog().items()}
