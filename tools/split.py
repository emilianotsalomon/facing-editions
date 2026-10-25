#!/usr/bin/env python3
"""usage: split.py [--into corpus] corpus/<slug>.md [corpus/vasconcelos/<slug>.md ...]

Turns an interleaved edition into a folder (see facing.py for the layout): edition.yaml, original.md, en.md; the
edition's glossary (corpus/glossaries/<rel>.md) and notes (corpus/notes/<rel>.md) move in as glossary.md and notes.md,
and the interleaved file is removed (reader.py generates it again, as facing/<rel>.md on the site).
Refuses when the folder exists, or when the file cannot be split without changing what the reader shows.
With --into DIR (export_all.sh: the files are staged in staging/, the folders live in DIR = corpus/) the folder is made in DIR, and an
edition that already has its folder there is skipped with a message, never touched: the folder is the source, corrections go into it.
A staged file that cannot be split (the Trendelenburg originals, with quoted footnotes) is copied to DIR/<name>.md as the flat file it is.
For every edition it reports whether merging the folder gives back the old file byte for byte, and whether en.md
carries the same page marks, in the same order, as the original side."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facing


def corpus_root(path):
    d = os.path.dirname(os.path.abspath(path))
    for c in (d, os.path.dirname(d)):
        if os.path.basename(c) == 'corpus' or os.path.isdir(f'{c}/glossaries') or os.path.isdir(f'{c}/notes'):
            return c
    return d


def split_file(path, into=None):
    path = os.path.abspath(path)
    root = corpus_root(path)                     # where the file and its glossaries/notes stand
    rel = os.path.relpath(path, root)[:-3]
    dest = into or root
    folder = f'{dest}/{rel}'
    if os.path.exists(folder):
        if into:
            return f'skipped {rel}: corpus/{rel}/ is the source now; correct it there'
        return f'{rel}: REFUSED, {folder} exists'
    text = open(path, encoding='utf-8').read()
    try:
        y, o, e, inserted = facing.split_text(text)
        merged = facing.merge_parts(y, o, e)
    except (facing.Unsplittable, ValueError) as ex:
        if into:
            os.makedirs(os.path.dirname(f'{dest}/{rel}.md'), exist_ok=True)
            shutil.copy(path, f'{dest}/{rel}.md')
            return f'{rel}: cannot be split ({ex}); copied to {dest}/{rel}.md as a flat file'
        return f'{rel}: REFUSED, {ex}'
    os.makedirs(folder)
    for name, content in (('edition.yaml', y), ('original.md', o), ('en.md', e)):
        if content is not None:
            open(f'{folder}/{name}', 'w', encoding='utf-8').write(content)
    for src, name in ((f'{root}/glossaries/{rel}.md', 'glossary.md'), (f'{root}/notes/{rel}.md', 'notes.md')):
        if os.path.exists(src):
            shutil.move(src, f'{folder}/{name}')
    os.remove(path)
    pages = facing.page_labels(o) if o else facing.page_labels(e)
    marks = 'marks ok' if e is None or pages == facing.page_labels(e) else \
        f'MARKS DIFFER (original side {len(pages)}, en.md {len(facing.page_labels(e))})'
    return (f'{rel}: ' + ('round trip identical' if merged == text else 'round trip DIFFERS (interleaving order or an empty quote)')
            + f', {marks}' + (f', {len(inserted)} marks added to en.md' if inserted else ''))


if __name__ == '__main__':
    args, into = sys.argv[1:], None
    if args[:1] == ['--into']:
        into, args = os.path.abspath(args[1]), args[2:]
    results = [split_file(p, into) for p in args if os.path.isfile(p) and os.path.basename(p) != 'README.md']
    print('\n'.join(results))
    sys.exit(1 if any('REFUSED' in r for r in results) else 0)
