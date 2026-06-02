# deal-documents / templates

Tokenized document templates filled per-deal by the `deal-documents` skill.

- `loi.template.html` — non-binding LOI (clean HTML → PDF). **Done** — filled section-by-section
  by `/search:loi`; Purchase Price pulls from the deal's locked Offer Value. See the skill's LOI spec.
- `nda.template.html` — buyer-side mutual NDA (HTML → PDF). **TODO** — author fresh;
  no clean source exists.

Tokens use `{{UPPER_SNAKE}}` placeholders; unknown values render as `[CONFIRM]`.
