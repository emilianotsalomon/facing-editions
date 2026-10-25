# Repeated passages in the Vasconcelos corpus: where they occur and how far they overlap

This report covers every work in this folder (37 texts).
- **Same-language overlap (Spanish–Spanish)** was found by machine: every 6-word sequence in every text was matched against every other text, the hits were chained into blocks, and each block's word-level similarity was measured. A looser second pass compared vocabulary paragraph by paragraph, to catch passages that were rewritten rather than reprinted.
- **Cross-language overlap (English–Spanish)** can't be found that way. Each English text was read against its likely Spanish sources, and the matches were confirmed with anchor phrases. A sample of anchors was re-checked against the files.

**How to read locations.** "¶n" is the paragraph number in the plain-text extraction of each HTML file (blank-line separated). It lines up with the paragraph order in the HTML. "p." is the original pagination where the file carries `[n]` markers. *Ideario de acción*, the *Mensaje* of 1924, *El Día del Maestro*, *Los últimos cincuenta años* and *Reneguemos* have no reliable markers.

**Classes.**
- **VERBATIM**: the same printed text (≥95% word identity; differences are OCR or typesetting).
- **TRANSLATION**: a close sentence-by-sentence translation.
- **VERSION**: the same passage freely rewritten; most sentences have counterparts.
- **PARTIAL**: some sentences or arguments carried over.
- **THEMATIC**: the same idea or example only. These are listed only briefly.

---

## 1. Summary

| Text A | Text B | Class | Size of overlap | Share of A | Share of B |
|---|---|---|---|---|---|
| *Ideario de acción* | *Discursos 1920–1950* | VERBATIM | 6 pieces, ~10,600 words | **~38%** | ~10% |
| *Ideario de acción* §11 | "Education in Mexico" (1922, Eng.) | TRANSLATION | whole lecture, ~7,500 words (Sp.) | ~27% | **~98–100%** |
| *El Día del Maestro* | *Discursos* | VERBATIM | ~2,800 words | **~93%** | ~2.7% |
| *La filosofía de la coordinación* (1949) | *Todología* | VERBATIM / near-verbatim | ~1,500 words | **~85%** | ~1.7% |
| *Mensaje* (1924) | "Some Ways…" (1924, Eng.) | TRANSLATION (abridged) | — | **~100%** of the *Mensaje* | **~61%** of the English |
| "The Esthetic Development of Creation" (1949, Eng.) | *Todología* | TRANSLATION / VERSION + PARTIAL | ~800 words close + ~450 partial | **~27% close; ~40–45% any** | <1% |
| *Aspects of Mexican Civilization* (1926, Eng.) | *Indología* (1926) | TRANSLATION / VERSION / PARTIAL | ~4,600 words (Eng.) | **~20%** (5% close) | ~5% |
| *Discursos* | *Todología* | VERBATIM | ~680 words | <1% | <1% |
| *Ideario de acción* §5 | *La raza cósmica* (travel part) | VERBATIM | ~560 words | ~2% | <1% |
| "Education in Mexico" | *Orientaciones* (1922) | PARTIAL / VERSION | arguments and examples reused | ~30% partial | — |
| "A Mexican's Point of View" (1927, Eng.) | *Bolivarismo y monroísmo*; *Los últimos cincuenta años* | PARTIAL only | scattered | ~8–10% | <1% |
| *Estética* | *Lógica orgánica* | VERBATIM / PARTIAL | 6 short blocks, ~330 words | <1% | <1% |
| *Estética* | *El realismo científico* | VERBATIM (shared quotations) | 3 blocks, ~180 words | <1% | <1% |
| *La revulsión de la energía* (1924) | *Tratado de metafísica* | VERSION (2 passages) | ~2 paragraphs | small | small |
| "Educational Aspirations" (1924, Eng.) | — | none (thematic echoes in *Indología*) | — | 0% | — |
| "Why I Became a Magazine Editor" (1932, Eng.) | — | none | — | 0% | — |

No verbatim overlap was found among *La raza cósmica*, *Indología*, *Bolivarismo*, the *Metafísica*, the *Ética*, the *Estética* and *De Robinson a Odiseo*, apart from the short items listed above. The loose vocabulary pass turned up no further rewritten passages in Spanish beyond those in §4.

---

## 2. Spanish–Spanish reprints

### 2.1 *Ideario de acción* ↔ *Discursos 1920–1950*

Six pieces of *Ideario* are reprinted in *Discursos*. Word identity is 95–98%; the differences are OCR and spelling.

