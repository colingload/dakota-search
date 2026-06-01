---
description: Publish plugin changes — commit + push holdco/dakota-search to GitHub (main) so Cowork can update
argument-hint: "(optional commit message)"
---

Publish the Dakota Search plugin so Cowork can pull the update. Run from the repo (local Claude Code).

Steps:
1. Stage **only** the plugin + marketplace:
   `git add holdco/dakota-search .claude-plugin/marketplace.json`
2. Show the staged file list and **verify none are confidential**: reject real seller data
   (`*/cim/`, `*/financials/`, `*/correspondence/`, `*/inbox/` with actual files, tax returns, bank
   statements, PFS, resume). The plugin's own **blank template assets** are expected and fine
   (`assets/financials-side-by-side.template.html`, `assets/folder-stubs/*/README.md`).
3. Commit with the message in `$ARGUMENTS` (or "Update Dakota Search plugin" if empty), ending with:
   `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
4. Push to `origin main`.
5. Remind the user: in **Cowork**, run `/plugin marketplace update` to pull the new version.

Do NOT stage or commit anything outside the plugin + `marketplace.json` — leave deal data and all
other repo changes untouched.
