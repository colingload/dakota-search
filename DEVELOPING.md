# Developing the Dakota Search plugin

How to update skills / improve the plugin. **GitHub (`colingload/dakota-search`) is the single
source of truth. Edit in one place, push, everything else pulls.**

## Setup (once)
- Open both repos together: open **`dakota.code-workspace`** (multi-root: this plugin repo +
  `dakota-strategy` which holds the deal data). You build the plugin here and test against real
  deals next door.
- Local Claude Code, point at this repo:
  ```
  /plugin marketplace remove dakota-strategy        # clear the old (now-deleted) source
  /plugin marketplace add colingload/dakota-search
  /plugin install search@dakota-search
  ```
  (Power option for instant local edits without pushing: launch with
  `claude --plugin-dir <path>/dakota-search/search`, then `/reload-plugins` after each edit.)

## The loop — improving one skill per session
1. **Open the workspace**, focus on the one skill: `search/skills/<skill-name>/`.
2. **Edit** its `SKILL.md` (the method) + bundle what it needs into its own `references/`,
   `templates/`, `scripts/`. Source material from `dakota-strategy/holdco/reference/` and real
   deals from `dakota-strategy/holdco/deal-flow/` — but **copy/distill it INTO the skill** (see rule).
3. **Test** against a real deal (run from the `dakota-strategy` side where `holdco/deal-flow/` lives).
4. **Ship:** `/search:publish` (commit + push this repo).
5. **In Cowork:** `/plugin marketplace update` to pull the new version.

## The one rule: skills must be self-contained
In **Cowork only this plugin repo exists** — the main repo's `reference/` and `deal-flow/` are NOT
there. So everything a skill needs (templates, distilled guides, scripts) must live **inside the
skill folder** and travel with the plugin. The only outside thing a skill touches at runtime is the
specific deal folder it's pointed at (`holdco/deal-flow/{deal}/`). Never have a skill read a file
that only exists in the private repo.

## Don't edit in two places
If you edit directly in Cowork, that copy can diverge from GitHub. Pick one edit surface (local is
recommended — git + deal data are here), push, and let the other pull. Never edit local and Cowork
in the same change without pulling first.
