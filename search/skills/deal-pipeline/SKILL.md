---
name: deal-pipeline
description: >-
  Maintain the deal pipeline view and the Gmail/Calendar connectors. Use when the user says
  "refresh the dashboard", "update the pipeline", "sync deals to the sheet", "export the
  dashboard", "run the gmail routine", "pull deal email", or "check deal email". Regenerates
  pipeline.md, pushes each deal row to the Google Sheet dashboard, optionally exports a
  Dakota-branded dashboard.html, and runs the Gmail/Calendar routine that matches each deal to its
  closest Gmail label — pulling email to backfill missing data points, refresh each deal's
  communication timeline, and catalog attachments. Source of truth is the local files
  (pipeline.md + deal folders); the Sheet is a synced view.
---

# Deal Pipeline — dashboard sync, export & Gmail routine

> ⚠️ **PARTIAL.** The **Gmail/Calendar routine runs in-model now** — it just drives the connected
> Gmail/Calendar MCP, so no extra code is needed. **Dashboard sync + HTML export are still TODO**
> (they need the Apps Script endpoint + `build_dashboard.py`); if those are invoked, explain and
> offer to build.

## Source-of-truth rule
`holdco/deal-flow/pipeline.md` is canonical for the roster; each `{deal}/` folder is canonical for
depth. The Google Sheet is a **one-way synced view** — change deals through the skills/commands,
not by hand-editing the Sheet.

## Intended behavior

### `/search:dashboard` — refresh + push (optional `--export`)
1. Re-read `holdco/deal-flow/pipeline.md` and each `{deal}/README.md` (+ §12 of `analysis.md`).
2. Regenerate `pipeline.md` cleanly (consistent columns, sorted by phase then fit score).
3. Push each deal row to the dashboard Sheet via the Apps Script Web App endpoint
   (`holdco/dashboard/sheets/appscript/sync_api.gs`, `doPost` upsert keyed on slug).
4. With `--export`: render a Dakota-branded `holdco/deal-flow/dashboard.html` snapshot.

### `/search:gmail [deal]` — Gmail/Calendar routine
Pull deal email into the deal folder. With a `{deal}` arg, deep-pull that one deal; omit it to sweep
all deals. Label convention (ideal): one Gmail label per deal, `Deals/{slug}` — but in practice match
the **closest label by name** (see step 1), since the user's labels won't always follow the convention.
Use `get_thread` with `FULL_CONTENT` (returns `plaintext_body` + `attachment_ids`).
1. `list_labels` → pick the label that best matches the deal (not just an exact `Deals/{slug}`):
   normalize names — lowercase, strip the `YYYY-MM-DD-` date prefix, treat `-`, spaces, and `/` as
   equal — then fuzzy-match the deal slug **or** company name against each label's display name
   (nested like `Deals/CW Flooring` or top-level like `CW Flooring`). Take the best hit; if several
   are plausible, ask which; if none, offer `create_label` for `Deals/{slug}`. Keep the matched
   label's **ID** — `search_threads` filters by label ID, not display name.
2. Per matched label: `search_threads` newer than that deal's Last Contact → `get_thread`, then:
   - **Backfill data points.** Fill blank Headline Terms in `{deal}/README.md` (asking price, SDE,
     industry, broker, listing link, etc.) and move answered items in `{deal}/questions.md`
     Open → Answered (source = email date/subject). Propose + flag; append, never overwrite.
   - **Refresh the timeline.** Upsert `{deal}/correspondence/email-timeline.md` — one row per
     message (date, from→to, subject, key points, commitments, follow-ups, thread link).
     Paraphrase; do NOT store full confidential bodies.
   - **Catalog attachments.** List every attachment (filename, email date, thread link) under
     "Docs to pull" in the timeline. The Gmail tools expose attachment names/IDs but cannot
     download bytes — the user drops files into `{deal}/inbox/`, then runs `/search:organize`.
3. Update Last Contact in `pipeline.md`; surface today's deal-related calendar events.
4. **Post a report** of exactly what changed so the user can eyeball it: per deal — label matched
   (+ how confident), # threads/emails parsed, data points backfilled (`field: value` `[flagged]`),
   questions moved Open → Answered, timeline rows added, and attachments queued in "Docs to pull".
   For a full sweep, give a per-deal digest plus a roll-up line. (The file edits themselves also show
   as diffs in-session, so nothing is written invisibly.) Dashboard sync is still TODO.

#### Modes & cadence
- **One deal:** `/search:gmail {deal}` — match + pull that deal only (manual, on demand).
- **Sweep all:** `/search:gmail` (no arg) — `list_labels` once, match every deal folder to its
  closest label, process each, then post a per-deal digest. This is the "each morning" routine.
- **On a schedule:** point the user's scheduler (Cowork scheduled task / Claude Code `/schedule`) at
  the no-arg sweep to run every morning. Caveat: an unattended run only works if the Gmail/Calendar
  connector is available in that run context — verify once in Cowork, since interactively
  authenticated connectors can be absent in headless/cron runs.

## TODO (build session)
- [ ] Dashboard: re-title the Sheet (SBA → Deal), add `sync_api.gs` `doPost`, deploy Web App,
      store URL + shared token in plugin config (`userConfig`).
- [ ] `scripts/build_dashboard.py` — parse `pipeline.md` + glob deal READMEs → fill the template.
- [ ] `templates/dashboard.template.html` — model on
      `business-strategy/playbooks/gtm-audit/templates/audit_report.html` (token + repeating-card
      pattern) with Dakota branding from
      `holdco/dakota-search/skills/acquisition-analysis/assets/financials-side-by-side.template.html`.
- [x] Gmail/Calendar routine — executable in-model now (fuzzy label→deal match, data-point backfill,
      timeline upsert, attachment catalog; no auto-download — the Gmail MCP exposes `attachment_ids`
      but has no get-attachment tool). Setup remaining: create `Deals/{slug}` labels for current
      deals and verify live in Cowork.
- [ ] No-script fallback (Cowork): if Python is unavailable, do the parse/fill in-model.
