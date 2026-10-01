# Provisional source

User authorization to skip the golden edition is recorded in ../DECISIONS.md.
The governing electronic text is `../root/001_v2.txt` at legacy commit
`c0a66002a0d51183ac5856ca6dbe4d03ab808d9d`. No physical edition is authenticated.

The old generator inserted ASCII word spaces, `་␣` before detached affixes, and
` ` where original spaces were represented by underscores. Decode in order:
remove ASCII spaces; remove the entire `་␣` sequence; restore ` ` to ASCII space.
Removing only `␣` would leave spurious tshegs inside words.

`scripts/prepare_source.py` verifies all 258 decoded PO entries against stripped
original lines before writing generated entries and the normalization report.
The 382 artificial affix markers, 3,435 tokenizer spaces, and 107 original-space
placeholders are display machinery. Repeated tshegs and unusual spellings still
present in the original transcript are source readings, retained without repair.

Authored: segmentation.json and canonical ../paired/source.md.
Generated: entries.json and normalization-report.json.
Archival files in root/, wip/, and source/originals/ retain their original bytes.
Human-reference translations are preserved separately in translations/.

Legacy Transifex workflow and configuration are archived in source/originals/
under legacy-first_phase.yml, legacy-transifex.yml, and legacy-languages. They
are provenance material; the active workflow is the paired-text build above.
The historical Transifex setup guide is preserved in source/originals/legacy-documentation/; its old relative links describe the archival layout.
