"""Editions as folders of single-language files, and the interleaved ("facing") text they merge into.

    corpus/<slug>/edition.yaml   front matter of the old file (keys and values as they were) + heading: + conventions:
                 original.md     the original's paragraphs, `> ` removed (original-only texts: all paragraphs, as they are)
                 en.md           the English paragraphs
                 glossary.md, notes.md   when the edition has them

`merge_dir(folder)` returns the interleaved Markdown text the reader renders from; `split_text(text)` is its inverse
(tools/split.py writes the files). Synchronisation points shared by both files: standalone page marks (`[p. N]`,
`[scan N]`, `[PDF N]`), headings and the separator `⁂`. Between two of them the merge pairs the i-th original paragraph
with the i-th English paragraph (original first, each followed by its footnotes), leftovers at the end. An interleaving
that does not follow this pairing is not recoverable from the two files; the HTML does not depend on it.
An edition whose edition.yaml says `paragraphs: printed` (the paragraph standard of tools/realign.py: original.md holds the printed
paragraphs, en.md one unit per unit) is merged unit n with unit n across the whole text instead (`merge_units`); a heading pair whose
two texts differ shows as `<original> — <English>`. When such an edition does not pair (unit counts, marks or headings differ) the
merge raises ValueError rather than fall back. Every other edition keeps the per-page merge.
Standard library only."""
import os, re, json, difflib

MARK = r'\[(?:p\. [^\]]+|scan \d+|PDF \d+)\]'
INLINE = re.compile(r'\[(?:p\. |scan |PDF )([^\]]+)\]')                       # as in reader.py: label = m.group(0)[1:-1]
NOTE = re.compile(r'^(\d{1,3}\s?[a-c]?\)|\*+\)|\(\d{1,3}\)|[†‡]|<sup>[^<]*</sup>\s)')   # a footnote paragraph


class Unsplittable(Exception):
    pass


def labels(text):
    return [m.group(0)[1:-1] for m in INLINE.finditer(text)]


def front_matter(fm):
    h = dict(re.findall(r'^(\w+): (.*)$', fm, re.M))
    return {k: v.strip('"') for k, v in h.items()}


def is_mono(fm):
    """original-only text: the plain paragraphs are the original (reader.py: translation_language none or empty)"""
    return front_matter(fm).get('translation_language', '') in ('none', '')


def sync_kind(p):
    if re.fullmatch(MARK, p):
        return 'M'
    if re.match(r'^#{1,6} ', p):
        return 'H'
    if p == '⁂':
        return 'S'
    return None


def is_note(plain, quoted):
    return bool(NOTE.match(' '.join(l.lstrip('> ').strip() for l in plain.split('\n')) if quoted else plain))


def groups(items):
    """items: [(is_note, text, label)] -> [[main or None, [notes], anchor]]; a footnote belongs to the paragraph before it.
    The anchor of a paragraph is the page mark it carries inline (or, for an English paragraph, the mark standing before it)."""
    g = []
    for note, text, label in items:
        if note and g:
            g[-1][1].append(text)
        elif note:
            g.append([None, [text], None])
        else:
            g.append([text, [], (labels(text) or [label])[0] if (labels(text) or label) else None])
    return g


def pair_plain(og, eg):
    """the i-th original group with the i-th English group (main paragraphs, then their notes two by two); leftovers follow"""
    out = []
    for k in range(max(len(og), len(eg))):
        if k < len(og) and og[k][0] is not None: out.append(('O', og[k][0]))
        if k < len(eg) and eg[k][0] is not None: out.append(('E', eg[k][0]))
        on = og[k][1] if k < len(og) else []
        en = eg[k][1] if k < len(eg) else []
        for m in range(max(len(on), len(en))):
            if m < len(on): out.append(('O', on[m]))
            if m < len(en): out.append(('E', en[m]))
    return out


def pair_groups(og, eg):
    """pair_plain between page marks that both sides carry (an inline mark in an original paragraph and in the English one,
    or the standalone mark split.py put before the English paragraph)"""
    cuts, j0 = [], 0
    for i, g in enumerate(og):
        if g[2] is None:
            continue
        for j in range(j0, len(eg)):
            if eg[j][2] == g[2]:
                cuts.append((i, j)); j0 = j + 1
                break
    out, pi, pj = [], 0, 0
    for ci, cj in cuts + [(len(og), len(eg))]:
        out += pair_plain(og[pi:ci], eg[pj:cj])
        pi, pj = ci, cj
    return out


