#!/usr/bin/env python3
"""Validate the provisional paired-text/2 contract, with corruption tests.

Structural/source validation is not semantic translation certification.
"""
from pathlib import Path
from collections import Counter
import argparse
import copy
import hashlib
import json
import re
import sys
from prepare_source import inputs

ROOT = Path(__file__).resolve().parents[1]
FORMATS = {'prose','verse','h1','h2','h3'}
MARKER = re.compile(r'^<!-- pair: ([A-Za-z0-9-]+)((?: \| [^\n]+)?) -->$', re.M)
END = '<!-- end-pairs -->'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def parse(text, source):
    require(text.startswith('---\n'), 'missing front matter')
    end = text.find('\n---\n', 4)
    require(end >= 0, 'unterminated front matter')
    fm = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(':')
        require(sep and key not in fm, 'invalid/duplicate front matter field')
        fm[key] = value.strip()
    require(text.count(END) == 1, 'missing/duplicate end-pairs marker')
    body, footer = text[end+5:].split(END)
    matches = list(MARKER.finditer(body))
    require(matches and not body[:matches[0].start()].strip(), 'unpaired prefix content')
    require(body.count('<!-- pair:') == len(matches), 'malformed pair marker')
    rows, seen = [], set()
    for i, m in enumerate(matches):
        ident = m[1]
        require(ident not in seen, 'duplicate pair ID')
        seen.add(ident)
        meta = {}
        for piece in m[2].split('|'):
            if not piece.strip():
                continue
            key, sep, value = piece.strip().partition(':')
            require(sep and key not in meta, 'invalid/duplicate pair metadata')
            meta[key] = value.strip()
        if source:
            require(set(meta) == {'source','role','format'}, 'source metadata fields')
            require(meta['format'] in FORMATS, 'unsupported format')
        else:
            require(not meta, 'translation must inherit format; no duplicate metadata')
        stop = matches[i+1].start() if i+1 < len(matches) else len(body)
        content = body[m.end():stop].strip()
        require(content and '<!--' not in content, 'empty/malformed pair content')
        rows.append(dict(id=ident,meta=meta,body=content))
    return fm, rows, footer


def unheading(body, fmt):
    if fmt.startswith('h'):
        prefix = '#' * int(fmt[1]) + ' '
        require(body.startswith(prefix), 'missing heading syntax')
        return body[len(prefix):]
    require(not body.startswith('#'), 'undeclared heading in body')
    return body


def validate(source, translation, entries, segments, notes, manifest):
    sf, sr, sx = parse(source, True)
    tf, tr, tx = parse(translation, False)
    require(not sx.strip(), 'unexpected source footer')
    expected_source = dict(schema='paired-text/2', **{'text-id':'Nangpa-Sangyepa', 'edition':'ns-provisional-source-v1','language':'bo','source-status':'provisional'})
    for key,value in expected_source.items():
        require(sf.get(key)==value, 'source front matter mismatch: '+key)
    for key,value in {'schema':'paired-text/2','text-id':'Nangpa-Sangyepa','source-edition':sf['edition'],'translation-edition':'ns-english-draft-v1','language':'en','status':'annotated-working-draft'}.items():
        require(tf.get(key)==value, 'translation front matter mismatch: '+key)
    require([r['id'] for r in sr] == [r['id'] for r in tr], 'source/translation IDs or order differ')
    require([r['id'] for r in sr] == [s['pair_id'] for s in segments], 'segmentation/pair order differs')
    require(len(entries)==258 and [e['index'] for e in entries]==list(range(1,259)), 'entry coverage')
    require(len({s['source_id'] for s in segments})==len(segments), 'duplicate source object')
    last_entry, position, entry_counts = 1, 0, Counter()
    for s, r, t in zip(segments,sr,tr):
        i = s['entry_index']
        require(i in {last_entry,last_entry+1}, 'source order/omission')
        if i != last_entry:
            require(position==len(entries[last_entry-1]['text']), 'lost previous entry tail')
            last_entry, position = i, 0
        text = entries[i-1]['text']
        require(s['start']==position and s['end']>s['start'] and s['end']<=len(text), 'source range gap/overlap')
        require(r['meta']=={'source':s['source_id'],'role':s['role'],'format':s['format']}, 'source metadata differs from frozen segmentation')
        require(unheading(r['body'],s['format'])==text[s['start']:s['end']], 'source text differs from pinned transcript')
        unheading(t['body'],s['format'])
        separator = s['separator_after']
        require(separator in {'',' '}, 'unsupported split separator')
        require(text[s['end']:s['end']+len(separator)]==separator, 'split separator mismatch')
        position = s['end']+len(separator)
        entry_counts[i]+=1
    require(last_entry==258 and position==len(entries[-1]['text']) and len(entry_counts)==258, 'lost final/source entries')
    require(segments[-1]['role']=='work_colophon', 'lost work colophon')
    require(segments[0]['format']=='h1', 'lost title')
    # Known mixed prose/verse boundaries must survive segmentation, not merely metadata.
    for i,formats in {28:['prose','verse'],30:['verse','prose'],35:['verse','prose'],112:['prose','verse']}.items():
        require([s['format'] for s in segments if s['entry_index']==i]==formats, f'format boundary crossed at entry {i}')
    ids = [n['id'] for n in notes]
    require(len(ids)==len(set(ids)), 'duplicate note ID')
    refs = set(re.findall(r'\[\^([^\]]+)\]', '\n'.join(r['body'] for r in tr)))
    defs = re.findall(r'^\[\^([^\]]+)\]: ',tx,re.M)
    require(len(defs)==len(set(defs)) and refs==set(defs)==set(ids), 'missing/orphan/duplicate notes')
    for n in notes:
        require(n['entry_index'] in entry_counts, 'note entry outside source')
        require(n['exact_tibetan'] and n['exact_tibetan'] in entries[n['entry_index']-1]['text'], 'note quotation not exact source')
        for field in ['category','problem','working_treatment','uncertainty','review_action']:
            require(n.get(field), 'incomplete note: '+field)
        require(n['id'] in tx and n['exact_tibetan'] in tx, 'note footer lacks exact source')
    hashes = manifest.get('canonical_sha256',{})
    for path, content in [('paired/source.md',source),('paired/translation.md',translation)]:
        require(hashlib.sha256(content.encode()).hexdigest()==hashes.get(path), 'canonical manifest hash mismatch: '+path)
    return dict(entries=258,pairs=len(sr),formats=dict(sorted(Counter(s['format'] for s in segments).items())),notes=len(notes),colophon='retained',source_edition=sf['edition'],translation_edition=tf['translation-edition'])


