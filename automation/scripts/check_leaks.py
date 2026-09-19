#!/usr/bin/env python3
"""Fail the build when kit content carries traces of a private origin.

This kit is extracted from a real, private setup. Nothing about that setup — the
people, the employer, the product, the board, the machines — may survive into the
published material. Editorial care is not enough for that: this check is the gate.

Two layers, deliberately:

1. STRUCTURAL rules (in this file, public): shapes that are almost always a leak
   regardless of who you are — a Windows drive path, a real e-mail address, a URL
   pointing at one specific board, issue or workspace. These catch the accident
   nobody thought to add to a list.

2. A DENYLIST of literal terms (never committed): names of people, companies and
   products. It is read from the PACT_DENYLIST environment variable or from a
   local, git-ignored file. It stays out of the repository on purpose — a
   committed list of secrets-to-avoid is itself an index of what you are hiding.

Usage:
    check_leaks.py [paths...]          # defaults to the repository root
    PACT_DENYLIST="acme,jane doe" check_leaks.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
DENYLIST_FILE = REPO_ROOT / ".leakcheck-denylist"
# The list (and its committed example) name the terms they forbid; scanning
# them would make every configured denylist fail against itself.
DENYLIST_NAMES = {".leakcheck-denylist", ".leakcheck-denylist.example"}

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".render-out"}
TEXT_SUFFIXES = {
    ".md", ".yml", ".yaml", ".json", ".py", ".txt", ".toml", ".cfg",
    ".ini", ".sh", ".ps1", ".graphql", ".wiql", ".example", ".svg", ".mdc", ".csv", ".tsv",
}
# LICENSE, Makefile and the rest have no suffix and would otherwise skip L0.
EXTENSIONLESS_TEXT_NAMES = {
    "license", "makefile", "notice", "authors", "copying", "dockerfile",
    "gemfile", "procfile", "contributing", "changelog", "version",
}

# Placeholders the kit uses on purpose. A structural rule that matches one of
# these is a false positive, not a leak.
ALLOWED = {
    "acme-corp", "acme.example", "example-org", "example.com", "sample-team",
    "your-org", "your-team", "user@example.com",
    "dev.azure.com/example-org", "github.com/example-org",
}

# Rules that do not apply to some file types: a Python decorator is not a handle.
# .wiql has @project / @Me macros; .graphql has @directives; .svg has @media.
RULE_SKIP_SUFFIXES: dict[str, set[str]] = {
    "handle": {".py", ".wiql", ".graphql", ".svg", ".ps1"},
}
RULE_SKIP_NAMES: dict[str, set[str]] = {
    "handle": {"makefile", "gnumakefile"},
}

# Directories whose content is SUPPOSED to trip the rules (known-bad fixtures).
SKIP_PATH_PARTS: tuple[tuple[str, ...], ...] = (("automation", "tests", "fixtures", "leaks"),)

STRUCTURAL_RULES: list[tuple[str, re.Pattern[str], str]] = [
    (
        "local-path",
        re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][A-Za-z0-9_\-]"),
        "Windows drive path — points at someone's machine. Use a relative path or a placeholder.",
    ),
    (
        "local-path",
        re.compile(r"(?<![\w.])/(?:home|Users)/(?!user\b|you\b)[A-Za-z0-9_\-]+/"),
        "Absolute home directory — points at someone's machine.",
    ),
    (
        "email",
        re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
        "E-mail address. Use user@example.com.",
    ),
    (
        "board-url",
        re.compile(r"github\.com/(?:users|orgs)/[^/\s)]+/projects/\d+"),
        "Link to one specific GitHub Project. Describe the board, do not link it.",
    ),
    (
        "item-url",
        re.compile(r"github\.com/[^/\s)]+/[^/\s)]+/(?:issues|pull)/\d+"),
        "Link to one specific issue or pull request from a real repository.",
    ),
    (
        "repo-url",
        re.compile(
            r"github\.com/(?!users/|orgs/|example-org/|your-org/)"
            r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9._-]+"
        ),
        "Link to one specific GitHub repository. Describe it, or use github.com/example-org/…",
    ),
    (
        "board-url",
        re.compile(r"dev\.azure\.com/[^/\s)]+/[^/\s)]+"),
        "Link to one specific Azure DevOps project.",
    ),
    (
        "workspace-url",
        re.compile(r"[A-Za-z0-9\-]+\.slack\.com"),
        "Link to one specific Slack workspace.",
    ),
    (
        "workspace-url",
        re.compile(r"notion\.so/[0-9a-f]{32}"),
        "Link to one specific Notion page.",
    ),
    (
        "handle",
        re.compile(r"(?<![\w`/])@[A-Za-z][A-Za-z0-9\-]{2,}(?![\w`/])"),
        "Looks like a user handle. Name a role, not a person.",
    ),
]


def load_denylist() -> list[str]:
    """Literal terms to forbid. Never read from a committed file."""
    terms: list[str] = []
    raw_env = os.environ.get("PACT_DENYLIST", "")
    terms.extend(part.strip() for part in raw_env.split(",") if part.strip())
    if DENYLIST_FILE.is_file():
        for line in DENYLIST_FILE.read_text(encoding="utf-8").splitlines():
            entry = line.strip()
            if entry and not entry.startswith("#"):
                terms.append(entry)
    return [t.lower() for t in terms]


def is_allowed(match: str, line: str) -> bool:
    lowered = match.lower()
    if any(placeholder in lowered for placeholder in ALLOWED):
        return True
    # f-string / template braces: `dev.azure.com/{org}/{project}` is a shape, not a place.
    if "{" in match or "<" in match:
        return True
    # A match sitting inside a {{TEMPLATE_VAR}} is a placeholder by construction.
    return "{{" in line and "}}" in line and match in line[line.find("{{") :]


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith("."):
        return True
    return path.name.lower() in EXTENSIONLESS_TEXT_NAMES


def is_denylist_path(path: Path) -> bool:
    if path.name in DENYLIST_NAMES:
        return True
    try:
        return path.resolve() == DENYLIST_FILE.resolve()
    except OSError:
        return False


def iter_files(roots: list[Path], explicit: bool = False):
    for root in roots:
        if root.is_file():
            yield root
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            parts = path.parts
            if any(all(seg in parts for seg in skip) for skip in SKIP_PATH_PARTS) and not explicit:
                continue
            if is_text_file(path):
                yield path


def scan(paths: list[Path], denylist: list[str], explicit: bool = False) -> Report:
    report = Report(check="check_leaks — origin traces in kit content")
    for path in iter_files(paths, explicit=explicit):
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            if is_text_file(path):
                report.add(str(rel), None, "encoding", "not valid UTF-8 — text suffixes in this kit must be UTF-8")
            continue
        except OSError:
            continue
        report.scanned += 1

        for lineno, line in enumerate(text.splitlines(), start=1):
            for rule, pattern, message in STRUCTURAL_RULES:
                if path.suffix.lower() in RULE_SKIP_SUFFIXES.get(rule, set()):
                    continue
                if path.name.lower() in RULE_SKIP_NAMES.get(rule, set()):
                    continue
                for match in pattern.findall(line):
                    found = match if isinstance(match, str) else match[0]
                    if is_allowed(found, line):
                        continue
                    report.add(str(rel), lineno, rule, f"{message}  (found: {found!r})")

            if is_denylist_path(path):
                continue
            lowered = line.lower()
            for term in denylist:
                if term in lowered:
                    report.add(
                        str(rel),
                        lineno,
                        "denylist",
                        "Matches a term on the local denylist. Replace it with a neutral placeholder.",
                    )
    return report


def main() -> int:
    args = [Path(a).resolve() for a in sys.argv[1:]] or [REPO_ROOT]
    denylist = load_denylist()
    if not denylist:
        print(
            "  note: no denylist configured — structural rules only.\n"
            "        set PACT_DENYLIST=term1,term2 or copy .leakcheck-denylist.example "
            "to .leakcheck-denylist to also forbid literal names.",
            file=sys.stderr,
        )
    # Paths given on the command line are scanned even if they are known-bad fixtures
    # (that is how the fixture test exercises the rules).
    return scan(args, denylist, explicit=bool(sys.argv[1:])).emit()


if __name__ == "__main__":
    raise SystemExit(main())
