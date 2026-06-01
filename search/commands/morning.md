---
description: Morning routine — match Gmail Deals/{slug} labels to deals, digest new email
argument-hint: ""
---

Use the **deal-pipeline** skill to run the morning routine.

Find `Deals/*` Gmail labels, reconcile them against deal folders, pull new threads since each
deal's Last Contact into a dated digest in `{deal}/correspondence/` (digest-only — no confidential
bodies committed), update Last Contact in `pipeline.md`, surface today's deal-related calendar
events, then run `/search:dashboard` and post a summary.
