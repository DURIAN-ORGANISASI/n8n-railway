#!/usr/bin/env python3
"""Regenerate or verify FILE-MANIFEST.json using only the Python standard library."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "FILE-MANIFEST.json"
EXCLUDED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "backups"}
EXCLUDED_NAMES = {".DS_Store", "Thumbs.db"}
EXCLUDED_SUFFIXES = {".pyc", ".dump", ".sql", ".log", ".sqlite", ".sqlite3"}


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if relative.as_posix() == "FILE-MANIFEST.json":
        return False
    if path.name in EXCLUDED_NAMES or path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if path.name == ".env":
        return False
    if path.name.startswith(".env.") and path.name != ".env.example":
        return False
    return True


def build_manifest() -> list[dict[str, str | int]]:
    entries = []
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and included(p)):
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return entries


def main() -> int:
    expected = json.dumps(build_manifest(), indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        try:
            current = MANIFEST_PATH.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Cannot read FILE-MANIFEST.json: {exc}", file=sys.stderr)
            return 1
        if current != expected:
            print("FILE-MANIFEST.json is stale. Run: python scripts/update-manifest.py", file=sys.stderr)
            return 1
        print("FILE-MANIFEST.json is up to date.")
        return 0

    MANIFEST_PATH.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Updated FILE-MANIFEST.json with {len(build_manifest())} file entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
