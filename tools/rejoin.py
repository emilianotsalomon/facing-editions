#!/usr/bin/env python3
"""usage: rejoin.py [--write] <corpus/slug> [<corpus/vasconcelos/slug> ...]      (edition folders; see facing.py)

Paragraph standard: original.md holds printed paragraphs, never cut at a page turn, with `[p. N]` inline where the page
begins; en.md has one paragraph per original paragraph, with `[p. N]` at the matching point. Photocopy editions were
translated page by page, so a paragraph that runs over a page turn sits as two paragraphs with a standalone `[p. N]`
line between them. This joins them: `prev [p. N] next`.

A turn continues when the English paragraph after the mark starts in lower case, or the last English paragraph before
it does not end a sentence (. ! ? : ; … or a dash, then closing quotes/brackets, footnote cues ignored). The original is
only read for the report (turns where it would decide otherwise). Footnote paragraphs and headings are never partners:
the partners are the last and first non-note paragraphs, notes standing between them go after the joined paragraph.
A page that opens or closes with a heading, a separator or another mark never continues.
When the edition has an original, a turn is joined only where the pairing is certain: the page before the mark has as many
original as English paragraphs (so the last pairs with the last) and the page after has an original paragraph (first with
first). A line-end hyphen on the original side ("Wahr-" + "heit der") drops the hyphen and the mark follows the joined word.
Dry run by default; --write rewrites original.md and en.md. Only photocopy editions are touched."""
import os, re, sys, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facing

HYPHENS = '-=⸗¬‐'
LOWER_MIN, NOEND_MIN = 25, 60          # a lower-case start counts from 25 characters; a missing sentence end alone counts from 60
STOP_EN = {'and', 'or', 'nor', 'to', 'but'}
STOP = {'und', 'oder', 'bis', 'sowie', 'bzw', 'et', 'ou', 'y', 'o', 'e', 'ed', 'ac', 'vel', 'atque', 'aut', 'ni', 'sive', 'seu'}
CLOSERS = '\'"”’»)]*_” '


def ends_sentence(s):
    s = re.sub(r'(<sup>[^<]*</sup>\s*)+$', '', s.rstrip()).rstrip()
    s = s.rstrip(CLOSERS)
    return s.endswith(('.', '!', '?', ':', ';', '…', '—', '–', '--'))


def lower_start(s):
    m = re.match(r'[\W_]*(\w)', s.lstrip())
    return bool(m) and m.group(1).isalpha() and m.group(1).islower()


def hyphen_end(s):
    s = s.rstrip()
    return len(s) > 1 and s[-1] in HYPHENS and s[-2].isalpha()


def clip(s, n=40, tail=False):
    s = ' '.join(s.split())
    return s[-n:] if tail else s[:n]


def build(o_text, e_text):
    """-> (O segments or None, E segments, syncs, unmatched-O-sync count); segment items are (text, is_note)"""
    E = facing.read_stream(e_text, False)
    if o_text is None:
        return None, segs_of(E, {i for i, t in enumerate(E) if t[0] != 'C'}), [t[1] for t in E if t[0] != 'C'], 0
    O = facing.read_stream(o_text, True)
    osync = [i for i, t in enumerate(O) if t[0] != 'C']
    esync = [j for j, t in enumerate(E) if t[0] != 'C']
    sm = difflib.SequenceMatcher(None, [O[i][1] for i in osync], [E[j][1] for j in esync], autojunk=False)
    mo, me = [], []
    for a, b, n in sm.get_matching_blocks():
        mo += [osync[a + k] for k in range(n)]; me += [esync[b + k] for k in range(n)]
    if len(me) != len(esync):
        raise ValueError('a mark or heading of en.md is not in original.md')
    loose = [O[i][1] for i in osync if i not in set(mo)]
    if any(not t.startswith('#') for t in loose):
        raise ValueError('original.md has a mark or separator that en.md does not')
    return segs_of(O, set(mo)), segs_of(E, set(me)), [E[j][1] for j in me], len(loose)


def segs_of(toks, shared):
    segs = [[]]
    for i, t in enumerate(toks):
        if i in shared:
            segs.append([])
        else:
            segs[-1].append((t[1], t[2] if t[0] == 'C' else False))
    return segs


def text_of(segs, syncs):
    out = []
    for k, seg in enumerate(segs):
        out += [t for t, _ in seg]
        if k < len(syncs):
            out.append(syncs[k])
    return '\n\n'.join(out) + '\n'


def partner(seg, from_end):
    """index of the last (first) non-note paragraph of a segment, or None"""
    rng = range(len(seg) - 1, -1, -1) if from_end else range(len(seg))
    for i in rng:
        if not seg[i][1]:
            return i
    return None


def join_english(a, b, mark):
    """-> (text, hyphen?); a translator's hyphen at the end of a stays, the next word follows without a space"""
    a, b = a.rstrip(), b.lstrip()
    w = re.match(r'\S+', b)
    if len(a) > 1 and a[-1] in '-‐' and a[-2].isalpha() and w and w.group(0)[0].isalpha() \
            and w.group(0).strip('.,;:!?)»”').lower() not in STOP | STOP_EN:
        rest = b[w.end():].lstrip()
        return a + w.group(0) + ' ' + mark + (' ' + rest if rest else ''), True
    return a + ' ' + mark + ' ' + b, False


def join_original(a, b, mark):
    """-> (text, hyphen?); a line-end hyphen at the end of a drops and the mark follows the joined word"""
    a = a.rstrip()
    w = re.match(r'\S+', b)
    if hyphen_end(a) and w and w.group(0)[0].isalpha() and w.group(0)[0].islower() and w.group(0).strip('.,;:!?)»”').lower() not in STOP:
        rest = b[w.end():].lstrip()
        return a[:-1] + w.group(0) + ' ' + mark + (' ' + rest if rest else ''), True
    return a + ' ' + mark + ' ' + b.lstrip(), False


