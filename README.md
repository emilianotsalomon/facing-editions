# Facing editions — corpus and reader

The research group's bilingual editions of philosophical texts (German, Spanish, Latin, French, Italian, Hungarian → English), as a text corpus for a knowledge base and as a web reader.

- `corpus/` — one Markdown file per edition: the original in quoted blocks (`> …`), the English in plain paragraphs, `[p. N]` where each printed page begins; a header says where the texts come from and how far they have been checked. `corpus/README.md` lists the editions. `corpus/glossaries/` holds each translation's terminology decisions. `corpus/PROJECT-INSTRUCTIONS.md` is the text to paste into the Claude Project that answers questions from these files.
- The reader site is built by a GitHub Action from `corpus/` on every push (`.github/workflows/pages.yml`, `tools/reader.py`); repository **Settings → Pages → Source: GitHub Actions**. Notes in `corpus/notes/` appear on the pages they name (`corpus/notes/README.md` has the format).
- `docs/` — a local build of the reader: one web page per edition, one card per printed page (or per paragraph pair for the clean-text editions), original left, English right, find-on-page. kept for preview; the published site comes from the Action above.
- The PDF editions themselves (scan beside the English) are on the repository's **Releases** page, not in the repository.
- `originals/` — source files of texts that are not facing editions: the Trendelenburg *Logische Untersuchungen* (German volumes and the translated chapters), Klages's *Persönlichkeit*, and `vasconcelos-obras-v2/`, the Vasconcelos collected works as HTML readers; they come out as `corpus/*.md` and `corpus/vasconcelos/*.md`. Only public-domain texts and the group's own translations belong here.
- `corpus/notes/` — the group's own working notes (concordances, reading notes), kept beside the texts so that they are searched together with them.
- `export_all.sh` — regenerates `corpus/` from the edition work folders (needs the side-by-side-translation skill on the machine); then `reader.py corpus docs` regenerates the reader. Corrections to a translation go into the edition's page files and come through on the next export. For the editions marked "recovered from the PDF" the corpus file is the source and may be edited directly.

All translations are machine-made (Claude) and reviewed against the original by Claude, not by a human translator, unless a file's header says otherwise. Where the header says the original is "OCR, uncorrected", the scan in the PDF edition is the authority.

## Working with the corpus

Claude Project: create a project, paste `corpus/PROJECT-INSTRUCTIONS.md` into its instructions, upload the `corpus/*.md` files and `corpus/glossaries/*.md` as project knowledge, share the project with the group.

Searching directly (any machine with the repository): `grep -n "Vorstellung" corpus/*.md` finds every occurrence with its file and line; the nearest `[p. N]` above gives the printed page.
