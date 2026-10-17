#!/usr/bin/env python3
"""Mechanical checks for the AI-agent docs (how the docs work: docs/ai/README.md).

Errors (exit code 1):
  paths     every `dir/file` path written in backticks exists (globs allowed)
  files     every `Name.cs` written in backticks exists somewhere under Assets/
  symbols   every `Identifier` or `Type.member` written in backticks occurs in some .cs file (agent docs only)
  meta      every CLAUDE.md under Assets/ has a .meta file (Unity)
  coverage  every code "shelf" (child of SHELF_PARENTS) and every directory with a CLAUDE.md is listed in MAP.md
  budgets   docs stay within their size budget (tokens ~ chars / 4)
  records   files in docs/ai/errors/ follow the template
Warnings (exit code 0):
  drift     code in a directory changed after its CLAUDE.md was last updated (or after the last /doc-sync)
  inbox     docs/ai/INBOX.md has many unprocessed entries
  lessons   an error record marked portable is not linked from docs/ai/LESSONS.md

Usage: python3 docs/ai/check_docs.py
"""
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "Assets"
CODE_ROOT = ASSETS / "Runtime" / "Assembly-CSharp"
AI = ROOT / "docs" / "ai"
MAP = AI / "MAP.md"
INBOX = AI / "INBOX.md"
LESSONS = AI / "LESSONS.md"
ERRORS = AI / "errors"
LAST_SYNC = AI / ".last-sync"
HUMAN_DOCS = {AI / "README.md"}  # prose for people: only paths are checked, not identifiers

# Every directory directly inside these that contains .cs files is a "shelf" and must be listed in MAP.md.
SHELF_PARENTS = ["Assets", "Assets/Runtime", "Assets/Editor", "Assets/Runtime/Assembly-CSharp",
	"Assets/Runtime/Assembly-CSharp/Unturned", "Assets/Runtime/Assembly-CSharp/Framework"]
# Size budgets in approximate tokens (chars / 4). The root CLAUDE.md is loaded into every session.
BUDGETS = {"CLAUDE.md": 1600, "docs/ai/MAP.md": 4000, "docs/ai/LESSONS.md": 1500}
NESTED_BUDGET = 1000
INBOX_LIMIT = 10
RECORD_FIELDS = ["date:", "area:", "kind:", "portable:",
	"**Symptom:**", "**Cause:**", "**Fix:**", "**Prevention:**", "**Lesson:**"]

INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
PATH_LIKE = re.compile(r"^[A-Za-z0-9_.\-*/]+$")
SYMBOL_LIKE = re.compile(r"^[A-Za-z_]\w*(?:\(\))?(?:\.[A-Za-z_]\w*(?:\(\))?)*$")
FILE_LIKE = re.compile(r"\.(?:cs|md|json|dat|asmdef|meta|unity|txt|py|yml|log|dll|module)$")
IDENTIFIER = re.compile(r"[A-Za-z_]\w*")
IN_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"

errors = []
warnings = []


def rel(path):
	return path.relative_to(ROOT).as_posix()


def nested_docs():
	return sorted(ASSETS.rglob("CLAUDE.md"))


def is_path(token):
	return "/" in token and PATH_LIKE.match(token) and not token.startswith(("/", "."))


def reference_docs():
	"""Docs whose backticked references must match the current code (records and the inbox are history/notes)."""
	docs = [ROOT / "CLAUDE.md", ROOT / "AGENTS.md", MAP, AI / "README.md"]
	docs += sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
	return [doc for doc in docs + nested_docs() if doc.exists()]


def tokens(doc):
	text = FENCE.sub("", doc.read_text(encoding="utf-8"))
	return [token.strip() for token in INLINE_CODE.findall(text)]


def resolve(token, doc_dir):
	"""Existing paths a token can mean: relative to the repo root, the doc's directory or CODE_ROOT."""
	found = []
	for base in (ROOT, doc_dir, CODE_ROOT):
		if "*" in token:
			found += base.glob(token)
		elif (base / token).exists():
			found.append(base / token)
	return found


def code_index():
	"""Identifiers and file names of all C# sources under Assets/."""
	identifiers, names = set(), set()
	for path in ASSETS.rglob("*.cs"):
		names.add(path.name)
		identifiers.update(IDENTIFIER.findall(path.read_text(encoding="utf-8", errors="replace")))
	return identifiers, names


