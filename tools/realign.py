#!/usr/bin/env python3
"""usage: realign.py <slug> --old <interleaved.md> [--write] [--resolutions FILE] [--out DIR] [--corpus DIR]

Brings the en.md of a photocopy edition folder (corpus/<slug>/, see facing.py) to the paragraph standard after its
original.md was replaced by a clean transcription of the printed paragraphs (never cut at a page turn, `[p. N]` inline).
The English of such an edition was made page by page from a bad OCR, and the old interleaved file keeps that OCR in
quoted blocks (`> ...`) cut wherever an English paragraph starts, the English paragraph after each block, standalone
page marks between. The OCR is bad, but its words are in the right order and on the right pages.

1. Units of the old file: every English paragraph (with its page) and the quoted block(s) just before it. A heading line
   is a unit too; the block before it is the OCR of the heading and serves to place it.
2. Each unit is placed in the new original: old OCR and new text are folded to lower-case letters (s/f/long s, umlauts,
   sharp s alike), aligned page by page (difflib), and the unit's first letter is mapped to an offset. The first unit of a
   page starts where the page starts.
3. Snap: a start within 15 letters before or 90 after a new unit's start belongs to that unit (the earliest one still
   free; an English paragraph takes a paragraph, a heading a heading when there is one). The 90 is measured: the old blocks
   start about a line (20-40 letters) after the printed paragraph, because the first line went into the block before. Otherwise it falls inside a new paragraph: the old English broke a
   printed paragraph there, so its English joins the English before it.
4. en.md: each new unit gets the English units that start in it, joined with a space; `[p. N] ` stands before an English
   unit that opens a page (as a standalone paragraph where original.md has the mark standalone, i.e. before a heading). A
   heading unit takes the old English heading's text at the original's level, or copies the original heading.
5. Residue, listed and never guessed, written to <out>/realign-residue.json: a new paragraph that got no English (the print
   breaks a paragraph where the English did not; the case holds the English that spans it), and an English unit that could
   not be placed (no block, or no German on its page). With --resolutions FILE the splits and placements decided by a reader
   are applied and recorded in the residue file:
     {"cases": {"<id>": {"splits": [{"de_before":..,"de_after":..,"en_before":..,"en_after":..}, ..]}},
      "unlocated": {"<id>": {"unit": <new unit index>} | {"skip": "reason"}}}
   `en_after` is the English text where the next German unit's part begins (searched after the previous split).
Dry run by default; --write rewrites <corpus>/<slug>/en.md. Standard library only."""
import os, re, sys, json, bisect, difflib, argparse, collections, unicodedata, pickle, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SNAP = 15            # a block may start this many letters before a new unit's start
SNAP_H = 60          # a heading's block is sometimes the tail of the paragraph before it: look this far ahead
SNAP_BACK = 90       # ... or this many letters after it: the old blocks start about a line late (see the docstring)
MIN_BLOCK = 3
INLINE = re.compile(r'\[p\. ([^\]]+)\]')
STAND = re.compile(r'\[p\. ([^\]]+)\]')
OLDMARK = re.compile(r'\[(?:p\. |scan )([^\]]+)\]')


def fold(s):
    """lower-case letters only; long s, f and s alike; umlauts and sharp s folded"""
    out = []
    for ch in unicodedata.normalize('NFKD', s.lower()):
        if ch == 'ß' or ch == 'ſ':
            out.append('s')
        elif 'a' <= ch <= 'z':
            out.append('s' if ch == 'f' else ch)
    return ''.join(out)


def words(s):
    s = INLINE.sub(' ', s)
    s = re.sub(r'^#+ ', '', s, flags=re.M)
    return re.findall(r"[^\W_]+(?:[’'\-][^\W_]+)*", s.replace('*', ' '))


# ---------------------------------------------------------------- the old interleaved file

