#!/usr/bin/env python3
"""usage: audit_fixes.py [--write] [--samples FILE.md] [slug ...]

The fixes of AUDIT-2026-10-24.md that apply to the edition folders, run once. Each folder is merged into its facing
text (facing.merge_dir), fixed there, and split back (facing.split_text); only files that change are rewritten.
Bardili (paragraphs: printed, already redone) is left alone. Dry run by default.

Every edition
  folios        a misread page number outside a consistent run takes its place in the run (22 read as 2, 129 as 189)
  header        `source:` keeps the provenance but no longer tells you to correct elsewhere (the folder is the source);
                the Conventions paragraph says what this edition's files hold; known missing fields are filled
Editions recovered from a PDF or extracted once from one (the English, or an original-only text)
  running heads the book's running title with its signature ("History of Mexico, Vol. I.   D   because"), standalone or
                glued to the next page by rejoin.py, goes; the page's first words rejoin the previous page
  catchwords    the word repeated before a page mark ("maxims [p. 2] maxims, or") goes
  folio lines   `[PDF n]` + `— 166 —` becomes `[p. 166]`
  drop caps     "T     he" -> "The" when the joined word is a word (or occurs elsewhere in the book)
  joins         a paragraph that stops mid-line is joined to the next one that starts in lower case (never across a
                page mark, heading, note or table line; only when the piece is one printed line, so notes stay apart)
  boilerplate   pages carrying the Google Books notice go (Dacqué)
  in-text heads `## ` inside an original page's OCR goes (Luz, Rubio, Vaz Ferreira)
Single fixes listed in FIXES below (Fries vol. II marks, Klages margins, Vasconcelos note cues, Brentano note 6, ...)."""
import collections, glob, json, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facing

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
args = sys.argv[1:]
WRITE = '--write' in args
SAMPLES = args[args.index('--samples') + 1] if '--samples' in args else None
ONLY = [a for a in args if not a.startswith('--') and a != SAMPLES]
WORDS = set(w.strip().lower() for w in open('/usr/share/dict/words')) if os.path.exists('/usr/share/dict/words') else set()
SKIP = {'bardili-grundriss-der-ersten-logik'}
NOJOIN = {'klages-errungenschaften-nietzsches'}                # its short lines are Nietzsche's verse
HEADER = {                                                     # fields the export could not know
    'luz-y-caballero-obras-1': {'year': '1890'},
    'bachofen-graebersymbolik': {'year': '1859', 'edition': '2nd ed., Basel 1925'},
    'palagyi-logik-auf-dem-scheidewege': {'author_sort': 'Palágyi, Melchior (Menyhért)'},
    'palagyi-ismerettan-alapvetese': {'author_sort': 'Palágyi, Melchior (Menyhért)'},
}
VMETA = json.load(open(f'{ROOT}/originals/vasconcelos-obras-v2/meta.json'))   # English titles, two missing years
MK = r'\[(?:p\. [^\]]+|scan \d+|PDF \d+)\]'
MARK = re.compile(MK)
WIDE = re.compile(r'\S {4,}\S')
NOTE = re.compile(r'^(\(\w{1,3}\)|\d{1,3}\)|\*+\)?|[†‡])\s')
SIG = r'(?:[A-Z]{1,2}\d?|\d{1,3}|[A-Z] ?\d|[a-z]{1,2} ?\d?|[A-Z] i{2,4}j)'    # a signature mark or folio: D, A2, 12, A iij
kind = lambda p: 'm' if MARK.fullmatch(p) else 'q' if p.startswith('>') else 'h' if p.startswith('#') else 'p'


def fix_folios(text, log):
    """as corpus.fix_folios: consecutive repeats of a mark (both languages) count once; a number outside the run that a
    mark within two on each side brackets consistently takes its place in the run"""
    ms = list(re.finditer(r'\[p\. ((?:[IVXL]+\.)?)(\d+)\]', text))
    groups = []
    for m in ms:
        key = (m.group(1), int(m.group(2)))
        if groups and groups[-1][0] == key:
            groups[-1][1].append(m)
        else:
            groups.append([key, [m]])
    fixes = {}
    for i, ((pre, v), mm) in enumerate(groups):
        new = None
        for l in (i - 1, i - 2):
            for r in (i + 1, i + 2):
                if l < 0 or r >= len(groups) or groups[l][0][0] != pre or groups[r][0][0] != pre:
                    continue
                lv, rv = groups[l][0][1], groups[r][0][1]
                if rv - lv == r - l and not lv < v < rv:
                    new = lv + (i - l); break
            if new is not None:
                break
        if new is not None and new != v:
            log['folios'].append(f'{pre}{v} → {pre}{new} (after {groups[i - 1][0][0]}{groups[i - 1][0][1]})')
            groups[i][0] = (pre, new)
            for m in mm:
                fixes[m.start()] = (m.end(), f'[p. {pre}{new}]')
    out, k = [], 0
    for st in sorted(fixes):
        en, new = fixes[st]; out.append(text[k:st]); out.append(new); k = en
    return ''.join(out) + text[k:]


