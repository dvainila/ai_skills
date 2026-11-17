#!/usr/bin/env python3
"""Heuristic check of Mermaid fences. No renderer, no network."""

from __future__ import annotations

import re
import sys
from pathlib import Path

FENCE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
RESERVED = {
    "end",
    "graph",
    "flowchart",
    "subgraph",
    "class",
    "click",
    "style",
    "classDef",
}
BLOCK_START = re.compile(r"^\s*(subgraph|alt|opt|loop|par|rect|box|critical|break)\b")
KEYWORDS = {
    "flowchart",
    "graph",
    "classDiagram",
    "sequenceDiagram",
    "erDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "architecture-beta",
    "gitGraph",
    "gantt",
    "pie",
    "direction",
    "classDef",
    "class",
    "click",
    "style",
    "linkStyle",
    "participant",
    "actor",
    "Note",
}


def diagrams(text: str, path: Path) -> list[tuple[int, str]]:
    if path.suffix.lower() == ".mmd":
        return [(1, text)]
    found = [(m.start(), m.group(1).strip()) for m in FENCE.finditer(text)]
    return found or ([(1, text)] if text.strip() else [])


def check_balances(src: str) -> list[str]:
    errors: list[str] = []
    depth = 0
    for i, line in enumerate(src.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("%%"):
            continue
        if BLOCK_START.match(stripped):
            depth += 1
        if re.match(r"^\s*end\s*$", stripped):
            depth -= 1
            if depth < 0:
                errors.append(f"L{i}: extra 'end'")
                depth = 0
    if depth > 0:
        errors.append(f"unclosed block (subgraph/alt/loop/…): depth={depth}")
    return errors


def check_ids(src: str) -> list[str]:
    errors: list[str] = []
    is_flow = any(
        line.strip().startswith(("flowchart", "graph"))
        for line in src.lstrip().splitlines()[:5]
    )
    if not is_flow:
        return errors
    for i, line in enumerate(src.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        if s.startswith("subgraph"):
            m = re.match(r"subgraph\s+(\S+)", s)
            if not m:
                continue
            sid = m.group(1)
            if sid.startswith("["):
                continue
            if not re.match(r"^[A-Za-z][\w]*$", sid):
                errors.append(f"L{i}: bad subgraph id '{sid}'")
            continue
        head = re.match(r"^([A-Za-z][\w-]*)", s)
        if not head:
            continue
        tok = head.group(1)
        if tok in KEYWORDS or tok in RESERVED:
            continue
        if "-" in tok:
            errors.append(f"L{i}: id with dash '{tok}' (use underscore)")
    return errors


def check_architecture(src: str) -> list[str]:
    if src.lstrip().startswith("architecture"):
        return ["architecture-beta may not render on GitHub; prefer flowchart"]
    return []


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate.py <file.md|.mmd>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR {path}: not a file")
        return 1
    text = path.read_text(encoding="utf-8")
    blocks = diagrams(text, path)
    if not blocks:
        print(f"ERROR {path}: no mermaid content")
        return 1
    failed = False
    for idx, (_pos, src) in enumerate(blocks, 1):
        prefix = f"{path}#{idx}"
        errs = check_balances(src) + check_ids(src)
        warns = check_architecture(src)
        for e in errs:
            print(f"ERROR {prefix}: {e}")
            failed = True
        for w in warns:
            print(f"WARN {prefix}: {w}")
        if not errs:
            print(f"OK {prefix}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