def parse_old(text):
    paras = text.strip().split('\n\n')
    i = next(i for i, p in enumerate(paras) if p.startswith('Conventions:')) + 1
    labels, units, pend = [], [], []
    for p in paras[i:]:
        m = re.fullmatch(r'\[(?:p\. |scan )([^\]]+)\]', p)
        if m:
            labels.append(m.group(0)[1:-1]); continue
        page = len(labels) - 1
        if p.startswith('>'):
            pend.append((page, '\n'.join(l[2:] if l.startswith('> ') else l.lstrip('>') for l in p.split('\n')).strip()))
            continue
        units.append({'kind': 'H' if p.startswith('#') else 'E', 'text': p, 'quotes': pend,
                      'page': pend[0][0] if pend else page})
        pend = []
    return labels, units, pend


# ---------------------------------------------------------------- the new original

def parse_new(text):
    blocks, pages, pieces, pos = [], [], [], 0
    for i, p in enumerate(text.rstrip('\n').split('\n\n')):
        if STAND.fullmatch(p):
            pages.append({'label': STAND.fullmatch(p).group(1), 'pos': pos, 'standalone': True, 'block': i})
            blocks.append({'kind': 'M', 'text': p}); continue
        start = pos
        for j, part in enumerate(INLINE.split(p)):
            if j % 2 == 0:
                f = fold(part); pieces.append(f); pos += len(f)
            else:
                pages.append({'label': part, 'pos': pos, 'standalone': False, 'block': i})
        blocks.append({'kind': 'H' if p.startswith('#') else 'P', 'text': p, 'start': start, 'end': pos})
    units = [b for b in blocks if b['kind'] != 'M']
    for n, b in enumerate(blocks):
        b['unit'] = None
    for n, b in enumerate(units):
        b['unit'] = n
    return blocks, units, pages, ''.join(pieces)


# ---------------------------------------------------------------- alignment

def map_off(bl, s, tlen):
    prev = nxt = None
    for b in bl:
        if b.a <= s < b.a + b.size:
            return b.b + (s - b.a)
        if b.a + b.size <= s:
            prev = b
        else:
            nxt = b; break
    if prev and nxt:
        pa, pb = prev.a + prev.size, prev.b + prev.size
        r = pb + (s - pa) if s - pa <= nxt.a - s else nxt.b - (nxt.a - s)
        return max(pb, min(nxt.b, r))
    if nxt:
        return max(0, nxt.b - (nxt.a - s))
    if prev:
        return min(tlen, prev.b + prev.size + (s - prev.a - prev.size))
    return 0


def locate(old_units, old_labels, pages, newL, cache):
    """sets e['g'] (global letter offset in the new text) for every unit with a block; returns per-page stats"""
    n = len(pages)
    S = collections.defaultdict(str)
    for e in old_units:
        for j, (pg, q) in enumerate(e['quotes']):
            if j == 0:
                e['s'] = len(S[pg])
            S[pg] += fold(q)
    stats = {}
    edges = [p['pos'] for p in pages] + [len(newL)]
    for k in range(n):
        s, T = S.get(k, ''), newL[edges[k]:edges[k + 1]]
        key = hashlib.md5((s + '|' + T).encode()).hexdigest()
        if key not in cache:
            cache[key] = [(b.a, b.b, b.size) for b in difflib.SequenceMatcher(None, s, T, autojunk=False).get_matching_blocks()]
        bl = [difflib.Match(a, b, z) for a, b, z in cache[key] if z >= MIN_BLOCK]
        stats[k] = (len(s), len(T), sum(b.size for b in bl))
        for e in old_units:
            if e['quotes'] and e['page'] == k:
                if not T:
                    e['g'] = None
                else:
                    e['g'] = edges[k] + (0 if e['s'] == 0 else min(len(T), map_off(bl, e['s'], len(T))))
    return stats


# ---------------------------------------------------------------- assignment

