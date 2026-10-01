#!/usr/bin/env python3
"""Rebuild derived views/coverage/manifest from canonical paired files.

Canonical authored: paired/source.md, paired/translation.md,
source/segmentation.json, translations/notes.json, translations/usage.json.
Run validate_paired.py after regeneration; this command is not source validation.
"""
from pathlib import Path
import hashlib
import json
from collections import Counter
from validate_paired import parse,unheading

ROOT=Path(__file__).resolve().parents[1]

def write(path,data):
    (ROOT/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def main():
    source=(ROOT/'paired/source.md').read_text()
    translation=(ROOT/'paired/translation.md').read_text()
    sf,sr,_=parse(source,True);tf,tr,footer=parse(translation,False)
    segments=json.loads((ROOT/'source/segmentation.json').read_text())
    notes=json.loads((ROOT/'translations/notes.json').read_text())
    by_entry={i:[n['id'] for n in notes if n['entry_index']==i] for i in range(1,259)}
    coverage=[]
    out=['# Nangpa-Sangyepa — Tibetan and English working draft','',
        'Generated from canonical paired/source.md and paired/translation.md by scripts/build_views.py.',
        'Provisional electronic source; golden phase waived. Source-linked notes flag readings and terminology for review.','']
    for s,t,seg in zip(sr,tr,segments):
        if s['id']!=t['id'] or s['id']!=seg['pair_id']:
            raise ValueError('pair order mismatch before building')
        fmt=s['meta']['format'];en=unheading(t['body'],fmt);bo=unheading(s['body'],fmt)
        out.extend([f"<!-- {s['id']} | legacy entry {seg['entry_index']} -->",''])
        if fmt.startswith('h'):
            out.extend(['#'*int(fmt[1])+' '+en,'',bo,''])
        else:
            out.extend([bo,'',en,''])
        coverage.append(dict(pair_id=s['id'],source_object=s['meta']['source'],legacy_entry=seg['entry_index'],
            format=fmt,role=seg['role'],represented=True,notes=by_entry[seg['entry_index']],
            review_status='review-flagged' if by_entry[seg['entry_index']] else 'drafted-self-checked'))
    out.extend(['---','',footer.strip(),''])
    (ROOT/'paired/bilingual.md').write_text('\n'.join(out),encoding='utf-8')
    write('paired/coverage.json',coverage)
    fixed=['root/001.txt','root/001_v2.txt','wip/bo/001.po','wip/en/001.po','scripts/sentences_to_transifex.py',
        'glossary/expanded_tibetan_english_glossary.csv','guidelines/tibetan_translation_standard_v2.md',
        'source/entries.json','source/segmentation.json']
    manifest=dict(schema='paired-text/2',text_id='Nangpa-Sangyepa',
        source_edition=sf['edition'],source_status='provisional',translation_edition=tf['translation-edition'],
        legacy_commit='c0a66002a0d51183ac5856ca6dbe4d03ab808d9d',template_commit='f6431c25c7c9fa852c404b8cd3e0e3cdeae1178f',
        entry_count=258,pair_count=len(sr),format_counts=dict(sorted(Counter(s['meta']['format'] for s in sr).items())),
        note_count=len(notes),entries_with_notes=sum(bool(x) for x in by_entry.values()),
        independent_qc=False,full_scan_proofreading=False,exhaustive_collation=False,
        canonical_sha256={p:sha(p) for p in ['paired/source.md','paired/translation.md','translations/notes.json','translations/usage.json']},
        fixed_input_sha256={p:sha(p) for p in fixed})
    write('paired/manifest.json',manifest)
    print(f'Generated bilingual view and coverage for {len(sr)} pairs / 258 entries.')

if __name__=='__main__': main()
