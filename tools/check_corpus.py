#!/usr/bin/env python3
"""Consistency checks over corpus/*.md (see AUDIT-2026-10-24.md).

  python3 tools/check_corpus.py [corpus] [--json out.json] [--file NAME]

Prints one line per file with every non-zero count, then the totals. Run before each commit: a change should lower
the counts it targets and raise none.
"""
import collections, glob, json, os, re, sys

args = [a for a in sys.argv[1:]]
opt = {}
for k in ('--json', '--file'):
    if k in args:
        i = args.index(k); opt[k] = args[i + 1]; del args[i:i + 2]
ROOT = args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'corpus')

MK = re.compile(r'\[(?:p\.|scan|PDF)\s+[^\]]+\]')
OWN = re.compile(r'\[(?:p\.|scan|PDF)\s+[^\]]+\]')
EN = set('the of and to in is that it which for as with be by this not are from or but on an his have was its we they their has so what all one may can'.split())
OTHER = set('der die das und ist nicht zu den von sich des mit dem ein eine auch es als im auf daß dass wird werden sind aber wie oder '
            'el la de que y los las en un una por con no se del al es su lo como más para sus pero '
            'le les des et est qui une dans du pas il au par sur ne ce plus pour sont il di che e gli della non per si da dei nel alla sono '
            'et est in non ad quod ut cum sed quae qui enim esse vel ex per autem etiam sunt quam hoc atque nec'.split())


def front(t):
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if not m:
        return None, t
    d = {}
    for l in m.group(1).split('\n'):
        if ':' in l:
            a, b = l.split(':', 1); d[a.strip()] = b.strip()
    return d, t[m.end():]


def paras(body):
    out = []
    for b in re.split(r'\n\s*\n', body):
        b = b.strip()
        if not b:
            continue
        ty = 'm' if OWN.fullmatch(b) else 'q' if b.startswith('>') else 'h' if b.startswith('#') else 'p'
        out.append((ty, re.sub(r'^>\s?', '', b, flags=re.M) if ty == 'q' else b))
    return out