| *Ideario* | *Discursos* | Piece | Words shared | Similarity |
|---|---|---|---|---|
| §2, ¶43–58 | ¶264–286 (pp. 65–76), cap. 13 | "Mensaje a la juventud peruana" / "A los estudiantes de Trujillo" (13 Feb 1924) | 3,946 | 0.96 |
| §3, ¶60–82 | ¶247–259 (pp. 57–64), cap. 12 | "Carta a la juventud de Colombia" (to Germán Arciniegas) | 2,670 | 0.96 |
| §6, ¶105–111 | ¶236–242 (pp. 54–56), cap. 11 | "En la fiesta de la raza", speech of 12 Oct 1918 | 582 | 0.97 |
| §7, ¶115–129 | ¶329–341 (pp. 92–97) | "El bronce del indio mexicano…": the Cuauhtémoc statue speech, Rio de Janeiro | 2,186 | 0.98 |
| §9, ¶165–170 | ¶360–366 (pp. 100–103) | "Carta a Romain Rolland" (4 Feb 1924) | 1,206 | 0.95–0.96 |

Notes:
- *Discursos* ¶380–390 is *El Día del Maestro* (§2.2), not an *Ideario* piece.
- In the *Ideario* §2 block, the *Discursos* paragraphs are split differently, so the fuzzy paragraph scores there (0.52–0.9) understate the match. The word-level identity across the block is 0.96.

**Parts of *Ideario* not reprinted in *Discursos*:**
- §1 "Inicial biográfico" (¶8–41, an introduction about Vasconcelos)
- §4 "Discurso de bienvenida" (¶84–95)
- §5 "Discurso dicho en Chile" (¶96–102, but see §2.3)
- §8 "Nueva ley de los tres estados" (¶131–163, ~4,000 words)
- §10 "Himnos breves" (¶172–209)
- §11 "La educación en México" (¶210–268, which is the translation of the 1922 English lecture; see §3.1)

So §8, the most important doctrinal piece in *Ideario* for the race-and-spirit question, appears **only** there.

### 2.2 *El Día del Maestro* ↔ *Discursos*

- *El Día del Maestro* ¶10–35 ≈ *Discursos* ¶380–390 (pp. 106–114). 2,807 shared words, similarity 0.96.
- It begins "Figuras de maestras que pasan por mi memoria…".
- This is about **93%** of *El Día del Maestro*.

### 2.3 *Ideario* §5 ↔ *La raza cósmica*

- *Ideario* ¶98–101, the speech on receiving the honorary professorship in Santiago de Chile ("EL honor que se ha servido conferirme la Facultad…"), is reproduced verbatim inside the travel narrative of *La raza cósmica*, ¶536–539 (pp. 261–262).
- 557 shared words, similarity 0.97.

### 2.4 *La filosofía de la coordinación* (1949) ↔ *Todología*

| *Coordinación* | *Todología* | Words shared | Similarity | Content |
|---|---|---|---|---|
| ¶8–10 (p. ~865–866) | ¶140–142 (pp. 49–50) | 366 | 0.97 | "El silencio es al sonido lo que la luz blanca al color…" ("El secreto del sonido") |
| ¶11–14 (p. 866) | ¶80–83 (pp. 34–35) | 308 | 0.95 | "Las formas específicas del conocer como acción" |
| ¶16 (p. 867) | ¶173 (p. 62) | 39 | 0.85 | Empedocles as forerunner of the philosophy of coordination |
| ¶17–22 (pp. 867–869) | ¶176–181 (pp. 63–66) | 800 | 0.80 | "dos peras y dos manzanas…" |

That is about 85% of the congress paper. The last block was revised more heavily than the others.

### 2.5 *Discursos* ↔ *Todología*

- *Discursos* ¶944–949 (pp. 315–317), "Del Logos al Verbo", ≈ *Todología* ¶663–667 (pp. 183–185). Shared: 562 words, similarity 0.97. *Todología* introduces it with "En discurso reciente expresé:".
- *Discursos* ¶855–856 (p. 281) ≈ *Todología* ¶159–160 (p. 56). Shared: 118 words, similarity 0.71, revised.

### 2.6 Short shared blocks in the systematic works