def recovered(P, slug, head, log):
    """the cleanup of a text recovered line by line from a PDF; P = body paragraphs"""
    mono = head.get('translation_language') == 'none'
    side = lambda p: kind(p) == 'p'                             # the recovered text: English, or the original-only text
    # in-text headings inside an original page's OCR
    for i, p in enumerate(P):
        if kind(p) == 'q' and re.search(r'(^|\s)#{2,6} ', p):
            P[i] = re.sub(r'(^|(?<=\s))#{2,6} ', '', p); log['in-text heads'].append(p[:60])
    # Google Books notice pages
    out, page, drop = [], [], False
    for p in P + ['[PDF 0]']:
        if kind(p) == 'm':
            if drop:
                log['boilerplate'].append(' / '.join(x[:50] for x in page[:3]))
            else:
                out += page
            page, drop = [p], False
        else:
            page.append(p); drop = drop or bool(re.search(r'digitized by Google|Google Buchsuche|automatisierten Abfragen', p))
    P = out[:-1] if out and out[-1] == '[PDF 0]' else out
    # printed folio lines after a PDF mark
    out = []
    for p in P:
        f = re.fullmatch(r'[—–-]\s*(\d{1,4})\s*[—–-]', p.strip())
        if f and out and re.fullmatch(r'\[PDF \d+\]', out[-1]):
            log['folio lines'].append(f'{out[-1]} {p} → [p. {f.group(1)}]'); out[-1] = f'[p. {f.group(1)}]'
        else:
            out.append(p)
    P = out
    # running heads: a title at the start of a paragraph, a wide gap, a signature; recurring at least 3 times
    rh = re.compile(rf'^(?P<h>[A-Z][^\n]{{2,50}}?)\s{{4,}}{SIG}(?:\s{{3,}}|\s*(?={MK})|\s*$)')
    heads = collections.Counter(re.sub(r'\s+', ' ', m.group('h').strip()) for p in P if side(p) for m in [rh.match(p)] if m)
    titles = {h for h, n in heads.items() if n >= 3}
    out = []                                                    # \x00 marks a paragraph that now opens mid-sentence
    for p in P:
        m = rh.match(p) if side(p) else None
        if m and re.sub(r'\s+', ' ', m.group('h').strip()) in titles:
            rest = p[m.end():]
            cw = re.match(rf'(\S+)\s+({MK}) (?=\1)', rest)       # the catchword glued on by rejoin.py
            if cw:
                rest = rest[cw.end(1):].lstrip()
            log['running heads'].append(p[:m.end()].rstrip() + (f'  + catchword {cw.group(1)!r}' if cw else ''))
            if not rest.strip() or re.fullmatch(r'\S{1,20}', rest.strip()):   # nothing left but a lone catchword
                continue
            p = '\x00' + rest
        out.append(p)
    P = out
    # catchwords glued on by rejoin.py ("maxims [p. 2] maxims") and standalone ones before a mark
    for i, p in enumerate(P):
        if side(p) and not mono:
            new = re.sub(rf'(?:\s{{2,}}{SIG})?\s{{2,}}(\w+)[,;:]? ({MK}) (?=\1\b)', r' \2 ', p)
            new = re.sub(rf'\b(\w+)[,;:]? ({MK}) (?=\1\b)', r'\2 ', new)
            if new != p:
                log['catchwords'] += [x.group(0) for x in re.finditer(rf'\w+[,;:]? {MK} \w+', p)][:1]
                P[i] = new
    out = []
    for i, p in enumerate(P):
        mk = next((j for j in range(i + 1, min(i + 6, len(P))) if kind(P[j]) == 'm'), None)
        if side(p) and len(p) < 20 and len(p.split()) <= 2 and mk and all(NOTE.match(x) or WIDE.search(x) or kind(x) in 'hq' for x in P[i + 1:mk]):
            nxt = next((x for x in P[mk + 1:mk + 4] if side(x)), '')
            w = re.sub(r'[‐\-­]$', '', p.strip().split()[0]).lower()
            if len(w) >= 2 and nxt.lower().startswith(w):
                log['catchwords'].append(f'{p} ¶ {P[mk]} ¶ {nxt[:30]}')
                continue
        out.append(p)
    P = out
    # drop caps
    body = '\n'.join(P)
    def dc(mo):
        a, frag = mo.group(2), mo.group(3)
        if (a + frag).lower() in WORDS or (len(frag) > 1 and frag.lower() not in WORDS and re.search(rf'\b{a}{frag}\b', body)):
            return (mo.group(1) or '') + a + frag
        return mo.group(0)
    for i, p in enumerate(P):
        if kind(p) in 'pq':
            new = re.sub(r'^(> |\x00)?([A-Z]) {2,}([a-z]+)', dc, p)
            if new != p:
                log['drop caps'].append(f'{p[:24]!r} → {new[:18]!r}'); P[i] = new
    # joins
    out, last = [], 0
    for p in P:
        flag, p = p.startswith('\x00'), p.lstrip('\x00')
        a = out[-1] if out else ''
        b2 = MARK.sub('', p).strip()
        ok = out and side(a) and side(p) and slug not in NOJOIN and not NOTE.match(p) and not NOTE.match(a) \
            and not WIDE.search(a) and not WIDE.search(p) and re.match(r'[a-zà-ÿß]', b2) and re.search(r'[A-Za-zÀ-ÿß,;‐\-]$', a)
        if ok and (last <= 100 or (flag and MARK.match(p))):
            j = a[:-1] + p if a.endswith('‐') else a + p if a.endswith('-') and not MARK.match(p) else a + ' ' + p
            log['joins'].append(f'…{a[-30:]} ¶ {p[:30]}…'); out[-1] = j
        else:
            out.append(p)
        last = len(p)
    return out


