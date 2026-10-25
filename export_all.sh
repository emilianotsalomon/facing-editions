#!/bin/sh
# Regenerates the editions from the page files (and, for editions whose page files were not kept, from their PDFs) into staging/ (git-ignored),
# then tools/split.py moves only the editions that have no folder in corpus/ yet; an existing corpus/<slug>/ is the source and is skipped.
# Run after any edition changes:  sh export_all.sh        (needs the side-by-side-translation skill on this machine)
S=$(ls -d "$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"/*/*/skills/side-by-side-translation/scripts/facing 2>/dev/null | head -1)
[ -d "$S" ] || S="$HOME/.claude/skills/side-by-side-translation/scripts/facing"
[ -d "$S" ] || S=$(ls -d "$HOME/.claude/plugins"/*/*/skills/side-by-side-translation/scripts/facing 2>/dev/null | head -1)
[ -d "$S" ] || { echo "skill scripts not found"; exit 1; }
F="$HOME/Desktop/claude-folder/_facing-pipeline"; P="$HOME/Desktop/claude-folder"
H="$(cd "$(dirname "$0")" && pwd)"; [ -d "$H" ] || exit 1
C="$H/staging"; rm -rf "$C"; mkdir -p "$C/glossaries"
book() { [ -z "$ONLY" ] || [ "$ONLY" = "book" ] || return;  d=$1; slug=$2; shift 2; "$S/py" "$S/corpus.py" book "$F/$d" -o "$C" --slug "$slug" "$@" 2>&1 | grep -v "block structure" ; [ -f "$F/$d/work/GLOSSARY.md" ] && cp "$F/$d/work/GLOSSARY.md" "$C/glossaries/$slug.md"; }
pdf()  { [ -z "$ONLY" ] || [ "$ONLY" = "pdf" ] || return;  f=$1; slug=$2; shift 2; "$S/py" "$S/corpus.py" pdf "$P/$f" -o "$C" --slug "$slug" "$@"; }

# --- editions with page files (source of truth: the page files) ---
book bardili    bardili-grundriss-der-ersten-logik      --title "Grundriß der Ersten Logik" --title-en "Outline of First Logic" --author "C. G. Bardili" --year 1800 --lang de --genre "Logic"
book bolzano    bolzano-wissenschaftslehre-uebersicht   --title "Wissenschaftslehre und Religionswissenschaft in einer beurtheilenden Uebersicht" --title-en "Theory of Science and Science of Religion, a Critical Overview" --author "Bernard Bolzano" --year 1841 --lang de --genre "Logic"
book boutroux   boutroux-psychologie-du-mysticisme      --title "La Psychologie du mysticisme" --title-en "The Psychology of Mysticism" --author "Émile Boutroux" --year 1902 --lang fr --genre "Psychology and religion"
book brentano   brentano-psychologie-des-aristoteles    --title "Die Psychologie des Aristoteles" --title-en "The Psychology of Aristotle" --author "Franz Brentano" --year 1867 --lang de --genre "Psychology and religion"
book dilthey    dilthey-jugendgeschichte-hegels         --title "Die Jugendgeschichte Hegels" --title-en "The History of Hegel's Youth" --author "Wilhelm Dilthey" --year 1905 --lang de --genre "Hegel and his school"
book escritos   varona-escritos                         --title "Escritos" --title-en "Writings" --author "Enrique José Varona" --year 1917 --lang es --genre "Latin American philosophy"
book exner      exner-psychologie-hegelsche-schule      --title "Die Psychologie der Hegelschen Schule" --title-en "The Psychology of the Hegelian School" --author "Franz Exner" --year "1842–1844" --lang de --genre "Hegel and his school"
book fries      fries-neue-kritik-der-vernunft          --title "Neue Kritik der Vernunft I–II" --title-en "New Critique of Reason" --author "Jakob Friedrich Fries" --year 1807 --lang de --genre "Kant and post-Kantian philosophy"
book goeschel   goeschel-aphorismen-nichtwissen         --title "Aphorismen über Nichtwissen und absolutes Wissen" --title-en "Aphorisms on Not-Knowing and Absolute Knowing" --author "Carl Friedrich Göschel" --year 1829 --lang de --genre "Hegel and his school"
book hegel-enz  hegel-enzyklopaedie-1817                --title "Encyklopädie der philosophischen Wissenschaften im Grundrisse" --title-en "Encyclopaedia of the Philosophical Sciences in Outline" --author "G. W. F. Hegel" --year 1817 --lang de --genre "Hegel and his school"
book rosenkranz rosenkranz-hegels-leben                 --title "G. W. F. Hegel's Leben" --title-en "The Life of G. W. F. Hegel" --author "Karl Rosenkranz" --year 1844 --lang de --genre "Hegel and his school"
book seis       henriquez-urena-seis-ensayos            --title "Seis ensayos en busca de nuestra expresión" --title-en "Six Essays in Search of Our Expression" --author "Pedro Henríquez Ureña" --year 1928 --lang es --genre "Latin American philosophy"
book varona     varona-seis-conferencias                --title "Seis conferencias" --title-en "Six Lectures" --author "Enrique José Varona" --year 1887 --lang es --genre "Latin American philosophy"
book wolff      wolff-vernuenfftige-gedancken-1720      --title "Vernünfftige Gedancken von Gott, der Welt und der Seele des Menschen" --title-en "Reasonable Thoughts on God, the World and the Soul of Man" --author "Christian Wolff" --year 1720 --lang de --genre "Wolff and the German Enlightenment"