def read_stream(text, quoted):
    """a file's paragraphs -> [(kind, plain, is_note)]; kind M/H/S (sync) or C (content)"""
    if text is None or not text.strip():
        return []
    out = []
    for p in text.rstrip('\n').split('\n\n'):
        k = sync_kind(p)
        out.append((k, p, False) if k else ('C', p, is_note(p, quoted)))
    return out


def quote(p):
    return '\n'.join('> ' + l for l in p.split('\n'))


def merge_units(O, E):
    """unit n of the original with unit n of the English over the whole text, or None when the two files do not fit that"""
    UO = [t for t in O if t[0] in ('C', 'H')]
    UE = [t for t in E if t[0] in ('C', 'H')]
    if not UO or len(UO) != len(UE) or any((a[0] == 'H') != (b[0] == 'H') for a, b in zip(UO, UE)):
        return None

    def syncs(S):                                                # (number of units before it, the mark or separator)
        n, out = 0, []
        for t in S:
            if t[0] in ('M', 'S'):
                out.append((n, t[1]))
            else:
                n += 1
        return out
    if syncs(O) != syncs(E):
        return None
    out, ue = [], iter(UE)
    for t in O:
        if t[0] in ('M', 'S'):
            out.append(t[1]); continue
        e = next(ue)
        if t[0] == 'H':
            ot, et = re.sub(r'^#+\s*', '', t[1]).strip(), re.sub(r'^#+\s*', '', e[1]).strip()
            out.append(t[1] if ot == et else f'{t[1]} — {et}')
        else:
            out += [quote(t[1]), e[1]]
    return out


def merge_streams(O, E, mono, printed=False):
    """O, E: token streams -> paragraphs of the interleaved body"""
    if mono:
        return [t[1] for t in O]
    if not O or not E:                                           # one language only: that file is the body
        return [t[1] if t[0] != 'C' else (quote(t[1]) if O else t[1]) for t in (O or E)]
    if printed:
        paired = merge_units(O, E)
        if paired is None:
            raise ValueError('edition.yaml says paragraphs: printed, but original.md and en.md do not pair unit by unit')
        return paired
    O, E = list(O), list(E)
    osync = [i for i, t in enumerate(O) if t[0] != 'C']
    esync = [j for j, t in enumerate(E) if t[0] != 'C']
    sm = difflib.SequenceMatcher(None, [O[i][1] for i in osync], [E[j][1] for j in esync], autojunk=False)
    mo, me = set(), set()
    for a, b, n in sm.get_matching_blocks():
        mo.update(osync[a + k] for k in range(n)); me.update(esync[b + k] for k in range(n))
    for i in osync:
        if i not in mo:                                          # a quoted paragraph that only looks like a mark or heading
            O[i] = ('C', O[i][1], is_note(O[i][1], True))
    for j in esync:
        if j not in me:
            if E[j][0] != 'M':
                raise ValueError(f'{E[j][1]!r} is in en.md but not in original.md')
            E[j] = ('X', E[j][1], False)                         # the page begins inside the paired original paragraph
    out, i, j = [], 0, 0
    while True:
        orun, erun, pend = [], [], []
        while i < len(O) and O[i][0] == 'C':
            orun.append((O[i][2], O[i][1], None)); i += 1
        while j < len(E) and E[j][0] in ('C', 'X'):
            if E[j][0] == 'X':
                pend.append(E[j][1][1:-1])
            else:
                erun.append((E[j][2], E[j][1], pend[0] if pend and not E[j][2] else None)); pend = []
            j += 1
        out += [quote(t) if side == 'O' else t for side, t in pair_groups(groups(orun), groups(erun))]
        ot = O[i] if i < len(O) else None
        et = E[j] if j < len(E) else None
        if ot is None and et is None:
            return out
        if ot != et:
            raise ValueError(f'the two files do not agree at {ot!r} / {et!r}')
        out.append(ot[1]); i += 1; j += 1


