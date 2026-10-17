# Error records

One file per real error that cost time: compile/build, runtime, environment, a wrong assumption, an agent mistake.
Why: (1) when the same symptom returns, `grep -ril "<message or CS code>" docs/ai/errors` finds the cause and fix;
(2) records marked `portable: yes` are distilled into `docs/ai/LESSONS.md` and carried to other projects.

- File name: `YYYY-MM-DD-short-slug.md`.
- Records are history: never rewrite them when the code changes later (paths in them are not checked).
- **Symptom** holds the exact message — it is what the next person will search for.
- **Prevention** is the most valuable field: a check, test or doc rule that now catches the error earlier.
  A lesson that became an automated check transfers to another project as code, not just as advice.
- `check_docs.py` validates the fields and warns while a portable record is not yet in `LESSONS.md`.

Template:

```
---
date: YYYY-MM-DD
area: <directory or subsystem>
kind: code | build | environment | agent | process
tags: [unity, netgen, ...]
portable: yes | no
---
# <symptom in a few words>

**Symptom:** exact error text or observed behaviour.
**Cause:** the root cause, not the trigger.
**Fix:** what changed, with the commit hash.
**Prevention:** the check, test or doc rule that now catches it earlier — or "none" and why.
**Lesson:** one sentence that makes sense outside this project.
```
