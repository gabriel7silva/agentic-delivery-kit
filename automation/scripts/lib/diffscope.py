"""Changed paths → scopes → owners → risk floor.

The one piece of logic that both the PR validator and the tests depend on, so
it lives here and nowhere else. Glob matching supports `**` (any depth), `*`
(within one segment) and `?`. When several globs match a path, the most
specific one wins — measured as the number of literal (non-wildcard)
characters, so `src/storage/**` beats `src/**`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .model import REPO_ROOT, load_yaml

RISK_ORDER = {"low": 0, "medium": 1, "high": 2}


def glob_to_regex(glob: str) -> re.Pattern[str]:
    out = []
    i = 0
    while i < len(glob):
        ch = glob[i]
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
            continue
        if glob.startswith("**", i):
            out.append(".*")
            i += 2
            continue
        if ch == "*":
            out.append("[^/]*")
        elif ch == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(ch))
        i += 1
    return re.compile("^" + "".join(out) + "$")


def specificity(glob: str) -> int:
    return sum(1 for c in glob if c not in "*?")


@dataclass(frozen=True)
class Scope:
    id: str
    paths: tuple[str, ...]
    writer: str
    reviewers: tuple[str, ...]
    floor: str


@dataclass(frozen=True)
class Resolution:
    path: str
    scope: Scope
    floor: str            # from risk-floors.yml if a floor matches, else the scope's


class Ownership:
    def __init__(self, ownership: dict, floors: dict | None = None):
        self.scopes = [
            Scope(
                id=s["id"], paths=tuple(s["paths"]), writer=s["writer"],
                reviewers=tuple(s["reviewers"]), floor=s["floor"],
            )
            for s in ownership["scopes"]
        ]
        d = ownership["default_scope"]
        self.default = Scope(
            id="default", paths=(), writer=d["writer"],
            reviewers=tuple(d["reviewers"]), floor=d["floor"],
        )
        self._compiled = [
            (glob_to_regex(g), specificity(g), s) for s in self.scopes for g in s.paths
        ]
        self._floors = [
            (glob_to_regex(g), specificity(g), f["floor"])
            for f in (floors or {}).get("floors", []) for g in f["paths"]
        ]

    @classmethod
    def from_repo(cls, root: Path = REPO_ROOT) -> "Ownership":
        ownership = load_yaml(root / "agents" / "ownership.yml")
        floors_path = root / "agents" / "policies" / "risk-floors.yml"
        floors = load_yaml(floors_path) if floors_path.is_file() else None
        return cls(ownership, floors)

    def scope_for(self, path: str) -> Scope:
        best: tuple[int, Scope] | None = None
        for rx, spec, scope in self._compiled:
            if rx.match(path) and (best is None or spec > best[0]):
                best = (spec, scope)
        return best[1] if best else self.default

    def floor_for(self, path: str, scope: Scope) -> str:
        best: tuple[int, str] | None = None
        for rx, spec, floor in self._floors:
            if rx.match(path) and (best is None or spec > best[0]):
                best = (spec, floor)
        return best[1] if best else scope.floor

    def resolve(self, paths: list[str]) -> list[Resolution]:
        out = []
        for p in paths:
            scope = self.scope_for(p)
            out.append(Resolution(path=p, scope=scope, floor=self.floor_for(p, scope)))
        return out

    def duplicate_globs(self) -> list[tuple[str, str, str]]:
        seen: dict[str, str] = {}
        dups = []
        for s in self.scopes:
            for g in s.paths:
                if g in seen:
                    dups.append((g, seen[g], s.id))
                seen[g] = s.id
        return dups


def max_risk(levels: list[str]) -> str:
    if not levels:
        return "low"
    normalised = []
    for level in levels:
        key = (level or "").lower()
        normalised.append(key if key in RISK_ORDER else "high")
    return max(normalised, key=lambda l: RISK_ORDER[l])


def required_reviewers(resolutions: list[Resolution]) -> set[str]:
    """Union of reviewers on the touched scopes. Use missing_reviewers for the gate."""
    out: set[str] = set()
    for r in resolutions:
        out.update(r.scope.reviewers)
    return out


def missing_reviewers(
    resolutions: list[Resolution],
    have: set[str],
    risk: str,
    gates_path: str | None = None,
) -> list[str]:
    """Who is still missing, after agents/policies/gates.yml is applied.

    low → one reviewer from the pool is enough.
    medium / high → every reviewer on every touched scope.
    """
    from .policy import reviewers_mode

    pool = required_reviewers(resolutions)
    mode = reviewers_mode(risk, gates_path)
    if mode == "one":
        if pool & have:
            return []
        return sorted(pool)
    return sorted(pool - have)


def touched_scopes(resolutions: list[Resolution]) -> set[str]:
    return {r.scope.id for r in resolutions}
