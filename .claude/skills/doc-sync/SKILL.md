---
name: doc-sync
description: Bring the AI navigation docs up to date in one pass - process docs/ai/INBOX.md, review code drift reported by docs/ai/check_docs.py, distill portable error records into docs/ai/LESSONS.md and keep every doc within its size budget. Use when asked to sync, update or clean the AI docs, or when check_docs.py warns about drift, a full inbox or an undistilled lesson.
---

# Doc sync

Goal: the docs describe the current code, stay within budget, and nothing learned is lost. Work in this order.

1. Run `python3 docs/ai/check_docs.py`. Fix every ERROR first; the WARNING lines are your worklist.
2. **Inbox** (`docs/ai/INBOX.md`). For each line, verify the claim in code, then route it:
   - rule, pattern or pitfall of one directory → that directory's `CLAUDE.md`;
   - structure or "where to look" → `docs/ai/MAP.md`;
   - a real error with a known cause and fix → a new record in `docs/ai/errors/` (template in its `README.md`);
   - nothing a future agent would do differently → drop it.
   Delete every processed line. A line you cannot verify stays, with a note saying what is missing.
3. **Drift** (warning "N commit(s) changed code here"). Run the `git log --stat` command from the warning, open only
   the diffs that touch what the doc states, and rewrite the stale lines. No change needed is a valid outcome.
4. **Lessons.** Every record with `portable: yes` is represented in `docs/ai/LESSONS.md` by one project-agnostic rule
   that links the record. If a rule already covers it, add the link instead of a new rule.
5. **Budgets.** If a doc is over budget, compress: merge lines, delete what no longer changes agent behaviour,
   move detail down into a directory's `CLAUDE.md`.
6. Record the sync: `git rev-parse HEAD > docs/ai/.last-sync` (drift warnings are counted from this commit).
7. Run the checker again — it must report 0 errors — and commit as `docs(ai): sync` with a short summary of what
   moved where.

Editing rules: edit lines in place (add / rewrite / delete); never append "update:" notes or dates; never copy code
or line numbers; write a behavioural claim only after checking it in code.
