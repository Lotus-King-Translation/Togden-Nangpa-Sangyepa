# Project-owner decisions

## 2026-10-01 — Provisional translation, golden phase waived

The user explicitly requested the new Tibetan repository template, instructed us to skip the golden-edition phase and translate the entire text, and supplied the existing Nangpa-Sangyepa `wip/` human translation as reference. This authorizes a provisional source exception to AGENTS.md §2. It does not establish a corrected golden edition or approve new glossary entries.

The Tibetan PO strings are formatting derivatives of `root/001_v2.txt`; reverse only the documented tokenizer display operations. Preserve source spellings, punctuation, duplicate tshegs, and uncertain readings. Record any interpretive repair in translation notes. The human English is a reference, not an authority over the Tibetan or glossary.

## Implementation decisions (coordinator; not terminology approvals)

- Pin legacy inputs to `c0a66002a0d51183ac5856ca6dbe4d03ab808d9d` and template to `f6431c25c7c9fa852c404b8cd3e0e3cdeae1178f`.
- Bound this run to the complete single work: 258 original PO entries, title through colophon. Preserve legacy `msgctxt` and line-number provenance.
- Use stable source objects `L00001`–`L00258`; assign `NS-` pair identities before assembly. Source-side `source:` references explicitly identify provisional objects, never golden objects.
- No physical witness was supplied. No scan proofreading, golden edition, or exhaustive witness collation is claimed.
- Keep the template's 222-row glossary unchanged. Local proposals remain Proposed.
- Initial destination ambiguity resolved by the explicit owner decision below.

## 2026-10-01 — Separate repository authorized

The user instructed: “Separate, name it Togden-Nangpa-Sangyepa.” Create
`Lotus-King-Translation/Togden-Nangpa-Sangyepa` directly from
`Lotus-King-Translation/tibetan-text-project-template`, publish the prepared
whole-work provisional draft there, and retain the reference repository as the
archival source. Repository naming does not change the work identity
`Nangpa-Sangyepa`, source/English edition identifiers, or stable `NS-` pair IDs.
This decision resolves the publication destination; it does not approve open
source readings, terminology proposals, or final human translation status.
