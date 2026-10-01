#!/usr/bin/env python3
"""Decode the legacy PO display layer; never emend Tibetan text.

Authored inputs: archived root/001_v2.txt and wip/{bo,en}/001.po.
Generated: source/entries.json, translations/human-reference.json,
source/normalization-report.json. No third-party dependencies.
"""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
LEGACY_COMMIT = 'c0a66002a0d51183ac5856ca6dbe4d03ab808d9d'
PINNED_SHA256 = {
    'root/001.txt': 'e4fbc38aad658b35eacf1ecafd1bf568947e6f2dfce55f0edde11f1d4039e2cb',
    'root/001_v2.txt': 'e4fbc38aad658b35eacf1ecafd1bf568947e6f2dfce55f0edde11f1d4039e2cb',
    'wip/bo/001.po': '2746024c6cd9005db1c11286ceca1c64f7890277853df1aa8c2330e6aa983309',
    'wip/en/001.po': 'c2926accd73052bbb23c5b3f8c4774ab682cc8ee56ec8db3c10740eaeb195753',
    'scripts/sentences_to_transifex.py': '1942eb5446ff73bfaf326cc478205daec970a8d9ff3ccd862f79d6e95f5f583e',
    'glossary/expanded_tibetan_english_glossary.csv': '6b9029f7f02494e947e6a1273da7916b358e4d0738b35f012ce4da662d3fbbaf',
    'guidelines/tibetan_translation_standard_v2.md': '934f54616d1c55a6ecb0c594108397cca5b317dafc7c2c945972ffd1351b7760',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_po(path):
    result, row, field = [], {}, None
    for line in path.read_text(encoding='utf-8').splitlines() + ['']:
        if not line:
            if row.get('msgctxt'):
                result.append(row)
            row, field = {}, None
        elif line.startswith('#'):
            continue
        elif line.startswith(('msgctxt ', 'msgid ', 'msgstr ')):
            field, value = line.split(' ', 1)
            if field in row:
                raise ValueError('duplicate PO field')
            row[field] = ast.literal_eval(value)
        elif line.startswith('"') and field:
            row[field] += ast.literal_eval(line)
        else:
            raise ValueError('unsupported PO syntax: ' + line)
    contexts = [r['msgctxt'] for r in result]
    if len(contexts) != len(set(contexts)):
        raise ValueError('duplicate legacy context')
    return result

def decode(text):
    # Order matters: remove tokenizer ASCII spaces before restoring source spaces.
    # Remove the WHOLE injected tsheg + visible-space sequence to rejoin affixes.
    return text.replace(' ', '').replace('་␣', '').replace(' ', ' ')

def inputs():
    for path, expected in PINNED_SHA256.items():
        if sha(ROOT/path) != expected:
            raise ValueError('archived/template input differs from pinned commit: ' + path)
    bo = read_po(ROOT / 'wip/bo/001.po')
    en = read_po(ROOT / 'wip/en/001.po')
    lines = (ROOT / 'root/001_v2.txt').read_text(encoding='utf-8').splitlines()
    if len(bo) != 258 or len(en) != 258 or len(lines) != 258:
        raise ValueError('legacy input must contain exactly 258 entries')
    entries, reference = [], []
    for i, (b, e, line) in enumerate(zip(bo, en, lines), 1):
        if b['msgctxt'] != e['msgctxt'] or b['msgid'] != e['msgid']:
            raise ValueError(f'BO/EN source mismatch at {i}')
        clean = decode(b['msgid'])
        if clean != line.strip():
            raise ValueError(f'decode differs from archived root line {i}')
        if any(c in clean for c in '␣ _'):
            raise ValueError(f'leftover display marker at {i}')
        entries.append(dict(id=f'L{i:05}',index=i,context=b['msgctxt'],text=clean))
        reference.append(dict(index=i,context=e['msgctxt'],translation=e['msgstr']))
    report = dict(legacy_commit=LEGACY_COMMIT,entries=258,matched_root_lines=258,
        mismatches=0,tokenizer_ascii_spaces_removed=sum(r['msgid'].count(' ') for r in bo),
        artificial_affix_markers_removed=sum(r['msgid'].count('་␣') for r in bo),
        source_spaces_restored=sum(r['msgid'].count(' ') for r in bo),
        source_textual_emendations=0,unicode_normalization=False,
        line_edge_whitespace='strip per legacy generator; original bytes preserved',
        input_sha256={p:sha(ROOT/p) for p in ['root/001.txt','root/001_v2.txt','wip/bo/001.po','wip/en/001.po','scripts/sentences_to_transifex.py']})
    return entries, reference, report

def main():
    entries, reference, report = inputs()
    for path, data in [('source/entries.json',entries),('translations/human-reference.json',reference),('source/normalization-report.json',report)]:
        (ROOT/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Decoded 258/258 entries; exact archived-line agreement; no source emendations.')

if __name__ == '__main__':
    main()
