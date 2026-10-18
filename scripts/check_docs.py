#!/usr/bin/env python3
"""Validate repository-local Markdown links and documentation SVG integrity."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
HTML_ATTR_RE = re.compile(r"""<(?:a|img|source|link)\b[^>]*?\b(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
FENCED_BLOCK_RE = re.compile(r"(?ms)^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n.*?^[ \t]{0,3}\1[ \t]*$")
SVG_NS = "{http://www.w3.org/2000/svg}"


def markdown_files() -> list[Path]:
    files = set(ROOT.glob("*.md"))
    docs = ROOT / "docs"
    if docs.exists():
        files.update(docs.rglob("*.md"))
    return sorted(files)


def referenced_local_paths(markdown_path: Path) -> list[tuple[str, str]]:
    source = FENCED_BLOCK_RE.sub("", markdown_path.read_text(encoding="utf-8"))
    references = []
    for match in MARKDOWN_LINK_RE.finditer(source):
        references.append((match.group(1) or match.group(2), "Markdown link/image"))
    for match in HTML_ATTR_RE.finditer(source):
        references.append((match.group(1), "HTML href/src"))
    return references


def check_local_references() -> tuple[int, list[str]]:
    checked = 0
    errors: list[str] = []
    for markdown_path in markdown_files():
        for target, kind in referenced_local_paths(markdown_path):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith("//"):
                continue
            if not parsed.path:
                continue

            raw_path = unquote(parsed.path)
            candidate = (
                ROOT / raw_path.lstrip("/")
                if raw_path.startswith("/")
                else markdown_path.parent / raw_path
            ).resolve()
            checked += 1
            source = markdown_path.relative_to(ROOT)
            if not candidate.is_relative_to(ROOT):
                errors.append(f"{source}: {kind} escapes repository: {target}")
            elif not candidate.exists():
                errors.append(f"{source}: broken {kind}: {target}")
    return checked, errors


def check_svg_files() -> tuple[int, list[str]]:
    svg_files = sorted((ROOT / "docs").rglob("*.svg"))
    errors: list[str] = []
    for svg_path in svg_files:
        try:
            root = ET.parse(svg_path).getroot()
            if root.tag != f"{SVG_NS}svg":
                errors.append(f"{svg_path.relative_to(ROOT)}: root element is not SVG")
                continue
            if not (root.get("viewBox") or (root.get("width") and root.get("height"))):
                errors.append(f"{svg_path.relative_to(ROOT)}: missing viewBox or explicit dimensions")
            if svg_path.name != "logo.svg":
                text_count = len(root.findall(f".//{SVG_NS}text"))
                if text_count < 3:
                    errors.append(
                        f"{svg_path.relative_to(ROOT)}: illustration may be blank or incomplete "
                        f"({text_count} text elements; at least 3 expected)"
                    )
        except (ET.ParseError, OSError) as exc:
            errors.append(f"{svg_path.relative_to(ROOT)}: invalid SVG/XML: {exc}")
    return len(svg_files), errors


def main() -> int:
    link_count, link_errors = check_local_references()
    svg_count, svg_errors = check_svg_files()
    errors = link_errors + svg_errors

    print(f"Checked {link_count} local Markdown/HTML references.")
    print(f"Parsed {svg_count} SVG files for XML validity and non-empty illustration content.")
    if errors:
        print("Documentation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
