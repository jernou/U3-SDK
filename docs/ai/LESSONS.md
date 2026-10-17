# Portable lessons

Project-agnostic rules distilled from `docs/ai/errors/` by `/doc-sync`. Kept short (budget ~1 500 tokens) so the
whole file can be copied into another project's `CLAUDE.md` or a personal `~/.claude/CLAUDE.md`.
One rule per line, grouped by topic; each rule links the records that justify it. When a new record confirms
an existing rule, add the link instead of a second rule.

## Working with AI agents

- Agent-written docs are unverified claims: confirm every path and symbol with a script, and check each
  behavioural claim (threads, lifecycle, client/server side) in code before writing it down.
  (`errors/2026-10-17-agent-docs-unverified-facts.md`)