# --- editions that survive only as PDFs (source of truth: the corpus file) ---
pdf "Bachofen - Versuch über die Gräbersymbolik der Alten (DE-EN facing).pdf" bachofen-graebersymbolik --title "Versuch über die Gräbersymbolik der Alten" --title-en "Essay on the Tomb Symbolism of the Ancients" --author "J. J. Bachofen" --year "1859 (2nd ed. 1925)" --lang de --genre "Myth and symbolism"
pdf "Bello - Filosofía del entendimiento - Philosophy of the Understanding (ES-EN facing).pdf" bello-filosofia-del-entendimiento --title "Filosofía del entendimiento" --title-en "Philosophy of the Understanding" --author "Andrés Bello" --year 1881 --lang es --genre "Latin American philosophy"
pdf "Clavigero - Storia antica del Messico TOMO I (IT-EN facing).pdf"   clavigero-storia-antica-del-messico-1 --title "Storia antica del Messico, tomo I" --title-en "Ancient History of Mexico, vol. I" --author "Francesco Saverio Clavigero" --year 1780 --lang it --genre "History of the Americas"
pdf "Clavigero - Storia antica del Messico TOMO II (IT-EN facing).pdf"  clavigero-storia-antica-del-messico-2 --title "Storia antica del Messico, tomo II" --title-en "Ancient History of Mexico, vol. II" --author "Francesco Saverio Clavigero" --year 1780 --lang it --genre "History of the Americas"
pdf "Clavigero - Storia antica del Messico TOMO III (IT-EN facing).pdf" clavigero-storia-antica-del-messico-3 --title "Storia antica del Messico, tomo III" --title-en "Ancient History of Mexico, vol. III" --author "Francesco Saverio Clavigero" --year 1780 --lang it --genre "History of the Americas"
pdf "Clavigero - Storia antica del Messico IV - Dissertations (IT-EN facing).pdf" clavigero-storia-antica-del-messico-4 --title "Storia antica del Messico, tomo IV: Dissertazioni" --title-en "Ancient History of Mexico, vol. IV: Dissertations" --author "Francesco Saverio Clavigero" --year 1781 --lang it --genre "History of the Americas"
pdf "Gamarra - Elementa recentioris philosophiae (Latin-English facing edition).pdf" gamarra-elementa-recentioris-philosophiae --title "Elementa recentioris philosophiae, vol. I" --title-en "Elements of Modern Philosophy" --author "Juan Benito Díaz de Gamarra" --year 1774 --lang la --genre "Latin American philosophy"
pdf "Gamarra - Juventuti Americanae (Latin-English facing edition).pdf" gamarra-juventuti-americanae --title "Juventuti Americanae (preface to the Elementa)" --title-en "To the Youth of America" --author "Juan Benito Díaz de Gamarra" --year 1774 --lang la --genre "Latin American philosophy"
pdf "Hostos_Tratado_de_Sociologia_parallel_EN.pdf" hostos-tratado-de-sociologia --title "Tratado de sociología" --title-en "Treatise on Sociology" --author "Eugenio María de Hostos" --year 1904 --lang es --genre "Latin American philosophy"
pdf "Logica_mexicana_facing.pdf" rubio-logica-mexicana --title "Logica mexicana" --title-en "Mexican Logic" --author "Antonio Rubio" --year 1615 --lang la --genre "Logic"
pdf "Luz y Caballero - Obras I - Works I (ES-EN facing).pdf" luz-y-caballero-obras-1 --title "Obras, tomo I" --title-en "Works, vol. I" --author "José de la Luz y Caballero" --lang es --genre "Latin American philosophy"
pdf "Palagyi_Logik_auf_dem_Scheidewege_facing.pdf" palagyi-logik-auf-dem-scheidewege --title "Die Logik auf dem Scheidewege" --title-en "Logic at the Crossroads" --author "Melchior Palágyi" --year 1903 --lang de --genre "Logic"
pdf "Palagyi_Ismerettan_alapvetese_facing.pdf" palagyi-ismerettan-alapvetese --title "Az ismerettan alapvetése" --title-en "Foundations of the Theory of Knowledge" --author "Menyhért Palágyi" --year 1904 --lang hu --genre "Logic"
pdf "Tiberghien_Logique_I_facing.pdf" tiberghien-logique-1 --title "Logique, tome I" --title-en "Logic, vol. I" --author "Guillaume Tiberghien" --year 1865 --lang fr --genre "Logic"
pdf "Vaz Ferreira - Lógica viva - Living Logic (ES-EN facing).pdf" vaz-ferreira-logica-viva --title "Lógica viva" --title-en "Living Logic" --author "Carlos Vaz Ferreira" --year 1910 --lang es --genre "Latin American philosophy"
pdf "Klages - Die psychologischen Errungenschaften Nietzsches (DE-EN).pdf" klages-errungenschaften-nietzsches --title "Die psychologischen Errungenschaften Nietzsches" --title-en "The Psychological Achievements of Nietzsche" --author "Ludwig Klages" --year 1926 --lang de --genre "Lebensphilosophie"

