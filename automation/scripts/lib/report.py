"""Shared PASS/FAIL reporting for every kit check.

Each check produces Findings; this module renders them the same way so a
contributor sees one consistent report whether a link is broken, a schema is
invalid, or a leak was caught.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field


GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


def _paint(text: str, color: str) -> str:
    """Colour only when attached to a terminal; CI logs stay clean."""
    if not sys.stdout.isatty():
        return text
    return f"{color}{text}{RESET}"


def _configure_stdio() -> None:
    """Windows cp1252 cannot print arrows used in findings. Prefer UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def _safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        raw = (text + "\n").encode(encoding, errors="replace")
        buffer = getattr(sys.stdout, "buffer", None)
        if buffer is not None:
            buffer.write(raw)
            buffer.flush()
        else:
            sys.stdout.write(raw.decode(encoding, errors="replace"))


@dataclass(frozen=True)
class Finding:
    """One problem, anchored where a human can go fix it."""

    path: str
    line: int | None
    rule: str
    message: str

    def render(self) -> str:
        where = self.path if self.line is None else f"{self.path}:{self.line}"
        return f"  {where}\n    {_paint(self.rule, YELLOW)}  {self.message}"


@dataclass
class Report:
    """Collects findings for one check and decides the exit code."""

    check: str
    findings: list[Finding] = field(default_factory=list)
    scanned: int = 0

    def add(self, path: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(Finding(path=path, line=line, rule=rule, message=message))

    @property
    def ok(self) -> bool:
        return not self.findings

    def emit(self) -> int:
        """Print the report and return the process exit code."""
        _configure_stdio()
        counted = f"{self.scanned} file{'s' if self.scanned != 1 else ''}"
        if self.ok:
            _safe_print(f"{_paint('PASS', GREEN)}  {self.check}  {_paint(f'({counted})', DIM)}")
            return 0

        _safe_print(f"{_paint('FAIL', RED)}  {self.check}  {_paint(f'({counted})', DIM)}")
        for finding in self.findings:
            _safe_print(finding.render())
        total = len(self.findings)
        _safe_print(f"\n  {total} problem{'s' if total != 1 else ''} found.")
        return 1
