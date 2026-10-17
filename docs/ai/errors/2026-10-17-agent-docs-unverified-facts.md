---
date: 2026-10-17
area: docs/ai, Assets/**/CLAUDE.md
kind: agent
tags: [docs, verification, hallucination]
portable: yes
---
# Agent-written navigation docs contained wrong facts

**Symptom:** The first version of the docs had statements that were false in code: path `UI/Menu/MenuPauseUI.cs`
(real: `Unturned/UI/Menu/MenuPauseUI.cs`); "`PopulateAsset` runs on a worker thread" (main thread, called from
`Assets.LoadFile`); "`LevelManager` handles arena/horde" (arena only); "manager methods early-return on clients"
(most don't check `Provider.isServer`); "`InvokeAndLoopback` … listen server" (Unturned has no listen server);
`PlayConfigData` named as a class (it is only a file name; classes are `ConfigData`, `ModeConfigData`).
**Cause:** Facts were inferred from file names, folder structure and general Unity knowledge and written down
before being checked in code; the path and class name were never checked against the file system.
**Fix:** 7de1c78 corrected the path (caught by `check_docs.py`) and the threading/arena claims (read the code);
the follow-up commit that added this record corrected the rest after reading `BarricadeManager.cs`,
`ClientMethodHandle.cs` and `Provider.cs`.
**Prevention:** `docs/ai/check_docs.py` fails on missing paths, missing `.cs` files and identifiers that occur
nowhere in code (the `PlayConfigData` mistake was caught this way). Root `CLAUDE.md` rule: behavioural claims
(threads, lifecycle, server/client side) go into docs only after they were checked in code.
**Lesson:** Treat agent-written documentation as unverified until a script confirms every path and symbol exists
and each behavioural claim was checked against the code; the mechanical check costs seconds and catches the
most frequent class of mistakes.