- ***Estética* ↔ *Lógica orgánica*.** Six blocks of 32–89 words, similarity 0.57–1.00. All are on sound, interval, chord and counterpoint:
  - *Estética* ¶274–275 (p. 82) ↔ *Lógica* ¶492–493 (pp. 150–151)
  - ¶754 (p. 197) ↔ ¶501 (p. 153)
  - ¶808 (p. 210) ↔ ¶505 (p. 154)
  - ¶812 (pp. 210–211) ↔ ¶506 (p. 154)
  - ¶822 (p. 215) ↔ ¶514–515 (p. 156)
  - ¶834–835 (p. 217) ↔ ¶517–518 (p. 156)
- ***Estética* ↔ *El realismo científico*.** Three blocks, ¶889, ¶892 and ¶917 (pp. 228–236) ↔ ¶121–123. These are mostly the same quotations from Gley and on muscular oscillation, with one framing paragraph (¶892 ↔ ¶123, similarity 0.83).
- ***Lógica orgánica* ¶533 (p. 159) ↔ *Todología* ¶496 (p. 149).** 66 words, similarity 0.97: "las almas humanas que no llegan al conocimiento de la verdad sino discursivamente…".
- ***Lógica orgánica* ¶468 ↔ *Todología* ¶392.** PARTIAL: the same sentence on the helium atom inside differently framed paragraphs.

---

## 3. English–Spanish correspondences

### 3.1 "Education in Mexico: Present Day Tendencies" (Washington, 1922) ↔ *Ideario* §11 "La educación en México"

**A complete translation (TRANSLATION, ~98–100% of the body).** The English text runs in the same order as *Ideario* ¶210–257; only the editorial front matter (Eng. ¶1–9) is missing.

| Eng. ¶ | *Ideario* ¶ | Note | Anchor (Eng. / Sp.) |
|---|---|---|---|
| 10 | 212–214 | | "To educate is to prepare men and women for a certain social purpose" / "Educar es preparar al individuo para determinado propósito social" |
| 13 | 215–216 | Spanish adds a sentence on Díaz | "his facial angle was not up to such and such Norwegian or Scottish standards" / "su ángulo facial no correspondía a tales o cuales normas propias del tipo escocés o noruego" |
| 20–22 | 220–224 | Spanish adds Madero's 12 million | "dismissing soldiers and recruiting teachers" / "licenciar soldados y reclutar maestros" |
| 25 | 225–229 | | "We saved in doctors in order to buy food" / "lo que ahorramos en médicos lo gastamos en pan" |
| 31–49 | 232–249 | | e.g. "200,000 bound volumes of Homer, Plato…" / "doscientos mil volúmenes empastados, de Homero, Platón…" |
| 52–55 | 250–254 | | "I preferred music to the methodology of music" / "preferimos la música a la metodogía de la música" |
| 58 | 255 | VERSION, ~70%: the school building is described differently | "not merely schools but social centers" / "no solamente escuelas, sino centros sociales" |
| **61–62** | **256–257** | Spanish says "veinte naciones" and drops "perhaps the Hindu" | "race sentiment is even more important than patriotism" / "el sentimiento de raza es más vigoroso aún que el patriotismo" |

**Secondary: *Orientaciones* (Córdoba lecture, 5 Oct 1922).** This is a different lecture that reuses the same examples. PARTIAL or VERSION covers about 30% of the English. The closest matches:
- Eng. ¶52 ↔ Orient. ¶22–23 (pp. 22–24): VERSION, ~75%. "a very real and larger unity would be found in the mind of the pupil" / "ha ido a refugiarse a la conciencia del alumno".
- Eng. ¶31 ↔ Orient. ¶18 (pp. 17–18): PARTIAL.
- Eng. ¶54 ↔ Orient. ¶25 (pp. 25–26): PARTIAL.
- Eng. ¶61–62 ↔ Orient. ¶31, ¶35–38 (pp. 32–38): PARTIAL, ~25%. "Our differing capacities make life more interesting" / "por sus distintas aptitudes enriquecen el acervo común".

### 3.2 "Some Ways…" (Texas, 1924) ↔ *Mensaje* (1924, *Nueva Democracia*)

**The *Mensaje* is an abridged Spanish translation of the English address.** Every part of the *Mensaje* has an English counterpart. The English section ¶14–22 (pp. 778–781, ~1,600 words, on religion, leisure, labour and capital) has no Spanish counterpart anywhere in the corpus.

