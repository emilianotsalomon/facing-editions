---
title: Translation style guide
author: the group (prepared with Claude)
about: all editions (default where a book's own glossary is silent)
kind: style guide
---

# Translation style guide — philosophical translation into English

The group's general style rulings for the translations in this corpus, with two short model passages at the end. It applies wherever a book's own glossary or policy file (`corpus/glossaries/<book>.md`) is silent; the book's file wins on any point where both speak. Term rulings are in `_general-german-to-english.md` and `_general-spanish-to-english.md`.

The target is a **scholarly reading edition**: accurate first, readable second,
period-faithful throughout. These rulings settle the recurring judgment calls so
they don't get re-decided (differently) every session.

## Register
- Formal, but not archaic. Match the author's own period diction (early-20th-c.
  Spanish; Kant/Hegel-era German) without pastiche.
- Keep the author's sentence architecture where English can bear it. German
  philosophy runs long, hypotactic sentences carrying the argument's joints; do
  not chop every one into short English sentences — you lose the logical
  subordination. Split only when English syntax would otherwise fail.
- Do not "improve," modernize, or de-jargon the author. If he is technical, be
  technical. If he is rhetorical, keep the rhetoric.

## Terminology (the core discipline)
- The glossary is binding for every listed term. **One source term ⇄ one
  English term** for load-bearing vocabulary, across the whole work.
- A term used technically, capitalized, repeated, or scare-quoted is
  load-bearing. Decide it once, apply it everywhere, and add it to the glossary.
- Never let a term drift (e.g. *espíritu* as "spirit" in one paragraph and
  "mind" in the next).

## Foreign & untranslatable terms
- Keep in the original, italicized, with a bracketed English gloss on first
  occurrence: *Einfühlung* [empathy], *Aufhebung* [sublation], *élan* [vital
  impulse]. After the first occurrence, the italic original alone is fine.
- Latin stays Latin and italic: *a priori*, *a posteriori*, *sui generis*.

## Original-term footnotes (flagged terms) — STANDALONE editions only

**Default: OFF.** In a **side-by-side / parallel** edition the original text sits
in the facing column, so a footnote repeating the original word is redundant —
do **not** emit original-term footnotes. Translate flagged terms normally and
leave them unfootnoted.

Emit these footnotes **only** when the output is a **standalone English-only
edition** (no facing original). The mechanism below applies in that mode; the
`FN` glossary flags are inert in side-by-side mode.

- **Which terms fire it (standalone mode):** only glossary entries flagged
  **FN ✓** — contested / load-bearing terms where the original matters (e.g.
  Kant's *Zweckmäßigkeit* → "purposiveness"). Do not footnote unflagged terms.
- **Scope:** by default, **first occurrence per chapter/section only** — once the
  reader has the original, repeats are noise. A glossary entry marked
  **FN ✓ (every)** fires on every occurrence instead.
- **Format:** English term in the text, marker after it, and a note whose entire
  content is the **italicized original**, nothing else:

  > …Kant's notion of purposiveness.[^t1]
  >
  > [^t1]: *Zweckmäßigkeit*

  If the original is a phrase, italicize the whole phrase. Add a gloss only if the
  entry's note says to (e.g. `*Aufhebung* (lit. "sublation")`).

- **Numbering — keep translator notes OUT of the author's footnote stream.**
  Author footnotes keep their numeric labels (`[^1]`, `[^2]`, …) exactly as in the
  source. Translator original-term notes use a **separate `[^t…]` series**
  (`[^t1]`, `[^t2]`, …) so nothing renumbers. In the finished edition these render
  as a distinct stream — e.g. lettered or symbol-marked, or under a "Translator's
  notes" rule — kept visually apart from the author's notes. (If a given edition's
  builder can't render two streams, fall back to a single numeric stream and
  renumber everything together — but say so.)

## Quotations, italics, emphasis
- Preserve the author's italics and his scare quotes exactly.
- Render Spanish «guillemets» and German „low quotes" as English "double
  quotes." Keep quotation nesting.
- Block quotations of other philosophers: translate them too (unless they are
  bibliographic titles — see below), keeping the author's attribution.

## Apparatus — keep the scholarly furniture intact
- **Page markers**: reproduce `[116]`, `[117]`, … exactly where they fall in the
  source. They anchor the side-by-side alignment.
- **Footnotes**: keep anchors `[^n]` at the same points; keep the notes in order.
- **Cited titles in footnotes stay in their original language** — do NOT
  translate book/article titles (`Der goldene Schnitt`, `Teoria generale e
  formale del Valore`). Translate only surrounding prose ("Obra citada" → "op.
  cit." or "cited work", chosen once).

## OCR reality
- The source is often OCR'd and dirty (`sli`, `hibertad`, `MtUIIónS`). Silently
  correct obvious OCR garble to the intended word **only when it is
  unambiguous**. When a garble could be more than one word, or drops text,
  render your best reading and flag it: `⟨translator note: OCR unclear, read as
  "libertad"⟩`.
- Never fabricate content to bridge a gap the OCR dropped. Mark the gap.

## When you are unsure
- Leave an inline `⟨translator note: …⟩` for any genuine interpretive fork, any
  term you had to coin, or any place two readings are defensible. These are for
  the editor to adjudicate; they are cheap and they are the point.

## Output shape
- English only, paragraph-for-paragraph with the source (1:1), so it drops
  straight into the side-by-side / parallel-edition pipeline.
- After the translation: a short **"New glossary terms"** list (term → ruling →
  one-line reason) and any **notes**.

## Model passages (exemplars)

Two short passages that show register, sentence handling and term discipline.

### Spanish — Deustua, *La estética contemporánea* (1924; the original is in the public domain, the English is the group's own)

> Bajo la influencia de la filosofía intelectualista, que ha dominado hasta los últimos tiempos, las ideas estéticas han girado al rededor del concepto de armonía, que es una modalidad del concepto de orden, engendrado por el funcionamiento lógico del espíritu. […] Tres ideas fundamentales han contribuído a su nacimiento: las ideas de valor, de creación y de intuición.

Under the influence of the intellectualist philosophy that has dominated until recent times, aesthetic ideas have revolved around the concept of harmony, which is a modality of the concept of order, engendered by the logical functioning of the spirit. […] Three fundamental ideas have contributed to its birth: the ideas of value, of creation, and of intuition.

What to copy from it:
- *espíritu* → **spirit** throughout (never "mind"); *libertad* → **freedom**; *orden* → **order**; *valor / creación / intuición* → **value / creation / intuition**.
- A long Spanish periodic sentence kept as one long English sentence: the subordination is the argument.
- Page markers reproduced exactly where they fall in the source.
- Block quotations of other authors translated, attribution kept.

Corrections logged from the human draft of this text (the rulings exist to prevent these): *pancalismo* had been rendered "panlogism", it must be **pancalism**; *notas de la imaginación* had been rendered "notes", it must be **marks / characteristics of the imagination**.

### German — term discipline

> *Gedanken ohne Inhalt sind leer, Anschauungen ohne Begriffe sind blind.* (Kant, *Kritik der reinen Vernunft*; public-domain original)

What to copy from it, with the group's own English wording: *Anschauung* → **intuition** (not "perception"); *Begriff* → **concept**; parallel clause structure preserved; one German term ⇄ one English term, held across the whole work. (The English line that accompanied this sentence in the working file was the standard published rendering and is not reproduced here.)