def assign(old_units, new_units):
    starts = [u['start'] for u in new_units]
    last, log = -1, collections.Counter()
    for e in old_units:
        e['unit'] = None
        g = e.get('g')
        if not e['quotes'] or g is None:
            e['status'] = 'unlocated'; log['unlocated'] += 1; continue
        lo, hi = bisect.bisect_left(starts, g - SNAP_BACK), bisect.bisect_right(starts, g + (SNAP_H if e['kind'] == 'H' else SNAP))
        c = [u for u in range(lo, hi) if u > last]
        if e['kind'] == 'E':
            c = [u for u in c if new_units[u]['kind'] == 'P']
        else:
            c = [u for u in c if new_units[u]['kind'] == 'H'] or c
        if c:
            u = min(c)        # the earliest unit not yet taken: the English units run in order, a block starts late, never early
            e['unit'], e['status'] = u, 'snap'; last = u; log['snap'] += 1
            continue
        v = bisect.bisect_right(starts, g) - 1
        while v >= 0 and new_units[v]['kind'] == 'H':
            v -= 1
        if last >= 0 and new_units[last]['kind'] == 'P':
            e['unit'], e['status'] = last, 'join'; log['join'] += 1
            if v < last:
                log['regress'] += 1
        else:
            nxt = last + 1
            while nxt < len(new_units) and new_units[nxt]['kind'] == 'H':
                nxt += 1
            e['unit'], e['status'] = max(v, nxt), 'forced'; last = e['unit']; log['forced'] += 1
    return log


def render_old(e, pages_by_k):
    """English of an old unit: heading hashes dropped, `[p. N] ` before the unit that opens its page unless the mark stands alone"""
    t = re.sub(r'^#+ ', '', e['text']) if e['kind'] == 'H' else e['text']
    t = ' '.join(t.split())
    if e.get('opens') and not pages_by_k[e['page']]['standalone']:
        t = f"[p. {pages_by_k[e['page']]['label']}] " + t
    return t


def assemble(old_units, units, pbk):
    """new unit -> its English: the old units assigned to it in old order, joined with a space"""
    en = collections.defaultdict(list)
    for e in old_units:
        if e['unit'] is not None:
            en[e['unit']].append(e)
    text = {}
    for u, es in en.items():
        if units[u]['kind'] == 'H':
            es = [e for e in es if e['kind'] == 'H'] or es
        text[u] = ' '.join(render_old(e, pbk) for e in es)
    return text, en


def clip_(s, n=90):
    return ' '.join(s.split())[:n]


def residue(old_units, units, pages, text):
    cases = []
    empty = [u for u in range(len(units)) if units[u]['kind'] == 'P' and u not in text]
    runs, i = [], 0
    while i < len(empty):
        j = i
        while j + 1 < len(empty) and all(units[x]['kind'] == 'H' or x in empty for x in range(empty[j] + 1, empty[j + 1] + 1)):
            j += 1
        runs.append(empty[i:j + 1]); i = j + 1
    for run in runs:
        w = max((x for x in range(run[0]) if units[x]['kind'] == 'P' and x in text), default=None)
        if w is not None and any(units[x]['kind'] == 'P' and x not in text for x in range(w + 1, run[0])):
            w = None
        members = ([w] if w is not None else []) + [x for x in range(run[0], run[-1] + 1) if units[x]['kind'] == 'P']
        cases.append({'id': len(cases) + 1, 'kind': 'no_english', 'with_english': w,
                      'german': [{'unit': x, 'text': clip_(units[x]['text'], 200)} for x in members],
                      'before': clip_(units[members[0] - 1]['text']) if members[0] > 0 else '',
                      'after': clip_(units[run[-1] + 1]['text']) if run[-1] + 1 < len(units) else '',
                      'english': text.get(w, '') if w is not None else ''})
    idx = {id(e): n for n, e in enumerate(old_units)}
    merged = []
    for e in (e for e in old_units if e['unit'] is None):
        if merged and idx[id(e)] == idx[id(merged[-1][-1])] + 1 and e['page'] == merged[-1][-1]['page']:
            merged[-1].append(e)
        else:
            merged.append([e])
    ucases = []
    for g in merged:
        a, b = idx[id(g[0])], idx[id(g[-1])]
        ucases.append({'id': len(ucases) + 1, 'kind': 'unlocated', 'page': pages[g[0]['page']]['label'],
                       'english': [e['text'] for e in g],
                       'ocr': [clip_(' '.join(q for _, q in e['quotes']), 120) for e in g],
                       'english_before': clip_(old_units[a - 1]['text']) if a else '',
                       'english_after': clip_(old_units[b + 1]['text']) if b + 1 < len(old_units) else '',
                       'old_index': [a, b]})
    return cases, ucases


