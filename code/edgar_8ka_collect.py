#!/usr/bin/env python3
"""EDGAR 8-K/A collector+joiner (design v2 after DeepSeek pre-mortem, run-218).
Downloads full-index master.gz for 2025Q1..2026Q3, extracts 8-K / 8-K/A rows,
joins each amendment to its nearest-preceding base 8-K by CIK within a 15-business-day
window (72h treated as recall floor), records filer-prefix match flag and dedupes
A->A chains. Output: data/edgar-8ka-pairs.json (JSONL rows). Descriptive UA mandatory.
"""
import urllib.request, gzip, json, os, collections
from datetime import datetime, timedelta

UA = 'Pennyforge research studio penny.forge.99@gmail.com'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'data/edgar-8ka-pairs.jsonl')
QUARTERS = ['2025/QTR1','2025/QTR2','2025/QTR3','2025/QTR4','2026/QTR1','2026/QTR2','2026/QTR3']

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=120).read()

def bus_days(d1, d2):
    """business days from d1 back to d2 (d1 >= d2), excluding Sat/Sun."""
    n, d = 0, d1
    while d > d2:
        d -= timedelta(days=1)
        if d.weekday() < 5: n += 1
    return n

rows_8k = []      # (cik, date, accession, name)
rows_8ka = []
for q in QUARTERS:
    url = f'https://www.sec.gov/Archives/edgar/full-index/{q}/master.gz'
    raw = fetch(url)
    lines = gzip.decompress(raw).decode('utf-8', 'replace').splitlines()
    n8, nka = 0, 0
    for l in lines:
        if '|' not in l: continue
        p = l.split('|')
        if len(p) < 5: continue
        cik, name, form, date, fn = p[0].strip(), p[1].strip(), p[2].strip(), p[3].strip(), p[4].strip()
        if form == '8-K':
            rows_8k.append((cik, date, fn, name)); n8 += 1
        elif form == '8-K/A':
            rows_8ka.append((cik, date, fn, name)); nka += 1
    print(f'{q}: 8-K {n8} | 8-K/A {nka}', flush=True)

by_cik = collections.defaultdict(list)
for cik, date, fn, name in rows_8k:
    try: by_cik[cik].append((datetime.strptime(date, '%Y-%m-%d').date(), fn))
    except ValueError: pass
for cik in by_cik: by_cik[cik].sort(reverse=True)

BUS_WINDOW = 15  # business days (pre-mortem: 72h is recall floor, 10-15 bus days is the honest window)
pairs = []
orphan = 0
for cik, date, fn, name in rows_8ka:
    try: d = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError: continue
    am_acc = fn.split('/')[-1].replace('.txt', '')
    am_prefix = '-'.join(am_acc.split('-')[:1])  # first dash segment = filer/agent id
    cands = [(bd, bfn) for (bd, bfn) in by_cik.get(cik, []) if bd <= d]
    if not cands:
        orphan += 1; continue
    base = None
    for bd, bfn in cands:  # cands sorted newest-first: first = nearest preceding
        base = (bd, bfn); break
    gap_bus = bus_days(d, base[0])
    base_acc = base[1].split('/')[-1].replace('.txt', '')
    prefix_match = ('-'.join(base_acc.split('-')[:1]) == am_prefix)
    pair = {
        'amend_cik': cik, 'company': name, 'amend_date': str(d), 'amend_accession': am_acc,
        'base_date': str(base[0]), 'base_accession': base_acc,
        'gap_bus_days': gap_bus, 'gap_cal_days': (d - base[0]).days,
        'filer_prefix_match': prefix_match, 'window': '15bd',
        'within_72h': (d - base[0]).days <= 3,
    }
    pairs.append(pair)

json.dump(pairs, open(OUT.replace('.jsonl', '.json'), 'w'))
with open(OUT, 'w') as f:
    for p in pairs: f.write(json.dumps(p) + '\n')
gaps = sorted(p['gap_bus_days'] for p in pairs)
import statistics
print(f'\namendments {len(rows_8ka)} | paired {len(pairs)} | no-base-in-history {orphan}')
print(f'gap business-days: median {statistics.median(gaps)} | p75 {gaps[int(len(gaps)*.75)]} | p95 {gaps[int(len(gaps)*.95)]}')
print(f'within 72h: {sum(1 for p in pairs if p["within_72h"])} ({100*sum(1 for p in pairs if p["within_72h"])/len(pairs):.0f}%) | filer-prefix match: {sum(1 for p in pairs if p["filer_prefix_match"])} ({100*sum(1 for p in pairs if p["filer_prefix_match"])/len(pairs):.0f}%)')