def conventions(head, body, mono):
    mk = ['`[p. N]` marks where a printed page begins (its folio as printed' +
          ('; `[p. II.N]` = vol. II' if re.search(r'\[p\. [IVXL]+\.\d', body) else '') + ')']
    if '[scan ' in body:
        mk.append('`[scan N]` a page of the scan with no printed number')
    if '[PDF ' in body:
        mk.append('`[PDF N]` a page of the source PDF with no printed number')
    ot = head.get('original_text', '')
    if mono:
        b = 'the text is the original only (no translation)'
    elif 'not in this file' in ot:
        b = 'the English only; the original is not in this edition (see the scan in the PDF edition)'
    elif 'OCR text layer' in ot:
        b = 'original and English are paired page by page: the original is the OCR of the whole page, not cut at paragraphs'
    else:
        b = 'original and English are paired paragraph by paragraph within each page (in the facing text: original in quoted blocks, English in plain paragraphs)'
    return (f"Conventions: {'; '.join(mk)}; {b}; `*…*` is emphasis as printed; `<sup>…</sup>` a footnote cue, the note "
            f"following its paragraph. This folder is the source: corrections go into its original.md, en.md and edition.yaml.")


def single_fixes(slug, text, log):
    def sub(pat, rep, label, flags=0, count=0):
        nonlocal text
        new, n = re.subn(pat, rep, text, count=count, flags=flags)
        if n:
            log[label].append(f'{n} × {pat[:50]}'); text = new
    if slug == 'fries-neue-kritik-der-vernunft' and '[p. II.' not in text:                 # vol. II restarts at p. 1: [p. II.N], vol. I [p. I.N]
        page = re.compile(r'\[p\. ([\dIVXLCivxlc]+)\]')                 # a real mark, not the `[p. N]` of the Conventions
        last347 = max(m.end() for m in page.finditer(text) if m.group(1) == '347')
        cut = page.search(text, last347).start()
        a = page.sub(r'[p. I.\1]', text[:cut]); b = page.sub(r'[p. II.\1]', text[cut:])
        log['volume marks'].append(f'vol. II from {b[:12]!r}'); text = a + b
    if slug == 'klages-persoenlichkeit':                         # margin debris inside a word at a page turn
        sub(r'(\w+)-\n\n\S{1,4} \[(\d{1,3})\] (\w+)', r'\1\3 [p. \2]', 'margins')          # "ver- ¶ ha [43] schiedenen"
        sub(r'(?<=[\w,;])\n\n\S{1,4} \[(\d{1,3})\] (?=[a-zäöüß])', r' [p. \1] ', 'margins')     # "wiederfinden ¶ no [71] läßt"
        sub(r'(?<!\[p\. )\[(\d{1,3})\]', r'[p. \1]', 'page marks')                              # its inline marks were bare [43]
    if slug.startswith('vasconcelos-'):                         # note cues whose opening tag was lost: "Atentos 1</sup>"
        sub(r' ?(?<!<sup>)\b(\d{1,3})</sup>', r'<sup>\1</sup>', 'note cues')
        sub(r'(?<=[^\W\d])\d{1,3}</sup>(?=<sup>)', '', 'note cues')               # "Norteamérica1</sup><sup>1</sup>"
        sub(r'(?<=[^\W\d])(\d{1,3})</sup>', r'<sup>\1</sup>', 'note cues')
    if slug == 'brentano-psychologie-des-aristoteles':          # the second half of note 6 sat in note 4's English
        m = re.search(r'(\n4\) De Anim\. III, 4\. §\. 5\. p\. 429, b, 5\.[^\n]*?ἀχώριστον γάρ\.)( — Just as he speaks of a being-separate[^\n]*)', text)
        if m and '\n6) De Anim. III, 4. §. 12. p. 430, a, 7.; and De Anim. III, 5. §. 1. p. 430, a, 10. 13. ibid. §. 2. p. 430, a, 19.\n' in text:
            text = text.replace(m.group(0), m.group(1))
            text = text.replace('\n6) De Anim. III, 4. §. 12. p. 430, a, 7.; and De Anim. III, 5. §. 1. p. 430, a, 10. 13. ibid. §. 2. p. 430, a, 19.\n',
                                '\n6) De Anim. III, 4. §. 12. p. 430, a, 7.; and De Anim. III, 5. §. 1. p. 430, a, 10. 13. ibid. §. 2. p. 430, a, 19.' + m.group(2) + '\n')
            log['note moved'].append('note 6 continuation from note 4')
    if slug == 'henriquez-urena-seis-ensayos':                  # running heads inside the original's text
        sub(r'(?<=\S )(?:SEIS ENSAYOS EN BUSCA DE NUESTRA EXPRESIÓN|PEDRO HENRÍQUEZ UREÑA) (?=\S)', '', 'running heads')
        sub(r'(?m)^(> (?:\[scan \d+\] )?)(?:SEIS ENSAYOS EN BUSCA DE NUESTRA EXPRESIÓN|PEDRO HENRÍQUEZ UREÑA) (?=\S)', r'\1', 'running heads')
    if slug == 'luz-y-caballero-obras-1':                       # a word clipped in the recovery (PDF p. 92: "but sown.")
        sub(r'should not be heaped up but so\n', 'should not be heaped up but sown.\n', 'clipped word', count=1)
    return text