def load():
    entries, reference, report = inputs()
    for name, expected in [('source/entries.json',entries),('translations/human-reference.json',reference),('source/normalization-report.json',report)]:
        require(json.loads((ROOT/name).read_text())==expected,'generated input mismatch: '+name)
    manifest=json.loads((ROOT/'paired/manifest.json').read_text())
    for path,digest in {**manifest['fixed_input_sha256'], **manifest['canonical_sha256']}.items():
        require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'fixed input hash mismatch: '+path)
    return [(ROOT/'paired/source.md').read_text(),(ROOT/'paired/translation.md').read_text(),entries,json.loads((ROOT/'source/segmentation.json').read_text()),json.loads((ROOT/'translations/notes.json').read_text()),manifest]


def negative_tests(data):
    cases=[]
    def case(name,change):
        changed=copy.deepcopy(data); change(changed); cases.append((name,changed))
    case('missing source format',lambda d:d.__setitem__(0,d[0].replace(' | format: h1','',1)))
    case('unsupported format',lambda d:d.__setitem__(0,d[0].replace('format: h1','format: bad',1)))
    case('wrong source edition',lambda d:d.__setitem__(1,d[1].replace('source-edition: ns-provisional-source-v1','source-edition: unset',1)))
    case('empty English',lambda d:d.__setitem__(1,re.sub(r'(<!-- pair: [^>]+ -->)\n\n.*?(?=\n\n<!--)',r'\1',d[1],count=1,flags=re.S)))
    case('duplicate pair',lambda d:d.__setitem__(1,d[1].replace('<!-- end-pairs -->','<!-- pair: NS-000001 -->\n\nDuplicate\n\n<!-- end-pairs -->',1)))
    case('source mutation',lambda d:d.__setitem__(0,d[0].replace('ནང་པ་','ནང་པའ་',1)))
    case('unknown source object',lambda d:d.__setitem__(0,d[0].replace('source: L00001','source: UNKNOWN',1)))
    case('missing translation pair',lambda d:d.__setitem__(1,re.sub(r'<!-- pair: [^>]+ -->.*?(?=<!-- pair:)', '',d[1],count=1,flags=re.S)))
    case('duplicate format metadata',lambda d:d.__setitem__(0,d[0].replace('format: h1','format: h1 | format: h1',1)))
    case('translation format metadata',lambda d:d.__setitem__(1,d[1].replace('<!-- pair: NS-000001 -->','<!-- pair: NS-000001 | format: h1 -->',1)))
    case('missing source tail',lambda d:d[3].pop())
    case('source overlap',lambda d:d[3][1].__setitem__('start',1))
    case('missing note definition',lambda d:d.__setitem__(1,re.sub(r'^\[\^[^\]]+\]: .*\n?', '',d[1],count=1,flags=re.M)))
    case('changed English',lambda d:d.__setitem__(1,d[1].replace('<!-- end-pairs -->','extra unauthorized translation\n\n<!-- end-pairs -->',1)))
    case('lost mixed format boundary',lambda d:next(s for s in d[3] if s['entry_index']==28 and s['format']=='verse').__setitem__('format','prose'))
    passed=[]
    for name, changed in cases:
        try:
            validate(*changed)
        except (ValueError,KeyError):
            passed.append(name)
        else:
            raise ValueError('negative fixture accepted: '+name)
    return passed


def main():
    p=argparse.ArgumentParser();p.add_argument('--negative-tests',action='store_true');args=p.parse_args()
    data=load();result=validate(*data)
    if args.negative_tests:
        result['negative_tests_rejected']=negative_tests(data)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try: main()
    except (OSError,ValueError,KeyError) as exc:
        print('PAIRED VALIDATION FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