"$S/py" "$S/corpus.py" index "$C"
# Klages, Der Geist als Widersacher der Seele (corpus/klages-geist-als-widersacher-der-seele.md) is NOT regenerated here:
# it was recovered once (Oct 2026) from the 1960-page parallel PDF, with the endnotes set under their cue paragraphs,
# and the corpus file itself is the source. Correct it in place.

# --- originals without a translation, and translations kept as chunk files (sources in originals/) ---
O="$(cd "$(dirname "$0")" && pwd)/originals"
text() { f=$1; slug=$2; shift 2; [ -z "$ONLY" ] || [ "$ONLY" = "text" ] || return; "$S/py" "$S/corpus.py" text "$f" -o "$C" --slug "$slug" "$@"; }
text "$O/trendelenburg-lu-1.de.md" trendelenburg-lu-1-original --title "Logische Untersuchungen, Bd. I (3. Aufl.)" --title-en "Logical Investigations, vol. I — German text" --author "F. A. Trendelenburg" --year 1870 --lang de --genre "Logic"
text "$O/trendelenburg-lu-2.de.md" trendelenburg-lu-2-original --title "Logische Untersuchungen, Bd. II (3. Aufl.)" --title-en "Logical Investigations, vol. II — German text" --author "F. A. Trendelenburg" --year 1870 --lang de --genre "Logic"
[ -z "$ONLY" ] || [ "$ONLY" = "text" ] && "$S/py" "$S/corpus.py" chunks "$O/trendelenburg-chunks" -o "$C" --slug trendelenburg-logische-untersuchungen --title "Logische Untersuchungen (translated chapters)" --title-en "Logical Investigations" --author "F. A. Trendelenburg" --year 1870 --lang de --genre "Logic"
text "$O/klages-persoenlichkeit.md" klages-persoenlichkeit --title "Persönlichkeit. Einführung in die Charakterkunde" --title-en "Personality. Introduction to Characterology — German text" --author "Ludwig Klages" --year 1928 --lang de --genre "Lebensphilosophie"
text "$HOME/Downloads/obereits-wiederruf.pdf" obereit-widerruf-fuer-kant --title "Obereits Widerruf für Kant" --title-en "Obereit's Recantation for Kant — German text" --author "Jakob Hermann Obereit" --year 1791 --lang de --genre "Kant and post-Kantian philosophy"
text "$HOME/Downloads/Edgar_Dacqué_Urwelt_Sage_und_Menschheit.pdf" dacque-urwelt-sage-und-menschheit --title "Urwelt, Sage und Menschheit" --title-en "Primeval World, Saga and Humanity — German text" --author "Edgar Dacqué" --year 1924 --lang de --genre "Myth and symbolism"
"$S/py" "$S/corpus.py" index "$C"

# --- Vasconcelos, Obras: the Tufte HTML readers in originals/vasconcelos-obras-v2 -> corpus/vasconcelos/ ---
[ "$ONLY" = "" ] || [ "$ONLY" = "html" ] && "$S/py" "$S/corpus.py" html "$O/vasconcelos-obras-v2" -o "$C/vasconcelos" --author "José Vasconcelos" --collection "Obras (vasconcelos-obras-v2)" --prefix vasconcelos --genre "Latin American philosophy" && "$S/py" "$S/corpus.py" index "$C"

# --- corpus/<slug>/ is the source now: staged files only add editions that have no folder there yet ---
NEW=$(python3 "$H/tools/split.py" --into "$H/corpus" "$C"/*.md "$C"/vasconcelos/*.md | tee /dev/stderr | sed -n 's/^\([^: ]*\): round trip.*/\1/p')
# --- a new edition enters in the paragraph standard: rejoin.py joins the paragraphs the page-by-page translation cut at page turns ---
for r in $NEW; do python3 "$H/tools/rejoin.py" --write "$H/corpus/$r"; done
