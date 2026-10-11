#!/usr/bin/env python3
"""Flag item-4.02 (non-reliance) language in EDGAR 8-K/A full submissions.
One fetch per amendment full-submission txt (header + all docs), grep language.
Resumable: appends JSONL rows, skips amendments already flagged. Gentle 0.35s sleep.
"""
import urllib.request, json, os, re, time, sys

UA = 'Pennyforge research studio penny.forge.99@gmail.com'
HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = os.path.join(HERE, 'data/edgar-8ka-pairs.json')
OUT = os.path.join(HERE, 'data/edgar-8ka-flags.jsonl')

pairs = json.load(open(PAIRS))
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        try: done.add(json.loads(l)['amend_accession'])
        except Exception: pass
todo = [p for p in pairs if p['amend_accession'] not in done]
print(f'{len(pairs)} pairs | {len(done)} already flagged | {len(todo)} to do', flush=True)

PAT = {
    'non_reliance': re.compile(r'non[- ]reliance|no longer be relied', re.I),
    'item_402': re.compile(r'item\s*4\.02', re.I),
    'auditor_change': re.compile(r'changing independent auditor|dismiss(?:ed|al) of (?:the )?auditor|resign(?:ed|ation) of (?:the )?auditor', re.I),
    'restatement': re.compile(r'restat(?:e|ement|ing)', re.I),
    'material_weakness': re.compile(r'material weakness', re.I),
}
ok, err = 0, 0
out = open(OUT, 'a', buffering=1)
for i, p in enumerate(todo):
    acc, cik = p['amend_accession'], p['amend_cik']
    url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{acc}.txt'
    row = {'amend_accession': acc, 'amend_cik': cik, 'company': p['company'], 'amend_date': p['amend_date'],
           'gap_bus_days': p['gap_bus_days'], 'filer_prefix_match': p['filer_prefix_match'],
           'within_72h': p['within_72h'], 'base_accession': p['base_accession']}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        raw = urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'replace')
        # strip SGML header before text matching (header itself names forms, not language)
        body = raw.split('</SEC-HEADER>', 1)[-1]
        for k, pat in PAT.items(): row[k] = bool(pat.search(body))
        row['bytes'] = len(raw)
        ok += 1
    except Exception as e:
        row['error'] = str(e)[:80]
        err += 1
    out.write(json.dumps(row) + '\n')
    if (i + 1) % 100 == 0: print(f'{i+1}/{len(todo)}', flush=True)
    time.sleep(0.35)
out.close()
print(f'done: ok {ok} err {err}', flush=True)
