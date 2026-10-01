# Togden-Nangpa-Sangyepa

**Dispelling the Darkness of the Mental Faculty: Instruction on Going for Refuge,
the Foundation of All the Paths of All Buddhist Practitioners**

A complete annotated English working translation of the Tibetan text, prepared
under the Lotus-King-Translation template and its 222-entry glossary.
The colophon attributes the work to Dharma lord Toktrul Thubten Tenpe Gyaltsen and dates
it to 1983. These are statements of the supplied transcript, not independently
authenticated bibliographic facts.

## Read the text

- [Tibetan source](paired/source.md)
- [English working translation and notes](paired/translation.md)
- [Bilingual reading view](paired/bilingual.md)
- [Current status](PROJECT-STATUS.md) and [translation handoff](translations/HANDOFF.md)

The user expressly waived the golden-edition phase. The source is therefore a
**provisional electronic transcript**, not a corrected critical or golden edition.
The previous human English translation is preserved as reference; the new draft
is governed by the Tibetan and the template glossary. Uncertain readings and
proposed terminology remain visible for human editing.

## Provenance and standards

- [Source register](editions/REGISTER.csv) and [normalization method](source/README.md)
- [Owner decisions and scope](DECISIONS.md)
- [Translation standard v2.0](guidelines/tibetan_translation_standard_v2.md)
- [Active glossary](glossary/expanded_tibetan_english_glossary.csv)
- [Paired-text format and provisional exception](FORMAT.md)
- [Annotations](translations/notes.json), [usage records](translations/usage.json),
  and [proposed additions](translations/proposed-glossary.csv)

Legacy inputs come from [Nangpa-Sangyepa at the pinned commit](https://github.com/Lotus-King-Translation/Nangpa-Sangyepa/tree/c0a66002a0d51183ac5856ca6dbe4d03ab808d9d);
this separate repository was generated from the [organization template](https://github.com/Lotus-King-Translation/tibetan-text-project-template/tree/f6431c25c7c9fa852c404b8cd3e0e3cdeae1178f).
The original `root/`, `wip/`, and processing scripts remain available.
The human-reference PO credits Inga Pogosyan (2023), Tenzin Norgyal (2024), and
Mikko Kotila (2024). Its [original README notice](source/originals/legacy-README.md)
is preserved.

## Reproduce and validate

Python 3, standard library only:

```sh
python3 scripts/prepare_source.py
python3 scripts/build_views.py
python3 scripts/validate_paired.py --negative-tests
```

`paired/source.md` and `paired/translation.md` are canonical authored content.
`source/segmentation.json`, `translations/notes.json`, and `translations/usage.json`
are authored support records. The normalized entries, human-reference projection,
coverage, manifest, and bilingual view are generated. Validation confirms
structure and preservation; it does not certify semantic accuracy.

Contributors and agents must read [AGENTS.md](AGENTS.md) first.
