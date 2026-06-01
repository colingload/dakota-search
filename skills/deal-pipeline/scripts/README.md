# deal-pipeline / scripts

**TODO (build session):** `build_dashboard.py` — parse `holdco/deal-flow/pipeline.md` (markdown
table) + glob `holdco/deal-flow/*/README.md` (+ §12 of `analysis.md`), fill
`../templates/dashboard.template.html`, write `holdco/deal-flow/dashboard.html`. Deterministic,
idempotent, no token cost.

Also (dashboard sync): `sync_api.gs` `doPost` upsert lives with the Sheet at
`holdco/dashboard/sheets/appscript/`, not here. This script only builds the local HTML snapshot.

**No-Python fallback (Cowork):** the `deal-pipeline` skill does the same parse/fill in-model when
Python is unavailable.