def parse_yaml(y):
    lines = y.rstrip('\n').split('\n')
    heading = conv = None
    keep = []
    for l in lines:
        if l.startswith('heading: '): heading = json.loads(l[9:])
        elif l.startswith('conventions: '): conv = json.loads(l[13:])
        else: keep.append(l)
    return '\n'.join(keep), heading, conv


def merge_parts(yaml_text, orig, en):
    fm, heading, conv = parse_yaml(yaml_text)
    mono = is_mono(fm)
    body = merge_streams(read_stream(orig, not mono), read_stream(en, False), mono, front_matter(fm).get('paragraphs') == 'printed')
    return f'---\n{fm}\n---\n\n{heading}\n\n{conv}\n\n' + '\n\n'.join(body) + '\n'


def _read(path):
    return open(path, encoding='utf-8').read() if os.path.exists(path) else None


def merge_dir(folder):
    return merge_parts(_read(f'{folder}/edition.yaml'), _read(f'{folder}/original.md'), _read(f'{folder}/en.md'))


def split_text(s):
    """interleaved text -> (edition.yaml, original.md or None, en.md or None, inserted); raises Unsplittable"""
    m = re.match(r'---\n(.*?)\n---\n', s, re.S)
    if not m:
        raise Unsplittable('no front matter')
    fm = m.group(1)
    mm = re.fullmatch(r'\n(# [^\n]*)\n\n(Conventions:[^\n]*)\n\n(.*)', s[m.end():], re.S)
    if not mm:
        raise Unsplittable('no "# " heading and Conventions paragraph in the expected place')
    heading, conv, body = mm.groups()
    if re.search(r'^(heading|conventions): ', fm, re.M):
        raise Unsplittable('front matter already has a heading: or conventions: key')
    mono = is_mono(fm)
    toks = []                       # (kind, side, plain, is_note): side 'O' original, 'E' English, None for sync points
    for p in body.rstrip('\n').split('\n\n'):
        if p.startswith('>'):
            if mono:
                if p == '>':
                    continue        # an empty quote the reader ignores
                raise Unsplittable('quoted block in an original-only text: the reader leaves it out of the page')
            lines = p.split('\n')
            if not all(l.startswith('> ') for l in lines):
                raise Unsplittable('quoted block with a line that does not start with "> "')
            plain = '\n'.join(l[2:] for l in lines)
            if any(l == '' for l in plain.split('\n')):
                raise Unsplittable('quoted block with an empty quoted line')
            toks.append(('C', 'O', plain, is_note(plain, True)))
            continue
        k = sync_kind(p)
        if k:
            toks.append((k, None, p, False))
        elif mono:
            toks.append(('C', 'O', p, False))
        else:
            toks.append(('C', 'E', p, is_note(p, False)))
    has_o = any(t[1] == 'O' for t in toks)
    has_e = any(t[1] == 'E' for t in toks)
    O, E, inserted = [], [], []
    run = []

    def flush():
        need, queue = {}, []         # English main paragraph (index in run) -> marks that must stand before it
        for n, t in enumerate(run):
            if t[1] == 'O' and not t[3] and labels(t[2]):
                queue.append(t)
            elif t[1] == 'E' and not t[3] and queue:
                o = queue.pop(0)
                miss = [l for l in labels(o[2]) if l not in labels(t[2])]
                if miss:
                    need[n] = miss
        for n, t in enumerate(run):
            if t[1] == 'O':
                O.append(('C', t[2], t[3]))
            else:
                for l in need.get(n, []):
                    E.append(('M', f'[{l}]', False)); inserted.append(l)
                E.append(('C', t[2], t[3]))
        run.clear()
    for t in toks:
        if t[0] == 'C':
            run.append(t)
            continue
        flush()
        if has_o: O.append((t[0], t[2], False))
        if has_e: E.append((t[0], t[2], False))
    flush()
    yaml_text = fm + f'\nheading: {json.dumps(heading, ensure_ascii=False)}\nconventions: {json.dumps(conv, ensure_ascii=False)}\n'
    text = lambda S: '\n\n'.join(t[1] for t in S) + '\n'
    return yaml_text, (text(O) if has_o else None), (text(E) if has_e else None), inserted


def page_labels(text):
    """every page mark in a file, in order (standalone or inline)"""
    return labels(text) if text else []