def rejoin(O, E, syncs):
    st = dict(turns=0, joins=0, no_partner=0, lower_only=0, noend_only=0, both=0, no_join=0, unpaired=0, pseudo=0,
              hy_o=0, hy_e=0, de_no=0, de_yes=0, held=0, samples=[])
    i = 0
    while i < len(syncs):
        if facing.sync_kind(syncs[i]) != 'M':
            i += 1; continue
        st['turns'] += 1
        ia, ib = partner(E[i], True), partner(E[i + 1], False)
        if ia is None or ib is None:
            st['no_partner'] += 1; i += 1; continue
        ea, eb = E[i][ia][0], E[i + 1][ib][0]
        lo = lower_start(eb) and len(eb.strip()) >= LOWER_MIN
        ne = not ends_sentence(ea) and len(ea.strip()) >= NOEND_MIN
        cont = lo or ne
        oa = ob = None
        if O is not None:
            ka = sum(1 for _, n in O[i] if not n); ma = sum(1 for _, n in E[i] if not n)
            ja, jb = partner(O[i], True), partner(O[i + 1], False)
            if ja is not None and jb is not None and ka == ma:
                oa, ob = O[i][ja][0], O[i + 1][jb][0]
                de = lower_start(ob) or hyphen_end(oa) or not ends_sentence(oa)
                if de and not cont: st['de_yes'] += 1
                if cont and not de: st['de_no'] += 1
        if not cont:
            st['no_join'] += 1
            st['held'] += lower_start(eb) or not ends_sentence(ea)       # a signal fired but was too weak on a short paragraph
            i += 1; continue
        if O is not None and oa is None:
            st['unpaired'] += 1; i += 1; continue
        if O is not None and (oa.startswith('#') or ob.startswith('#')):
            st['pseudo'] += 1; i += 1; continue
        st['both' if lo and ne else 'lower_only' if lo else 'noend_only'] += 1
        mark = syncs[i]
        joined_e, hy = join_english(ea, eb, mark)
        st['hy_e'] += hy
        sample = [clip(ea, tail=True) + ' ' + mark + ' ' + clip(eb) + ('   [English hyphen kept]' if hy else '')]
        if O is not None:
            joined_o, hy = join_original(oa, ob, mark)
            st['hy_o'] += hy
            sample.append(clip(oa, tail=True) + ' ' + mark + ' ' + clip(ob) + ('   [hyphen joined]' if hy else ''))
            moved = [x for x in O[i][ja + 1:]] + [x for x in O[i + 1][:jb]]
            O[i] = O[i][:ja] + [(joined_o, False)] + moved + O[i + 1][jb + 1:]
            del O[i + 1]
        moved = [x for x in E[i][ia + 1:]] + [x for x in E[i + 1][:ib]]
        E[i] = E[i][:ia] + [(joined_e, False)] + moved + E[i + 1][ib + 1:]
        del E[i + 1]
        del syncs[i]
        st['joins'] += 1
        st['samples'].append(sample)
    return st


def process(folder, write):
    fm = facing.parse_yaml(open(f'{folder}/edition.yaml', encoding='utf-8').read())[0]
    layout = facing.front_matter(fm).get('edition_layout', '')
    name = folder.rstrip('/').split('corpus/')[-1]
    if not layout.startswith('photocopy'):
        return name, f'skipped: layout "{layout.split(" (")[0]}"' + (' (no English to read the turn from)' if layout.startswith('original text only') else ''), None
    rd = lambda f: open(f'{folder}/{f}', encoding='utf-8').read() if os.path.exists(f'{folder}/{f}') else None
    o_text, e_text = rd('original.md'), rd('en.md')
    if e_text is None:
        return name, 'skipped: no en.md', None
    O, E, syncs, loose = build(o_text, e_text)
    if (O is not None and text_of(O, syncs) != o_text) or text_of(E, syncs) != e_text:
        raise ValueError('files are not reproduced from their paragraphs')
    st = rejoin(O, E, syncs)
    st['loose'] = loose
    new_o = text_of(O, syncs) if O is not None else None
    new_e = text_of(E, syncs)
    st['labels_ok'] = o_text is None or facing.page_labels(new_o) == facing.page_labels(new_e)
    if write and st['joins']:
        if new_o is not None:
            open(f'{folder}/original.md', 'w', encoding='utf-8').write(new_o)
        open(f'{folder}/en.md', 'w', encoding='utf-8').write(new_e)
    return name, None, st


def samples(lst, n=3):
    if len(lst) <= n:
        return lst
    return [lst[0], lst[len(lst) // 2], lst[-1]][:n]


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    write = '--write' in sys.argv
    for f in args:
        try:
            name, skip, st = process(f.rstrip('/'), write)
        except ValueError as ex:
            print(f'{f}: REFUSED, {ex}'); continue
        if skip:
            print(f'{name}: {skip}'); continue
        print(f"{name}: turns {st['turns']}, joins {st['joins']} (lower+noend {st['both']}, lower only {st['lower_only']}, "
              f"no-sentence-end only {st['noend_only']}), no join {st['no_join']} (held back as too weak {st['held']}), no partner {st['no_partner']}, "
              f"continues but original unpaired {st['unpaired']}, original pseudo-heading {st['pseudo']}, hyphens dropped (original) {st['hy_o']}, kept (English) {st['hy_e']}, "
              f"English joins/German says no {st['de_no']}, English no/German says join {st['de_yes']}, labels {'ok' if st['labels_ok'] else 'DIFFER'}")
        for s in samples(st['samples']):
            for line in s:
                print('     ', line)
