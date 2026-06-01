---
description: Publish plugin changes — commit + push this repo so Cowork can update
argument-hint: "(optional commit message)"
---

Publish the Dakota Search plugin so Cowork can pull the update. Run from a local clone of the
`colingload/dakota-search` repo.

Steps:
1. Stage all plugin changes in this repo: `git add -A`
2. Show the staged file list and **verify none are confidential**: this repo holds plugin code only
   (commands, skills, templates, the SBA python model). Reject any real seller data
   (`*/cim/`, `*/financials/`, `*/correspondence/`, `*/inbox/` with actual files, tax returns, bank
   statements, PFS, resume). The plugin's own **blank template assets** are expected and fine
   (`skills/acquisition-analysis/assets/financials-side-by-side.template.html`, `assets/folder-stubs/*/README.md`).
3. Commit with the message in `$ARGUMENTS` (or "Update Dakota Search plugin" if empty), ending with:
   `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
4. Push: `git push origin main`
5. Remind the user: in **Cowork**, run `/plugin marketplace update` to pull the new version.
