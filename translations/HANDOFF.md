# Translation handoff

Read AGENTS.md, PROJECT-STATUS.md and DECISIONS.md first.

## Fixed inputs and scope

- Complete single work: legacy entries 1–258, title through colophon; original PO contexts retained.
- Provisional exception explicitly authorized by user; golden phase skipped.
- Source/reference commit: c0a66002a0d51183ac5856ca6dbe4d03ab808d9d.
- Template commit: f6431c25c7c9fa852c404b8cd3e0e3cdeae1178f.
- Active combined guideline: v2.0, unchanged from template.
- Active glossary: 222 rows, unchanged; SHA-256 6b9029f7f02494e947e6a1273da7916b358e4d0738b35f012ce4da662d3fbbaf.
- Source/English versions: ns-provisional-source-v1 / ns-english-draft-v1.

## Coverage and editorial state

- 258/258 original entries represented; 280 source/English pairs; 0 missing pairs.
- Source comparison: 258/258 exact decoded-to-root matches. 0 source textual emendations.
- 22 entries split at heading/prose/verse boundaries with exact offset/space reconstruction.
- 144 notes at 121 entries remain visible. Source-reading notes: 37; terminology-gap notes: 67; contextual-use notes: 17; syntax/reference notes: 15; interpretive-supply notes: 4; scope notes: 4.
- Entry150 / NS-000150b retains an explicitly unresolved Tibetan predicate; N-150 records exact wording. Do not silently replace it with the rough human English.
- 322 usage records; 139 separate Proposed term/usage worksheet rows. No proposed glossary changes activated.
- Source queries are future evidence work, not proof of corruption and not an undisclosed edition repair.
- Original human translation, root files, and legacy scripts are preserved unchanged.

## Checks and review

- Translators self-checked ranges 1–86,87–172,173–258. Coordinator checked integrated coverage, reading order, cross-range terminology, source-note quotations, role/format classification, and preserved provenance.
- Independent QC: not performed; no human certification.
- Full physical-scan proofreading and exhaustive witness collation: not performed.
- Positive validation passes; 15/15 negative fixtures rejected (validation-report.json).
- Source reconstruction and generated-output reproducibility pass.
- The standard's 30 semantic regression fixtures were not executed as a separate evaluation; do not conflate them with 15 structural corruption tests.

## Publication and continuation

The user explicitly selected a separate repository:
https://github.com/Lotus-King-Translation/Togden-Nangpa-Sangyepa

This repository was generated from the organization template and populated with
the prepared draft. Source work identity and pair IDs remain unchanged.

- Published paired version: v0.1.0-provisional.
- Published source and English tags: ns-provisional-source-v1 and ns-english-draft-v1.
- All three annotated tag objects and peeled commits verified remotely.
- Fixed release commit: b5fe195e9c52209a345f9650ad5d6a981afeaf61.
- Post-tag publication receipt: releases/v0.1.0-provisional.receipt.json.
- Receipt checkpoint verifies remote main and clean working tree without moving tags.

The repository-creation/publication task is complete after the receipt checkpoint.
A subsequent independent semantic QC/human-editing phase would cover all 280
pairs and the 144 recorded review notes; it has not started. Preserve all source
lineage, fixed tags, and pair IDs in any revision.
