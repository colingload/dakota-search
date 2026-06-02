# Dakota Search — Claude Code Plugin

One plugin for the Dakota Strategy acquisition workflow: analyze targets, draft NDAs/LOIs, keep a
pipeline dashboard, and run a morning email routine — from the terminal **or** Claude Cowork.

## Where it sits (HoldCo is split into 4 compartments)

```
holdco/
├── deal-flow/      (1) ACTIVE DEALS — one folder per target + _template + pipeline.md   ← data
├── reference/      (2) LEARNING & REFERENCE — ETA KB, SBA lender materials, LOI/DD guides
├── dashboard/      (3) DASHBOARD — Google Sheet + Apps Script (the deal CRM / pipeline view)
└── dakota-search/   (4) THIS PLUGIN — skills, commands, agent, hooks                       ← code
```

**Code vs. data:** the plugin never stores deal data. It reads/writes the existing `deal-flow/`
tree by path. `pipeline.md` + the deal folders are the source of truth; the dashboard Sheet is a
synced view (push, don't hand-edit).

## Install / activate

This plugin lives in its **own public repo** (`colingload/dakota-search`), separate from the private
`Dakota-Strategy` repo (which holds the consulting work + confidential deal data).

**In Cowork:** Create plugin → Add marketplace → `colingload/dakota-search` → install **search**.

**In Claude Code (local):**
```
/plugin marketplace add colingload/dakota-search
/plugin install search@dakota-search
```
(or point `--plugin-dir` at a local clone of this repo for live editing).

After pushing changes, pull them with **`/plugin marketplace update`** in Cowork (or `/search:publish`
from a local clone to ship). Note: the skills operate on deal data under `holdco/deal-flow/` in your
private repo at runtime — that data is never stored in this public plugin repo.

## Commands

| Command | What it does |
|---|---|
| `/search:new-deal {name}` | New Deal — clone `_template/`, prefill, add a pipeline row, then wait for inbox drops |
| `/search:organize {deal}` | Classify + rename a deal's `inbox/` into cim/financials/correspondence |
| `/search:analyze {deal}` | Financial analysis + risk/operating thesis (rebuild P&L, SDE/EBITDA, DSCR) |
| `/search:report {deal}` | Decision (§12) + executive summary + pipeline update |
| `/search:evaluate {deal}` | Quick independent go/no-go read |
| `/search:nda {deal}` | Draft/sign a buyer-side NDA *(draft — counsel review)* |
| `/search:loi {deal}` | Generate a non-binding LOI draft *(draft — counsel review)* |
| `/search:dashboard` | Refresh `pipeline.md` + push to the Sheet (`--export` for HTML) |
| `/search:morning` | Match Gmail `Deals/{slug}` labels to deals, digest new email |
| `/search:log` | Log the session to `WORKLOG.md` + route detail to its home |
| `/search:publish` | Commit + push this plugin repo so Cowork can `/plugin marketplace update` |

Commands also trigger from natural phrases ("new prospect: …", "run the financial analysis on …",
"draft an LOI for …", "log this") via each skill's description.

## Skills

- **acquisition-analysis** — the analytical brain (PLAYBOOK Steps 0–7). *Complete.*
- **deal-documents** — NDA + LOI generation. *Scaffold.*
- **deal-pipeline** — dashboard sync, HTML export, Gmail/Calendar morning routine. *Scaffold.*
- **session-log** — session-aware "log this". *Working (v1).*

## Agent
- **deal-evaluator** — read-only second-opinion reviewer. *Scaffold.*

## Connectors (account-level, via claude.ai)

The morning routine and dashboard sync use the **Gmail**, **Google Calendar**, and **Google Drive**
connectors. These are configured on your claude.ai account (native in Cowork) — the plugin uses them
but does not bundle them. Gmail label convention: one label per deal, `Deals/{slug}`.

## Session model

Every working session is one of three types — **deal · dashboard · plugin/skill**. State the goal at
the start; run `/search:log` at the end. The log lands in `holdco/WORKLOG.md` (universal journal) and
routes detail to the deal's `discussion-log.md` or the repo `CHANGELOG.md`.

## Build status (v0.1.0 — scaffold)

`acquisition-analysis` is lifted and complete; `session-log` works. `deal-documents`,
`deal-pipeline`, and `deal-evaluator` are scaffolded with full frontmatter + TODOs, to be fleshed
out one per session. See each `SKILL.md` for its TODO list, and the plan at
`.claude/plans/i-want-to-rethink-staged-lynx.md`.