def build(slug, old_path, corpus, outdir, resolutions=None, write=False):
    folder = f'{corpus}/{slug}'
    otext = open(f'{folder}/original.md', encoding='utf-8').read()
    blocks, units, pages, newL = parse_new(otext)
    old_labels, old_units, orphans = parse_old(open(old_path, encoding='utf-8').read())
    rep = {'old_pages': len(old_labels), 'new_pages': len(pages), 'new_units': len(units), 'old_units': len(old_units)}
    if len(old_labels) != len(pages):
        raise SystemExit(f'page marks differ: old {len(old_labels)}, new {len(pages)}')
    seen = set()
    for e in old_units:
        e['opens'] = bool(e['quotes']) and e['page'] not in seen
        if e['quotes']:
            seen.add(e['page'])
    os.makedirs(outdir, exist_ok=True)
    cache_path = f'{outdir}/realign-align.pkl'
    cache = pickle.load(open(cache_path, 'rb')) if os.path.exists(cache_path) else {}
    stats = locate(old_units, old_labels, pages, newL, cache)
    pickle.dump(cache, open(cache_path, 'wb'))
    for k, (ls, lt, lm) in stats.items():
        if ls and not lt:
            for e in old_units:
                if e['page'] == k:
                    e['g'] = None
    rep['assign'] = dict(assign(old_units, units))
    rep['weak_pages'] = [(k, pages[k]['label'], ls, lt, lm) for k, (ls, lt, lm) in stats.items() if ls and lt and lm < 0.6 * min(ls, lt)]
    pbk = dict(enumerate(pages))

    text, en = assemble(old_units, units, pbk)
    cases, ucases = residue(old_units, units, pages, text)
    rep['residue'] = {'no_english': len(cases), 'unlocated': len(ucases)}
    res = {'cases': cases, 'unlocated': ucases, 'resolved': []}
    left_out = []
    if resolutions:
        R = json.load(open(resolutions, encoding='utf-8'))
        for c in ucases:                                  # English units with no block: placed by their order in the old file
            r = R.get('unlocated', {}).get(str(c['id']))
            if r is None:
                continue
            a, b = c['old_index']
            if 'skip' in r:
                left_out += c['english']
                res['resolved'].append({'unlocated': c['id'], 'left_out': r['skip']}); continue
            x = r['unit'] if 'unit' in r else old_units[a - 1]['unit']
            for i in range(a, b + 1):
                old_units[i]['unit'] = x
            res['resolved'].append({'unlocated': c['id'], 'unit': x, 'german': clip_(units[x]['text'], 80),
                                    'how': 'in the German unit that holds it, in its place among that unit\'s English' if 'unit' in r else 'in its place in the English before and after it'})
        text, en = assemble(old_units, units, pbk)
        todo = [(c, R.get('cases', {}).get(str(c['id']))) for c in cases]
        todo += [({'id': 'x%d' % (n + 1), 'with_english': r['w'], 'german': [{'unit': t, 'text': clip_(units[t]['text'], 200)} for t in r['targets']]}, r)
                 for n, r in enumerate(R.get('extra', []))]
        for c, r in todo:
            if not r:
                continue
            if 'filled_by_unlocated' in r or 'merged_into' in r:
                res['resolved'].append({'case': c['id'], **{k: r[k] for k in ('filled_by_unlocated', 'merged_into') if k in r}}); continue
            w = c['with_english']
            targets = r.get('targets') or [m['unit'] for m in c['german']]
            s = text[w]
            for x in r.get('pull_before', []):
                s = text.pop(x) + ' ' + s
            for x in r.get('pull', []):                  # English that stands one unit too early: taken in, split again below
                s += ' ' + text.pop(x)
            for old, new in r.get('replace', []):
                if s.count(old) != 1:
                    raise SystemExit(f"case {c['id']}: {old!r} occurs {s.count(old)} times")
                s = s.replace(old, new)
            cuts, from_ = [], 0
            for sp in r['splits']:
                at = s.find(sp['en_after'], from_)
                if at < 0:
                    raise SystemExit(f"case {c['id']}: {sp['en_after']!r} not in the English after position {from_}: ...{s[max(0, from_ - 80):from_ + 700]!r}")
                m = re.search(r'\[p\. [^\]]+\]\s*$', s[:at])
                cuts.append(m.start() if m else at); from_ = at + 1
            parts = [s[a:b].strip() for a, b in zip([0] + cuts, cuts + [len(s)])]
            for k in range(len(parts) - 1):
                if parts[k].count('*') % 2:
                    parts[k] += '*'; parts[k + 1] = '*' + parts[k + 1]
            if len(parts) != len(targets):
                raise SystemExit(f"case {c['id']}: {len(parts)} parts for {len(targets)} targets")
            new = collections.OrderedDict()
            for x, part in zip(targets, parts):
                new[x] = (new[x] + ' ' + part) if x in new else part
            text.update(new)
            tail, head = (lambda t: ' '.join(t.split())[-50:]), (lambda t: ' '.join(t.split())[:50])
            res['resolved'].append({'case': c['id'], 'german': [m['text'][:60] for m in c['german']], 'targets': targets,
                                    'pulled_in': r.get('pull', []) + r.get('pull_before', []), 'replace': r.get('replace', []),
                                    'breaks': [{'de_before': tail(units[targets[k]]['text']), 'en_before': tail(parts[k]),
                                                'de_after': head(units[targets[k + 1]]['text']), 'en_after': head(parts[k + 1])}
                                               for k in range(len(parts) - 1)]})

    out = []
    for b in blocks:
        if b['kind'] == 'M':
            out.append(b['text'])
        elif b['kind'] == 'H':
            lvl = re.match(r'#+', b['text']).group(0)
            out.append(b['text'] if b['unit'] not in text else lvl + ' ' + re.sub(r'^#+ ', '', text[b['unit']]))
        else:
            out.append(text.get(b['unit'], ''))
    new_en = '\n\n'.join(out).rstrip('\n') + '\n'

    eparas = [p for p in new_en.rstrip('\n').split('\n\n') if not STAND.fullmatch(p)]
    rep['units'] = {'original': len(units), 'en': len(eparas)}
    olabels, elabels = INLINE.findall(otext), INLINE.findall(new_en)
    rep['labels_equal'] = olabels == elabels
    if not rep['labels_equal']:
        rep['labels_missing'] = [l for l in olabels if l not in elabels][:20]
    rep['empty_units'] = [n for n, p in enumerate(eparas) if not p.strip()]
    rep['odd_asterisks'] = [n for n, p in enumerate(eparas) if p.count('*') % 2]
    old_words = collections.Counter(w for e in old_units for w in words(e['text']))
    new_words = collections.Counter(words(new_en))
    rep['words_only_old'] = dict((old_words - new_words).most_common(60))
    rep['words_only_new'] = dict((new_words - old_words).most_common(60))
    rep['english_per_unit'] = dict(sorted(collections.Counter(len(es) for es in en.values()).items()))
    rep['merged_into_printed_paragraph'] = sum(len(es) - 1 for es in en.values() if len(es) > 1)
    json.dump(res, open(f'{outdir}/realign-residue.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if left_out:
        rep['english_left_out'] = left_out
    if write:
        open(f'{folder}/en.md', 'w', encoding='utf-8').write(new_en)
    return rep


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('slug'); ap.add_argument('--old', required=True); ap.add_argument('--write', action='store_true')
    ap.add_argument('--resolutions'); ap.add_argument('--out', default='.'); ap.add_argument('--corpus', default='corpus')
    a = ap.parse_args()
    print(json.dumps(build(a.slug, a.old, a.corpus, a.out, a.resolutions, a.write), ensure_ascii=False, indent=1))