| Eng. ¶ (pp.) | *Mensaje* ¶ | Class | Anchor |
|---|---|---|---|
| 4–5 | 5–6 | TRANSLATION | "the first university of America that tendered free scholarships" / "la primera de las universidades americanas que ofreció becas" |
| 6 | 7 | PARTIAL (names of professors dropped) | — |
| 7–13 (776–778) | 10–20 | TRANSLATION | "The tribe has grown into the state" / "La tribu se ha desarrollado hasta convertirse en estado" |
| 14–22 (778–781) | — | none | — |
| 23–26 (781) | 24–29 | TRANSLATION | "No more blind hates, no more race prejudice" / "Ya no más odios ciegos; ya no más odios de raza" |
| **27–28 (782)** | **30** | TRANSLATION ("ethical" rendered as "estética") | "we Mexicans are very few and ill-armed" / "nosotros los mexicanos somos pocos y mal armados" |

Coverage: about 61% of the English body by word count.

### 3.3 "The Esthetic Development of Creation" (1949, tr. Eliseo Vivas) ↔ *Todología*

The English text has two halves:

- **¶6–16, the aesthetic a priori: mostly English-only.**
  - ¶6 has PARTIAL counterparts in *Todología* ¶81–82, ¶187, ¶192, and in *Coordinación* ¶12–13 (the march and the horse's four hooves).
  - ¶16 has a PARTIAL counterpart in *Coordinación* ¶8–9 and *Todología* ¶140–141 (Pythagoras, silence and white light). The argument is condensed and runs the other way.
  - ¶7–15 (melody, harmony, Eros, love's affinity in place of gravitation) have no Spanish counterpart.
- **¶17–28, "Philosophy of Coordination" and "Unity and Truth": close translation of *Todología* pp. 48–53, in a different order.**

| Eng. ¶ | *Todología* ¶ (pp.) | Class | Anchor |
|---|---|---|---|
| 18 | 144 (50) | VERSION, ~80% | "I first took it up in my Aesthetics, published in 1937" / "En mi Estética, publicada por el 1937, apunté la solución" |
| 19 | 145 (50) | TRANSLATION, ~40% of ¶ | "to think, for modern man, no longer consists in the reduction of the particular to the general" / "pensar, para el hombre moderno, ya no es reducir lo particular a lo general" |
| 20 | 147 (50–51), 150 (52–53) | TRANSLATION / VERSION | "about man we see drawn a series of circles or zones of reality" / "en torno al hombre vamos deslindando una serie de círculos o zonas de realidad" |
| 21–22 | 154–155 (53) | TRANSLATION, 100% | "Truth presupposes diverse manners of unification" / "la verdad supone diversas maneras de unificación" |
| 23–24 | 168, 173, 176 (60–64) | PARTIAL, ~35–40% | Empedocles; "Do not try to reduce quality" / "No intentes reducir la calidad" |
| 25–28 | 133–137 (48–49) | TRANSLATION | "We do not say 'to unify' but 'to coordinate.'" / "Nosotros no decimos unificar sino coordinar" |

Coverage: about 27% close (TRANSLATION or VERSION), about 40–45% with any counterpart.

### 3.4 *Aspects of Mexican Civilization* (Harris lectures, Chicago 1926) ↔ *Indología* (1926)

About 20% of the English (≈4,600 of 22,100 words) has a Spanish counterpart, and only about 5% is close translation. Nearly all of it is in *Indología*.

| Lecture | Share with counterpart | Where |
|---|---|---|
| I "Similarity and Contrast" (¶9–54) | ~20% | *Indología* §"La Tierra", ¶159–174 (pp. 45–55); *La raza cósmica* ¶162 (Minas Geraes) |
| II "Democracy in Latin America" (¶56–99) | ~8% | scattered: *Ind.* ¶183, ¶278, ¶311–318, ¶369–370. Essentially English-only. |
| III "The Race Problem" (¶101–123) | ~35% | *Indología* §"El Hombre", ¶203–234 (pp. 70–94), in the same order as the English from ¶221 on |

Closest correspondences:

| Eng. ¶ (pp.) | *Indología* ¶ (pp.) | Class | Anchor |
|---|---|---|---|
| 38–39 (27–29) | 173–174 (54–55) | TRANSLATION, ~80–85% | "Our psychology as a rule is the psychology of the gambler" / "nuestra psicología sea como la del jugador" |
| 16–21 (9–13) | 170 (52–53) | VERSION, condensed | the four-colour map: "a golden yellow over all the section of the highland" / "un amarillo de oro, ara todo el altiplano" |
| 26 (16–19) | 115 (12–14) | VERSION, ~50% | the Guianas, "three first-class races" / "tres razas de primera" |
| 103 (76–77) | 221 (86–88) | TRANSLATION, ~80% | "Civilizations come and go" / "Las civilizaciones, en efecto, van y vienen" |
| 104 (77–79) | 221–222 (88) | TRANSLATION, first half | "Call it, if you will, a decayed stock, but not a primitive stock" / "Podrán acaso constituir casos de decadencia" |
| **107 (81–82)** | **224 (89)** | VERSION, ~50% (Cortés and Malintzin missing) | Garcilaso: "to make one mind of the two conflicting mentalities" / "hacer una sola alma con el conflicto" |
| 110 (85–86) | 208–209, 228 (76–77, 91) | VERSION, scattered | "race prejudice as it exists today is a comparatively modern feeling" / "El prejuicio del color de la piel es más bien un sentimiento moderno" |
| 111 (86–87) | 226 (90) | VERSION, ~55% | "as completely strangers in India as on the day their ancestors first landed" / "los ingleses siguen siendo en la India extranjero invasores" |
| 114 (89–91) | 232 (92–93) | VERSION, ~50% | the Zapatista Indian revival |
| 122 (99–101) | 234, 255, 406 | VERSION / PARTIAL, ~40% | "quality predominates over numbers" / "la América quiere calidad más bien que número" |

Notes:
- **Direction.** *Indología* ¶221 starts a close translation of English ¶103 abruptly, partway into a paragraph on immigration. *Indología* seems to have taken in lecture text, or both draw on a common draft. The English ¶26 says the Guianas argument had already been presented "to a learned audience", and *Indología* ¶115 is that version.
- ***Bolivarismo y monroísmo* (1934)** has no textual counterpart to *Aspects*. It often takes the opposite position (e.g. on Indian cultural revival).
- **English-only material of note:**
  - all of Lecture II's account of caudillismo and *facultades extraordinarias*;
  - Lecture III ¶115 (Carranza, Obregón and Villa as mestizos; Juárez's mestizo-Indian alliance);
  - the "substitution of Mendelism for Darwinism" programme (¶120);
  - the "soul-map" of the continent (¶31).

### 3.5 English texts with no Spanish counterpart in the corpus

- **"A Mexican's Point of View" (1927).** No translation or version. About 8–10% has PARTIAL counterparts, rewritten from scratch and often in a harsher tone:
  - *Bolivarismo* §"La revolución mexicana", ¶246–321 (pp. 123–146), and ¶52–58 (pp. 22–25);
  - *Los últimos cincuenta años* ¶58–59 (Aguascalientes, preconstitutionalism, Querétaro).
  The judgement of Woodrow Wilson is favourable in 1927 and reversed in *Bolivarismo*. Anecdotes found only in English: San Antonio with Madero, Niagara, Vasconcelos as the Convention's agent in Washington, Veracruz 1914.
- **"Educational Aspirations" (*The Survey*, 1924).** No translation. About a third of its points recur thematically in *Indología*'s education chapter (¶321–351, pp. 156–185). *Indología* ¶332–333 shares the "50,000 Quixotes" figure.
- **"Why I Became a Magazine Editor" (*Books Abroad*, 1932).** No counterpart, only thematic echoes (the "homogeneous race" of Ideario ¶74 and Indología ¶119).

---

## 4. Spanish rewritings (not verbatim)

| Earlier | Later | Class | Anchor |
|---|---|---|---|
| *La revulsión de la energía* (1924) ¶39 (p. 553) | *Tratado de metafísica* ¶1042 (p. 237), "Conclusiones" | VERSION (35 of ~60 words identical, similarity 0.56) | "La energía, una en esencia, no obedece, sin embargo, a los mismos ritmos de movimiento en todas sus manifestaciones" |
| *La revulsión de la energía* ¶33 (Trinity) | *Tratado de metafísica* ¶1104 | VERSION (reworded) | "La Trinidad es ritmo de creación" / "el mismo signo trino del ritmo ascendente … Padre, Hijo y la síntesis" |
| *Orientaciones* 1922 ¶22 (pp. 22–23) | *Ideario* ¶251 | PARTIAL (the same account of the Bellas Artes department and teachers of drawing and music) | — |

---

## 5. The race-and-spirit passages (from `raza-y-espiritu-pasajes.md`) that recur elsewhere

| Passage | Other location(s) | Class |
|---|---|---|
| *Ideario* ¶71 ("dar expresión a cada raza conforme a su misión… camino distinto para la revelación de lo divino") | *Discursos* ¶252 (pp. 59–60) | VERBATIM (Carta a Colombia) |
| *Ideario* ¶75 ("la estirpe, es decir, el tipo de cultura… raza superior y nosotros unos mestizos") | *Discursos* ¶254 (pp. 60–62) | VERBATIM |
| *Ideario* ¶80 ("rancio espíritu castellano… razas creadoras") | *Discursos* ¶257 | VERBATIM |
| *Ideario* ¶98 ("las razas tienen el derecho de organizarse… según sus simpatías y sus gustos") | *La raza cósmica* ¶536 (p. 261) | VERBATIM (Chile speech) |
| *Ideario* ¶121 ("la nueva raza latina… una en la sangre y en el anhelo") | *Discursos* ¶333 (p. 95) | VERBATIM (Cuauhtémoc speech) |
| *Ideario* ¶126 ("queremos dejar de ser colonias espirituales… alma propia") | *Discursos* ¶338 (pp. 96–97) | VERBATIM |
| *Ideario* ¶165 ("latinidad… que acoja en su seno a todas las razas") | *Discursos* ¶362 (p. 100) | VERBATIM (Rolland letter) |
| *Ideario* ¶169 ("estamos forjando con la raza nueva, un nuevo concepto de vida") | *Discursos* ¶365 (pp. 102–103) | VERBATIM |
| *Ideario* ¶257 ("el sentimiento racial… procede de hondas diferencias espirituales") | "Education in Mexico" ¶61–62 (pp. 244–245) | TRANSLATION (same text, 1922) |
| *Mensaje* 1924 ¶30 ("raza o más bien un tipo de civilización… murallas que separan las almas") | "Some Ways" ¶27–28 (p. 782) | TRANSLATION |
| *Aspects* ¶107, Garcilaso ("spiritual blending") | *Indología* ¶224 (p. 89) ("hacer una sola alma") | VERSION, ~50% |
| *Aspects* ¶111 ("strangers in India") | *Indología* ¶226 (p. 90) ("conquista de almas") | VERSION, ~55%. The "conquista de almas" sentence is Spanish-only. |
| *Aspects* ¶114 (Spanish spirit victorious over the native) | *Indología* ¶232 (pp. 92–93) ("el espíritu europeo ya se impuso") | VERSION, ~50% |
| *Aspects* ¶103 ("flesh and the soul of the high-type ancestors") | *Indología* ¶221 (pp. 86–88) ("en la carne y en el alma la herencia") | TRANSLATION, ~80% |
| *Aspects* ¶122 (quality over number) | *Indología* ¶234, ¶255, ¶406 | VERSION / PARTIAL |
| *Aspects* ¶116 ("blending of two different souls") | *La raza cósmica* ¶72 ("maleabilidad, comprensión rápida y emoción fácil") | THEMATIC only. The "two souls" formula is English-only. |
| *Aspects* ¶123 ("Spiritual affinities and similar fancies of taste") | *Indología* ¶230; *La raza cósmica* ¶52 | THEMATIC |

**Passages that appear only once in the corpus:**
- *Ideario* §8 "Nueva ley de los tres estados": ¶133, ¶135, ¶147, ¶158 and ¶162, including "una estirpe se constituye, más bien que por la sangre, por las ideas".
- Every *La raza cósmica* prologue passage ("mendelismo espiritual", "factor espiritual", "eugenesia estética").
- Every *Indología* passage not listed above, including ¶207 ("cada alma logra moldear su propia estructura externa"), ¶244 ("concepto de raza que no se ciñe a una sangre"), ¶134 ("fusión espiritual") and ¶406 ("con-fusión de las sangres").
- The *Ética* and *Estética* passages.
- The *Discursos* passages ¶573–576 (Día de la Raza, "alianzas del espíritu"), ¶658 (the Tabasco "yerro") and ¶803 ("linaje de espíritu").
- The 1924 *Revulsión* §3.

---

## 6. Limits

- The verbatim detector needs runs of six identical words. Heavy OCR damage inside a passage (e.g. "pue. blos") can split a block in two, but it does not hide a reprint.
- The loose pass compares vocabulary paragraph by paragraph. It catches rewritten paragraphs but not a single sentence moved into an otherwise different paragraph.
- The English–Spanish percentages are a reader's estimates weighted by paragraph length, not measurements.
- English page ranges in *Aspects* may be off by one page, because its folio markers are partly duplicated in the OCR.
- Works outside this folder (e.g. the *Ulises criollo* cycle, *Qué es el comunismo*, the *Breve historia de México*) were not checked.