def header(slug, text, log, mono):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    fm = m.group(1)
    vm = VMETA.get(re.search(r'^source: ‘([^’]+)’', fm, re.M).group(1), {}) if slug.startswith('vasconcelos-') and re.search(r'^source: ‘', fm, re.M) else {}
    want = dict(HEADER.get(slug, {}))
    want.update({k: v for k, v in vm.items() if k in ('title_en', 'year')})
    for k, v in want.items():
        cur = re.search(rf'^{k}: (.*)$', fm, re.M)
        if cur and cur.group(1).strip('"') == v:
            continue
        log['header'].append(f'{k}: {cur.group(1) if cur else "(none)"} → {v}')
        val = json.dumps(v, ensure_ascii=False) if ':' in v else v
        if cur:
            fm = fm[:cur.start()] + f'{k}: {val}' + fm[cur.end():]
        else:
            anchor = 'author' if k == 'author_sort' else 'year'
            fm = re.sub(rf'^({anchor}: .*)$', lambda mo: mo.group(1) + f'\n{k}: {val}', fm, count=1, flags=re.M)
    src = re.search(r'^source: (.*)$', fm, re.M)
    new = re.sub(r' — THIS FILE IS THE SOURCE, corrections go here| \(generated — edit the page files, not this file\)', '', src.group(1))
    new = new.replace('page files of _facing-pipeline/', 'exported from the page files of _facing-pipeline/')
    if new != src.group(1):
        log['header'].append(f'source: … → {new[:70]}')
        fm = fm[:src.start()] + f'source: {new}' + fm[src.end():]
    head = dict((a.strip(), b.strip().strip('"')) for a, b in (l.split(':', 1) for l in fm.split('\n') if ':' in l))
    rest = text[m.end():]
    yr = head.get('year', '')
    rest = re.sub(r'^\n# (.*?), \*(.*?)\*(?: \((?:[^()]|\([^()]*\))*\))?( — \*.*\*)?$',
                  lambda mo: f'\n# {mo.group(1)}, *{mo.group(2)}*' + (f' ({yr})' if yr else '') +
                  (mo.group(3) or (f" — *{head['title_en']}*" if head.get('title_en') else '')), rest, count=1, flags=re.M)
    if 'Generated file — see the header' in rest[:3000] or 'Generated from the page files' in rest[:3000] or 'Regenerated by export_all' in rest[:3000] or 'This file is the source' in rest[:3000]:
        rest = re.sub(r'^Conventions: .*$', lambda _: conventions(head, rest, mono), rest, count=1, flags=re.M)
        log['header'].append('Conventions paragraph rewritten')
    return f'---\n{fm}\n---\n' + rest


