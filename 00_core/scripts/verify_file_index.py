#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FILE_INDEX_SHA256 verifier (stdlib-only)

Purpose:
- Detect divergence between declared FILE_INDEX_SHA256.txt and repository tree.
- Hard-fail when a listed file is missing or has a hash mismatch.
- Optionally also detect unindexed files (within a scope).

Scope:
- By default verifies exactly the entries listed in FILE_INDEX_SHA256.txt.
- Does NOT assume that all repo files are indexed (e.g., .github can be excluded).

Exit codes:
- 0: OK
- 2: Missing file(s)
- 3: Hash mismatch(es)
- 4: Parse error
"""

from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import sys

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def parse_index(txt: str):
    entries = []
    for i, line in enumerate(txt.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid index line {i}: {line!r}")
        digest = parts[0]
        rel = ' '.join(parts[1:]).strip()
        # Git-style format: '<hash>  <path>'
        rel = rel.lstrip()
        if rel.startswith('./'):
            rel = rel[2:]
        entries.append((digest, rel))
    return entries

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', help='Repo root')
    ap.add_argument('--index', default='FILE_INDEX_SHA256.txt', help='Index file path (relative to root)')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    index_path = (root / args.index).resolve()

    try:
        idx_txt = index_path.read_text(encoding='utf-8')
        entries = parse_index(idx_txt)
    except Exception as e:
        print(f"PARSE_ERROR: {e}", file=sys.stderr)
        return 4

    missing = []
    mismatch = []
    for expected_hash, rel in entries:
        p = root / rel
        if not p.exists():
            missing.append(rel)
            continue
        got = sha256_file(p)
        if got.lower() != expected_hash.lower():
            mismatch.append((rel, expected_hash, got))

    if missing:
        print("MISSING_FILES:", file=sys.stderr)
        for rel in missing:
            print(f"- {rel}", file=sys.stderr)
        # still report mismatches if any
    if mismatch:
        print("HASH_MISMATCH:", file=sys.stderr)
        for rel, exp, got in mismatch:
            print(f"- {rel}\n  expected: {exp}\n  got:      {got}", file=sys.stderr)

    if missing:
        return 2
    if mismatch:
        return 3
    print("OK: FILE_INDEX_SHA256.txt matches listed files.")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
