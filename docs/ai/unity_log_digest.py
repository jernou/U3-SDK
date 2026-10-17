#!/usr/bin/env python3
"""Condense a Unity Editor.log into unique compile errors, exceptions and warning counts,
small enough to paste to an agent or to quote in a docs/ai/errors record.

Usage: python3 docs/ai/unity_log_digest.py [path/to/Editor.log]
Without a path the default Editor.log location of the current OS is used.
"""
import os
import re
import sys
from collections import Counter
from pathlib import Path

COMPILE = re.compile(r"^\s*(?P<file>[^\s(][^(]*\.cs)\((?P<line>\d+),\d+\): (?P<severity>error|warning) (?P<code>CS\d+): (?P<message>.+?)\s*$")
EXCEPTION = re.compile(r"^(?P<type>[A-Za-z_][\w.]*Exception)(?:: (?P<message>.*))?$")
OWN_FRAME = re.compile(r"SDG\.|Assets/")
MAX_ITEMS = 30
MAX_TEXT = 200


def default_log():
	if sys.platform.startswith("win"):
		return Path(os.environ.get("LOCALAPPDATA", "")) / "Unity" / "Editor" / "Editor.log"
	if sys.platform == "darwin":
		return Path.home() / "Library" / "Logs" / "Unity" / "Editor.log"
	return Path.home() / ".config" / "unity3d" / "Editor.log"


def short(text):
	return text if len(text) <= MAX_TEXT else text[:MAX_TEXT] + "…"


def digest(lines):
	compile_errors = Counter()
	warnings = Counter()
	warning_example = {}
	exceptions = Counter()
	for index, line in enumerate(lines):
		match = COMPILE.match(line)
		if match:
			where = f"{match['file']}:{match['line']}"
			if match["severity"] == "error":
				compile_errors[f"`{where}` {match['code']} {short(match['message'])}"] += 1
			else:
				warnings[match["code"]] += 1
				warning_example.setdefault(match["code"], f"`{where}` {short(match['message'])}")
			continue
		match = EXCEPTION.match(line.strip())
		if match:
			frames = []
			for frame in lines[index + 1:index + 15]:
				if not frame.strip():
					break
				frames.append(re.sub(r"^at ", "", frame.strip()))
			location = next((f for f in frames if OWN_FRAME.search(f)), frames[0] if frames else "(no stack trace)")
			exceptions[f"{short(line.strip())}\n  at {short(location)}"] += 1
	return compile_errors, exceptions, warnings, warning_example


def main():
	sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles and redirects default to a legacy code page
	path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_log()
	if not path.exists():
		print(f"Log not found: {path}")
		return 1
	lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
	compile_errors, exceptions, warnings, warning_example = digest(lines)
	print(f"# Unity log digest: {path.name} ({len(lines)} lines)\n")
	print(f"## Compile errors: {len(compile_errors)} unique")
	for text, count in compile_errors.most_common(MAX_ITEMS):
		print(f"- {text}" + (f" (×{count})" if count > 1 else ""))
	print(f"\n## Exceptions: {len(exceptions)} unique")
	for text, count in exceptions.most_common(MAX_ITEMS):
		head, location = text.split("\n", 1)
		print(f"- {head}" + (f" (×{count})" if count > 1 else "") + f"\n{location}")
	print(f"\n## Compiler warnings: {sum(warnings.values())} total, by code")
	for code, count in warnings.most_common(MAX_ITEMS):
		print(f"- {code} ×{count}, e.g. {warning_example[code]}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
