# Inbox — notes waiting for /doc-sync

Append one line per observation while you work; don't stop the task to edit docs for it.
Format: `- YYYY-MM-DD · <area or path> · <what you noticed and why it matters>`

Not for this file: a moved/renamed path or entry point (fix `MAP.md` / `CLAUDE.md` in the same commit) and a real
error you fixed (write a record in `docs/ai/errors/`). `/doc-sync` moves each line into the right doc or drops it,
then deletes it here — this file is a queue, not a history.

- 2026-10-17 · Assets/**/CLAUDE.md.meta · Written by hand, without Unity. After the first Unity import run `git status`: if Unity rewrote them, commit Unity's version.
- 2026-10-17 · Unturned/Throwables · `Grenade.cs` says modders use these scripts on their prefabs, so the ModHooks rules (no renames of classes/serialized fields) apply. Give it its own CLAUDE.md if work happens there.
