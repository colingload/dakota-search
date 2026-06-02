---
description: Gmail routine — pull deal email, backfill data points, refresh the comms timeline, catalog attachments
argument-hint: "[deal]"
---

Use the **deal-pipeline** skill to run the Gmail routine for: **$ARGUMENTS** (omit to sweep all deals).

Find the Gmail label that best matches the deal — the `Deals/{slug}` convention if present, else the
closest label by company name or slug (case-insensitive, ignoring the date prefix; nested or
top-level). If several fit, ask which; if none, offer to create `Deals/{slug}`. Then pull new threads
since Last Contact and:

- **Backfill missing data points** — fill blank Headline Terms in `{deal}/README.md` (asking price,
  SDE, industry, broker, listing link, etc.) and move answered items in `{deal}/questions.md` from
  Open → Answered (source = email date/subject). Propose + flag values; append, never overwrite.
- **Refresh the timeline** — upsert `{deal}/correspondence/email-timeline.md`, one row per message
  (date, from→to, subject, key points, commitments, follow-ups, thread link). Paraphrase — do NOT
  store full confidential bodies.
- **Catalog attachments** — list every attachment (filename, email date, thread link) under "Docs to
  pull" in the timeline. The Gmail tools expose attachment names/IDs but **cannot download bytes** —
  drop the files into `{deal}/inbox/` yourself, then run `/search:organize {deal}` to sort + rename.

Update Last Contact in `pipeline.md` and surface today's deal-related calendar events. Then **post a
report** of exactly what happened — per deal: the label matched, # emails parsed, data points
backfilled (`field: value`, marked `[flagged]`), questions moved to Answered, timeline rows added,
and attachments queued to pull. (Dashboard sync is still TODO.)

**Modes:** pass a deal (`/search:gmail acme-flooring`) to run one; omit the arg (`/search:gmail`) to
sweep every deal each morning. See the skill's "Modes & cadence" for scheduling.