def check(path):
    t = open(path, encoding='utf-8').read()
    d, body = front(t)
    c = collections.Counter()
    if d is None:
        return c
    tl, ol = d.get('translation_language'), d.get('original_language')
    head = body[:4000]
    # header / boilerplate
    for k in ('year', 'title_en'):
        if k in d and not d[k] and not (k == 'title_en' and ol == 'en'):
            c['empty_' + k] += 1
    if d.get('pages') == '0':
        c['pages_zero'] += 1
    c['quoted_fm_values'] += sum(1 for v in d.values() if v.startswith('"'))
    if 'THIS FILE IS THE SOURCE' in d.get('source', '') and 'Generated file' in head:
        c['conv_says_generated_but_source'] += 1
    if 'generated' in d.get('source', '') and 'THIS FILE IS THE SOURCE' in head:
        c['conv_says_source_but_generated'] += 1
    if 'not in this file' in d.get('original_text', '') and 'quoted blocks (`> …`) are the original' in head:
        c['conv_promises_original'] += 1
    if tl == 'none' and 'plain paragraphs the English' in head:
        c['conv_promises_english'] += 1
    P = paras(body)
    # page numbers: own-line markers, else inline markers in the main stream
    stream = 'q' if any(t == 'q' for t, _ in P) else 'p'       # the original's markers when it is there, else the text's
    seq = MK.findall('\n'.join(x for ty, x in P if ty in (stream, 'm', 'h')))
    nums = []
    for v in re.findall(r'\[p\.\s+(?:[IVXL]+\.)?(\d+)\]', ' '.join(seq)):
        if not nums or nums[-1] != int(v):
            nums.append(int(v))
    c['folio_out_of_run'] = sum(1 for a, b, n in zip(nums, nums[1:], nums[2:]) if n == a + 2 and b != a + 1)
    c['folio_dup'] = sum(v - 1 for v in collections.Counter(nums).values() if v > 1)
    # fragmentation of plain paragraphs (no marker between)
    for (ta, a), (tb, b) in zip(P, P[1:]):
        if ta == tb == 'p':
            a2, b2 = MK.sub('', a).strip(), MK.sub('', b).strip()
            if a2 and b2 and re.search(r'[A-Za-zÀ-ÿ,‐-]$', a2) and re.match(r'[a-zà-ÿ]', b2):
                c['midsentence_break'] += 1
    for i in range(len(P) - 2):
        ty, x = P[i]
        if ty == 'p' and len(x.split()) <= 2 and len(x) < 20 and P[i + 1][0] == 'm' and P[i + 2][1].lower().startswith(x.lower().strip('‐-')[:4]):
            c['catchword'] += 1
    pl = [x for ty, x in P if ty == 'p']
    c['wide_space_line'] = sum(1 for x in pl if re.search(r'\S {6,}\S', x))
    c['dropcap_split'] = sum(1 for ty, x in P if ty in 'pq' and re.match(r'[A-Z] {2,}[a-z]', x))
    c['folio_text_line'] = sum(1 for x in pl if re.fullmatch(r'[—–-]?\s*[\dIVXLCivxlc]+\s*[—–-]?\.?', x.strip()))
    c['heading_in_quote'] = sum(1 for ty, x in P if ty == 'q' and re.search(r'(^|\s)#{2,6} ', x))
    c['sup_unbalanced'] = abs(body.count('<sup>') - body.count('</sup>'))
    c['google_boilerplate'] = len(re.findall(r'digitized by Google|automatisierten Abfragen', body))
    # pairing: number tokens and § numbers shared between an original block and its English
    if tl == 'en':
        num = re.compile(r'(?<![\d.])\d{2,4}(?!\d)')
        for (ta, a), (tb, b) in zip(P, P[1:]):
            if ta == 'q' and tb == 'p':
                x, y = set(num.findall(a)), set(num.findall(b))
                if len(x) >= 2 and len(y) >= 2 and not x & y:
                    c['pair_no_shared_number'] += 1
        page = []
        for blk in re.split(r'\n(?=\[(?:p\.|scan|PDF) [^\]]+\]\n)', body):
            q = '\n'.join(l for l in blk.split('\n') if l.startswith('>'))
            e = '\n'.join(l for l in blk.split('\n') if not l.startswith('>'))
            a = set(re.findall(r'§\.?\s?(\d{2,3})', q)); b = set(re.findall(r'§\.?\s?(\d{2,3})', e))
            if a and b and not a & b:
                c['page_section_mismatch'] += 1
        for x in pl:
            w = re.findall(r"[a-zäöüßáéíóúñàèìòùç]+", x.lower())
            if len(x) >= 250 and len(w) >= 25:
                if sum(v in OTHER for v in w) / len(w) > 0.2 and sum(v in EN for v in w) / len(w) < 0.06:
                    c['english_column_not_english'] += 1
    return +c


files = sorted(glob.glob(os.path.join(ROOT, '*.md')) + glob.glob(os.path.join(ROOT, 'vasconcelos', '*.md')))
files = [f for f in files if os.path.basename(f) not in ('README.md', 'PROJECT-INSTRUCTIONS.md')]
if '--file' in opt:
    files = [f for f in files if opt['--file'] in f]
res, tot = {}, collections.Counter()
for f in files:
    r = check(f); n = os.path.relpath(f, ROOT); res[n] = dict(r); tot.update(r)
    if r:
        print(f'{n}: ' + ', '.join(f'{k} {v}' for k, v in sorted(r.items())))
print('\nTOTAL: ' + ', '.join(f'{k} {v}' for k, v in sorted(tot.items())))
if '--json' in opt:
    json.dump({'files': res, 'total': dict(tot)}, open(opt['--json'], 'w'), indent=1, ensure_ascii=False)
