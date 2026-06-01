---
name: deal-pipeline
description: >-
  Maintain the deal pipeline view and the email/calendar connectors. Use when the user says
  "refresh the dashboard", "update the pipeline", "sync deals to the sheet", "export the
  dashboard", "run the morning routine", or "check deal email". Regenerates pipeline.md,
  pushes each deal row to the Google Sheet dashboard, optionally exports a Dakota-branded
  dashboard.html, and runs the Gmail/Calendar morning routine that matches Deals/{slug} labels
  to deal folders (digest-only). Source of truth is the local files (pipeline.md + deal folders);
  the Sheet is a synced view.
---

# Deal Pipeline — dashboard sync, export & morning routine

> ⚠️ **SCAFFOLD — not yet fully implemented.** Trigger is live; sync/export/routine logic is
> TODO. If invoked now, explain the intended behavior and offer to build it.

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

### `/search:morning` — Gmail/Calendar morning routine (digest-only)
Label convention: one Gmail label per deal, `Deals/{slug}` (slug = folder name minus date prefix).
1. `list_labels` → find `Deals/*`; reconcile against deal folders; offer `create_label` for gaps.
2. Per matched label: `search_threads` newer than that deal's Last Contact → `get_thread` →
   write a **digest** (paraphrase + thread link) to `{deal}/correspondence/email-digest-{date}.md`.
   Do NOT store full confidential bodies/attachments in the repo.
3. Update Last Contact in `pipeline.md`; surface today's deal-related calendar events.
4. End by running `/search:dashboard` and posting a chat digest.

## TODO (build session)
- [ ] Dashboard: re-title the Sheet (SBA → Deal), add `sync_api.gs` `doPost`, deploy Web App,
      store URL + shared token in plugin config (`userConfig`).
- [ ] `scripts/build_dashboard.py` — parse `pipeline.md` + glob deal READMEs → fill the template.
- [ ] `templates/dashboard.template.html` — model on
      `business-strategy/playbooks/gtm-audit/templates/audit_report.html` (token + repeating-card
      pattern) with Dakota branding from
      `holdco/dakota-search/skills/acquisition-analysis/assets/financials-side-by-side.template.html`.
- [ ] Implement the Gmail/Calendar morning routine; create `Deals/{slug}` labels for current deals.
- [ ] No-script fallback (Cowork): if Python is unavailable, do the parse/fill in-model.