def fix(folder):
    slug = os.path.basename(folder)
    text = facing.merge_dir(folder)
    log = collections.defaultdict(list)
    fm = re.match(r'---\n(.*?)\n---\n', text, re.S).group(1)
    head = dict((a.strip(), b.strip()) for a, b in (l.split(':', 1) for l in fm.split('\n') if ':' in l))
    mono = facing.is_mono(fm)
    text = single_fixes(slug, text, log)
    if re.search(r'recovered from the PDF|\.pdf’', head.get('source', '')):    # text taken line by line from a PDF
        top, body = re.match(r'(---\n.*?\n---\n\n# [^\n]*\n\nConventions:[^\n]*\n\n)(.*)', text, re.S).groups()
        P = [p for p in body.rstrip('\n').split('\n\n') if p.strip()]
        text = top + '\n\n'.join(recovered(P, slug, head, log)) + '\n'
    text = header(slug, text, log, mono)
    return text, log


folders = sorted(os.path.dirname(f) for f in glob.glob(f'{ROOT}/corpus/*/edition.yaml') + glob.glob(f'{ROOT}/corpus/vasconcelos/*/edition.yaml'))
folders = [f for f in folders if os.path.basename(f) not in SKIP and (not ONLY or os.path.basename(f) in ONLY)]
report, samples = [], ['# Audit fixes — samples (dry run)\n', 'Random examples of each change, per edition. `¶` marks a paragraph break that is removed.\n']
for d in folders:
    slug = os.path.basename(d)
    new, log = fix(d)
    y, o, e, ins = facing.split_text(new)
    lo, le = collections.defaultdict(list), collections.defaultdict(list)     # page numbers: each language on its own
    o = fix_folios(o, lo) if o else o
    e = fix_folios(e, le) if e else e
    if lo['folios'] and le['folios'] and lo['folios'] != le['folios']:
        print(f'  {slug}: original and English page-number fixes differ — check', file=sys.stderr)
    if lo['folios'] or le['folios']:
        log['folios'] = le['folios'] or lo['folios']
    files = {'edition.yaml': y, 'original.md': o, 'en.md': e}
    changed = [k for k, v in files.items() if v is not None and v != (open(f'{d}/{k}').read() if os.path.exists(f'{d}/{k}') else None)]
    if not log:
        continue
    report.append(f'{slug}: ' + ', '.join(f'{k} {len(v)}' for k, v in log.items()) + f'  [{", ".join(changed)}]' + (f'  inserted marks {ins}' if ins else ''))
    samples.append(f'\n## {slug}\n')
    rnd = random.Random(slug)
    for k, v in log.items():
        pick = v if len(v) <= 12 else rnd.sample(v, 12)
        samples.append(f'\n**{k}** ({len(v)})\n'); samples += [f'- `{x}`' for x in pick]
    if WRITE:
        for k in changed:
            open(f'{d}/{k}', 'w', encoding='utf-8').write(files[k])
print('\n'.join(report))
if SAMPLES:
    open(SAMPLES, 'w').write('\n'.join(samples) + '\n'); print('samples:', SAMPLES)
print('written' if WRITE else 'dry run — nothing written (use --write)')
