#!/usr/bin/env python3
"""Checks that the AI-agent docs (CLAUDE.md files, AGENTS.md, docs/ai/*.md) are not stale.

1. Every path written in `backticks` (containing "/") must exist. A path is resolved against
   the repo root, the doc's own directory and Assets/Runtime/Assembly-CSharp; "*" globs are allowed.
2. Every CLAUDE.md under Assets/ must have a .meta file (Unity requirement).
3. Every directory with its own CLAUDE.md must be listed in docs/ai/MAP.md.

Usage: python3 docs/ai/check_docs.py   (exit code 1 on problems)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = ROOT / "Assets" / "Runtime" / "Assembly-CSharp"
MAP = ROOT / "docs" / "ai" / "MAP.md"

INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
PATH_LIKE = re.compile(r"^[A-Za-z0-9_.\-*/]+$")


def doc_files():
	files = [ROOT / "CLAUDE.md", ROOT / "AGENTS.md"]
	files += sorted((ROOT / "docs" / "ai").glob("*.md"))
	files += sorted(p for p in ROOT.rglob("CLAUDE.md") if ".git" not in p.parts and p != ROOT / "CLAUDE.md")
	return [f for f in files if f.exists()]


def exists(token, doc_dir):
	for base in (ROOT, doc_dir, CODE_ROOT):
		if "*" in token:
			if any(base.glob(token)):
				return True
		elif (base / token).exists():
			return True
	return False


def main():
	problems = []

	for doc in doc_files():
		text = FENCE.sub("", doc.read_text(encoding="utf-8"))
		for token in INLINE_CODE.findall(text):
			token = token.strip()
			if "/" not in token or token.startswith("/") or not PATH_LIKE.match(token):
				continue
			if not exists(token.rstrip("/"), doc.parent):
				problems.append(f"{doc.relative_to(ROOT)}: path not found: {token}")

	map_text = MAP.read_text(encoding="utf-8") if MAP.exists() else ""
	for doc in ROOT.rglob("CLAUDE.md"):
		if ".git" in doc.parts or doc.parent == ROOT:
			continue
		rel = doc.relative_to(ROOT)
		if rel.parts[0] == "Assets" and not Path(str(doc) + ".meta").exists():
			problems.append(f"{rel}: missing .meta file")
		folder = doc.parent
		names = {folder.relative_to(ROOT).as_posix()}
		if CODE_ROOT in folder.parents:
			names.add(folder.relative_to(CODE_ROOT).as_posix())
		if not any(f"`{n}`" in map_text or f"`{n}/" in map_text for n in names):
			problems.append(f"{rel}: directory is not listed in docs/ai/MAP.md")

	for p in problems:
		print(p)
	print(f"{len(problems)} problem(s)" if problems else "AI docs OK")
	return 1 if problems else 0


if __name__ == "__main__":
	sys.exit(main())
