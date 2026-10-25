# Idealisms Working Group — shared repository (corpus and reader)

The research group's bilingual editions of philosophical texts (German, Spanish, Latin, French, Italian, Hungarian → English), as a text corpus for a knowledge base and as a web reader.

- `corpus/` — one folder per edition, `corpus/<slug>/`: `original.md` and `en.md` (one language each, `[p. N]` where each printed page begins) and `edition.yaml`, whose header says where the texts come from and how far they have been checked, and `glossary.md` and `notes.md` when they exist. The folder is the source: corrections go into `corpus/<slug>/`; `tools/reader.py` merges the two languages into one facing text (original in quoted blocks `> …`, English in plain paragraphs). `corpus/README.md` lists the editions. Each translation's terminology decisions are in its folder's `glossary.md`. `corpus/PROJECT-INSTRUCTIONS.md` is the text to paste into the Claude Project that answers questions from these files.
- The paragraph standard (editions whose `edition.yaml` says `paragraphs: printed`; the other editions are still paired page by page, see `corpus/README.md`):
  - `original.md` holds the printed paragraphs, never cut at a page turn, with `[p. N]` inline where the page begins; headings are lines starting with `#`.
  - A page mark is `[p. N]` (the edition's own pages) or, for a text cited by a standard edition, that edition's mark: `[AA 4:388]` is page 388 of volume 4 of the Akademie-Ausgabe of Kant. The reader treats both alike (card label `p. 12` or `AA 4:388`); another scheme (Stephanus, Bekker) is one more alternative in `MARKS` in `tools/reader.py`. A heading that opens a page may carry its mark: `## [AA 4:387] Vorrede.`
  - An edition with an `original.md` only (`translation_language: none`) and `paragraphs: printed` is cut for display at its inline marks too, one card per page; a note `[^id]: …` stands under the card of the page that holds its call.
  - `en.md` has exactly one unit (paragraph or heading) per original unit, in the same order, with `[p. N]` inline at the matching point.
  - So paragraph n of one file pairs with paragraph n of the other; the files keep each paragraph whole, and the reader cuts each pair at its shared `[p. N]` marks, one card per printed page.
- The reader site is built by a GitHub Action from `corpus/` on every push (`.github/workflows/pages.yml`, `tools/reader.py`); repository **Settings → Pages → Source: GitHub Actions**. Notes in an edition's `notes.md` appear on the pages they name (`corpus/notes/README.md` has the format).
- `docs/` — a local build of the reader: one web page per edition, one card per printed page (or per paragraph pair for the clean-text editions), original left, English right, find-on-page. kept for preview; the published site comes from the Action above.
- The PDF editions themselves (scan beside the English) are on the repository's **Releases** page, not in the repository.
- `originals/` — source files of texts that are not facing editions: the Trendelenburg *Logische Untersuchungen* (German volumes and the translated chapters), Klages's *Persönlichkeit*, and `vasconcelos-obras-v2/`, the Vasconcelos collected works as HTML readers; they come out as `corpus/*.md` and `corpus/vasconcelos/*.md`. Only public-domain texts and the group's own translations belong here.
- `corpus/notes/` — the group's own working notes (concordances, reading notes), kept beside the texts so that they are searched together with them.
- `export_all.sh` — the owner's local export from the edition work folders (needs the side-by-side-translation skill on the machine). It writes into `staging/` (git-ignored), not into `corpus/`, and runs `tools/split.py` on it: an edition that already has a folder in `corpus/` is skipped (`skipped <slug>: corpus/<slug>/ is the source now; correct it there`), only new editions are moved in. Then `reader.py corpus docs` regenerates the reader. Corrections to a translation go into `corpus/<slug>/`, never into the page files or the staged files.

All translations are machine-made (Claude) and reviewed against the original by Claude, not by a human translator, unless a file's header says otherwise. Where the header says the original is "OCR, uncorrected", the scan in the PDF edition is the authority.

## Annotating in the reader

Select any passage in the reader and a small bar appears: three faded highlight colours, underline, strikeout, and a comment. Comments stand in the right-hand margin next to the passage they belong to; the two switches at the top hide comments, or all annotations, for your own view. Everything is shared: annotations are saved in this repository (`annotations/<text>.json`) and everyone sees them on the next load.

To write annotations (reading needs nothing), click **sign in to annotate** once and paste a GitHub token: github.com → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token; Repository access: only this repository; Permissions: Contents → Read and write. The token stays in your own browser. Your own comments carry a × to delete them; clicking a highlight, underline or strikeout offers to remove it.

## Working with the corpus

Claude Project: create a project, paste `corpus/PROJECT-INSTRUCTIONS.md` into its instructions, upload the generated facing files (`facing/<slug>.md` in the built site, one per edition, downloadable from the site; not `corpus/*.md`) and the `corpus/*/glossary.md` files as project knowledge, share the project with the group.

Searching directly (any machine with the repository): `grep -n "Vorstellung" corpus/*/original.md` finds every occurrence with its file and line; the nearest `[p. N]` above gives the printed page.