def check_references(identifiers, cs_names):
	for doc in reference_docs():
		for token in tokens(doc):
			where = f"{rel(doc)}: `{token}`"
			if token.startswith("."):
				continue  # an extension such as `.meta`
			if "/" in token:
				if is_path(token) and not resolve(token.rstrip("/"), doc.parent):
					errors.append(f"{where} - path not found")
			elif PATH_LIKE.match(token) and resolve(token, doc.parent):
				continue  # a bare directory or file name such as `NetMessaging`
			elif token.endswith(".cs") and PATH_LIKE.match(token):
				if not any(fnmatch.fnmatchcase(name, token) for name in cs_names):
					errors.append(f"{where} - no such .cs file")
			elif doc not in HUMAN_DOCS and SYMBOL_LIKE.match(token) and not FILE_LIKE.search(token) and "Foo" not in token:
				missing = [name for name in IDENTIFIER.findall(token) if name not in identifiers]
				if missing:
					errors.append(f"{where} - not found in code: {', '.join(missing)}")
	if LESSONS.exists():  # lessons are project-agnostic: only their links to error records are checked
		for token in tokens(LESSONS):
			if is_path(token) and not resolve(token.rstrip("/"), LESSONS.parent):
				errors.append(f"{rel(LESSONS)}: `{token}` - path not found")


def check_meta_and_coverage():
	for doc in nested_docs():
		if not Path(f"{doc}.meta").exists():
			errors.append(f"{rel(doc)} - missing .meta file (Unity)")
	listed = set()
	for token in tokens(MAP):
		if PATH_LIKE.match(token) and not token.startswith("/"):
			listed.update(path.resolve() for path in resolve(token.rstrip("/"), MAP.parent))
	shelves = [child for parent in SHELF_PARENTS for child in sorted((ROOT / parent).iterdir())
		if child.is_dir() and any(child.rglob("*.cs"))]
	for folder in shelves + [doc.parent for doc in nested_docs()]:
		folder = folder.resolve()
		if not any(path == folder or folder in path.parents for path in listed):
			errors.append(f"{rel(folder)} - not listed in docs/ai/MAP.md")


def check_budgets():
	budgets = {ROOT / name: limit for name, limit in BUDGETS.items()}
	budgets.update({doc: NESTED_BUDGET for doc in nested_docs()})
	for doc, limit in budgets.items():
		if doc.exists():
			size = len(doc.read_text(encoding="utf-8")) // 4
			if size > limit:
				errors.append(f"{rel(doc)} - ~{size} tokens, budget {limit}: compress it (/doc-sync, step 5)")


def check_records():
	lessons = LESSONS.read_text(encoding="utf-8") if LESSONS.exists() else ""
	for record in sorted(ERRORS.glob("*.md")):
		if record.name == "README.md":
			continue
		text = record.read_text(encoding="utf-8")
		if not re.match(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$", record.name):
			errors.append(f"{rel(record)} - name must be YYYY-MM-DD-short-slug.md")
		missing = [field for field in RECORD_FIELDS if field not in text]
		if missing:
			errors.append(f"{rel(record)} - missing fields: {', '.join(missing)}")
		if re.search(r"^portable:\s*yes\b", text, re.MULTILINE) and record.name not in lessons:
			warnings.append(f"{rel(record)} - portable lesson is not in docs/ai/LESSONS.md yet")


def check_inbox():
	if INBOX.exists():
		count = len(re.findall(r"^- \d{4}-\d{2}-\d{2}", INBOX.read_text(encoding="utf-8"), re.MULTILINE))
		if count >= INBOX_LIMIT:
			warnings.append(f"docs/ai/INBOX.md - {count} unprocessed entries: run /doc-sync")


def git(*args):
	try:
		result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
	except OSError:
		return None
	return result.stdout.strip() if result.returncode == 0 else None


def check_drift():
	if git("rev-parse", "HEAD") is None:
		return  # not a git checkout
	synced = LAST_SYNC.read_text(encoding="utf-8").strip() if LAST_SYNC.exists() else None
	if synced and git("cat-file", "-e", f"{synced}^{{commit}}") is None:
		synced = None
	for doc in nested_docs():
		base = git("log", "-1", "--format=%H", "--", rel(doc))
		if not base:
			continue  # doc is not committed yet
		if synced and git("merge-base", "--is-ancestor", base, synced) is not None:
			base = synced
		folder = rel(doc.parent)
		count = git("rev-list", "--count", f"{base}..HEAD", "--", folder, ":(exclude,glob)**/CLAUDE.md*")
		if count and int(count):
			warnings.append(f"{rel(doc)} - {count} commit(s) changed code here since the doc was updated or synced; "
				f"review: git log --stat {base[:8]}..HEAD -- {folder}")


def main():
	sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles and redirects default to a legacy code page
	identifiers, cs_names = code_index()
	check_references(identifiers, cs_names)
	check_meta_and_coverage()
	check_budgets()
	check_records()
	check_inbox()
	check_drift()
	found = {"error": list(dict.fromkeys(errors)), "warning": list(dict.fromkeys(warnings))}  # repeated tokens once
	for kind, items in found.items():
		for item in items:
			print(f"::{kind}::{item}" if IN_ACTIONS else f"{kind.upper()}: {item}")
	root_size = len((ROOT / "CLAUDE.md").read_text(encoding="utf-8")) // 4
	print(f"{len(found['error'])} error(s), {len(found['warning'])} warning(s). "
		f"Root CLAUDE.md ~{root_size} tokens (loaded every session).")
	return 1 if found["error"] else 0


if __name__ == "__main__":
	sys.exit(main())
