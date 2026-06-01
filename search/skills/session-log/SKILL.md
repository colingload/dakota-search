---
name: session-log
description: >-
  Log what a working session accomplished. Use when the user says "log", "log this",
  "log the session", "wrap up", or "end of session". Session-aware: determine whether the
  session was deal work, dashboard work, or plugin/skill work, append a dated newest-first
  entry to holdco/WORKLOG.md, and route the detail to the right home — a deal's
  discussion-log.md for deal sessions, or the repo CHANGELOG.md for code/plugin changes.
---

# Session Log — "log this"

This skill is functional in v1 (it only appends markdown — no external dependencies). It keeps a
single, universal history of everything done across the three kinds of work.

## Step 1 — Determine the session type
Infer from what the conversation actually did (ask only if genuinely unclear):
1. **Deal work** — created/analyzed a deal, drafted an NDA/LOI, answered diligence (touched files
   under `holdco/deal-flow/{deal}/`).
2. **Dashboard work** — changed `holdco/dashboard/` (Sheet/Apps Script/templates).
3. **Plugin/skill work** — changed `holdco/dakota-search/` (skills, commands, agents, hooks). Note
   the specific skill if the session focused on one.

## Step 2 — Always append to `holdco/WORKLOG.md`
Prepend a new entry directly under the `<!-- New entries -->` marker (newest first):

```
## {YYYY-MM-DD} · {Deal | Dashboard | Plugin} — {one-line goal}
- **Goal:** what this session set out to do
- **Did:** the substantive things accomplished (decisions, numbers, files created/changed)
- **Next:** concrete next steps
- **Links:** [file](relative/path) references
```

Use today's date (`YYYY-MM-DD`). Keep it substantive; skip ephemeral chatter.

## Step 3 — Route the detail to its home (no duplication)
- **Deal session** → also append substantive findings to `holdco/deal-flow/{deal}/discussion-log.md`
  (newest first, the deal's deep record). The WORKLOG entry links to it; don't repeat the depth.
- **Dashboard / plugin session with code changes** → add a dated bullet to the repo `CHANGELOG.md`.
- **Skill-specific work** → if useful, a short note in that skill's folder.

## Conventions
- Newest entry on top in both WORKLOG.md and discussion-log.md.
- Append-only — never rewrite prior entries.
- Dates `YYYY-MM-DD`.

## TODO (refine later)
- [ ] Optional `holdco/.session.md` scratch holding the session's declared goal for this skill to
      read and clear (only if the user wants explicit session framing).
