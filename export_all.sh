#!/bin/sh
# Regenerates corpus/ from the page files (and, for editions whose page files were not kept, from their PDFs).
# Run after any edition changes:  sh export_all.sh        (needs the side-by-side-translation skill on this machine)
S=$(ls -d "$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"/*/*/skills/side-by-side-translation/scripts/facing 2>/dev/null | head -1)
[ -d "$S" ] || S="$HOME/.claude/skills/side-by-side-translation/scripts/facing"
[ -d "$S" ] || S=$(ls -d "$HOME/.claude/plugins"/*/*/skills/side-by-side-translation/scripts/facing 2>/dev/null | head -1)
[ -d "$S" ] || { echo "skill scripts not found"; exit 1; }
F="$HOME/Desktop/claude-folder/_facing-pipeline"; P="$HOME/Desktop/claude-folder"
C="$(cd "$(dirname "$0")" && pwd)/corpus"; mkdir -p "$C/glossaries"
book() { [ "$ONLY" = "pdf" ] && return;  d=$1; slug=$2; shift 2; "$S/py" "$S/corpus.py" book "$F/$d" -o "$C" --slug "$slug" "$@" 2>&1 | grep -v "block structure" ; [ -f "$F/$d/work/GLOSSARY.md" ] && cp "$F/$d/work/GLOSSARY.md" "$C/glossaries/$slug.md"; }
pdf()  { [ "$ONLY" = "book" ] && return;  f=$1; slug=$2; shift 2; "$S/py" "$S/corpus.py" pdf "$P/$f" -o "$C" --slug "$slug" "$@"; }

# --- editions with page files (source of truth: the page files) ---
book bardili    bardili-grundriss-der-ersten-logik      --title "Grundriß der Ersten Logik" --title-en "Outline of First Logic" --author "C. G. Bardili" --year 1800 --lang de
book bolzano    bolzano-wissenschaftslehre-uebersicht   --title "Wissenschaftslehre und Religionswissenschaft in einer beurtheilenden Uebersicht" --title-en "Theory of Science and Science of Religion, a Critical Overview" --author "Bernard Bolzano" --year 1841 --lang de
book boutroux   boutroux-psychologie-du-mysticisme      --title "La Psychologie du mysticisme" --title-en "The Psychology of Mysticism" --author "Émile Boutroux" --year 1902 --lang fr
book brentano   brentano-psychologie-des-aristoteles    --title "Die Psychologie des Aristoteles" --title-en "The Psychology of Aristotle" --author "Franz Brentano" --year 1867 --lang de
book dilthey    dilthey-jugendgeschichte-hegels         --title "Die Jugendgeschichte Hegels" --title-en "The History of Hegel's Youth" --author "Wilhelm Dilthey" --year 1905 --lang de
book escritos   varona-escritos                         --title "Escritos" --title-en "Writings" --author "Enrique José Varona" --year 1917 --lang es
book exner      exner-psychologie-hegelsche-schule      --title "Die Psychologie der Hegelschen Schule" --title-en "The Psychology of the Hegelian School" --author "Franz Exner" --year "1842–1844" --lang de
book fries      fries-neue-kritik-der-vernunft          --title "Neue Kritik der Vernunft I–II" --title-en "New Critique of Reason" --author "Jakob Friedrich Fries" --year 1807 --lang de
book goeschel   goeschel-aphorismen-nichtwissen         --title "Aphorismen über Nichtwissen und absolutes Wissen" --title-en "Aphorisms on Not-Knowing and Absolute Knowing" --author "Carl Friedrich Göschel" --year 1829 --lang de
book hegel-enz  hegel-enzyklopaedie-1817                --title "Encyklopädie der philosophischen Wissenschaften im Grundrisse" --title-en "Encyclopaedia of the Philosophical Sciences in Outline" --author "G. W. F. Hegel" --year 1817 --lang de
book rosenkranz rosenkranz-hegels-leben                 --title "G. W. F. Hegel's Leben" --title-en "The Life of G. W. F. Hegel" --author "Karl Rosenkranz" --year 1844 --lang de
book seis       henriquez-urena-seis-ensayos            --title "Seis ensayos en busca de nuestra expresión" --title-en "Six Essays in Search of Our Expression" --author "Pedro Henríquez Ureña" --year 1928 --lang es
book varona     varona-seis-conferencias                --title "Seis conferencias" --title-en "Six Lectures" --author "Enrique José Varona" --year 1887 --lang es
book wolff      wolff-vernuenfftige-gedancken-1720      --title "Vernünfftige Gedancken von Gott, der Welt und der Seele des Menschen" --title-en "Reasonable Thoughts on God, the World and the Soul of Man" --author "Christian Wolff" --year 1720 --lang de

# --- editions that survive only as PDFs (source of truth: the corpus file) ---
pdf "Bachofen - Versuch über die Gräbersymbolik der Alten (DE-EN facing).pdf" bachofen-graebersymbolik --title "Versuch über die Gräbersymbolik der Alten" --title-en "Essay on the Tomb Symbolism of the Ancients" --author "J. J. Bachofen" --year "1859 (2nd ed. 1925)" --lang de
pdf "Bello - Filosofía del entendimiento - Philosophy of the Understanding (ES-EN facing).pdf" bello-filosofia-del-entendimiento --title "Filosofía del entendimiento" --title-en "Philosophy of the Understanding" --author "Andrés Bello" --year 1881 --lang es
pdf "Clavigero - Storia antica del Messico TOMO I (IT-EN facing).pdf"   clavigero-storia-antica-del-messico-1 --title "Storia antica del Messico, tomo I" --title-en "Ancient History of Mexico, vol. I" --author "Francesco Saverio Clavigero" --year 1780 --lang it
pdf "Clavigero - Storia antica del Messico TOMO II (IT-EN facing).pdf"  clavigero-storia-antica-del-messico-2 --title "Storia antica del Messico, tomo II" --title-en "Ancient History of Mexico, vol. II" --author "Francesco Saverio Clavigero" --year 1780 --lang it
pdf "Clavigero - Storia antica del Messico TOMO III (IT-EN facing).pdf" clavigero-storia-antica-del-messico-3 --title "Storia antica del Messico, tomo III" --title-en "Ancient History of Mexico, vol. III" --author "Francesco Saverio Clavigero" --year 1780 --lang it
pdf "Clavigero - Storia antica del Messico IV - Dissertations (IT-EN facing).pdf" clavigero-storia-antica-del-messico-4 --title "Storia antica del Messico, tomo IV: Dissertazioni" --title-en "Ancient History of Mexico, vol. IV: Dissertations" --author "Francesco Saverio Clavigero" --year 1781 --lang it
pdf "Gamarra - Elementa recentioris philosophiae (Latin-English facing edition).pdf" gamarra-elementa-recentioris-philosophiae --title "Elementa recentioris philosophiae, vol. I" --title-en "Elements of Modern Philosophy" --author "Juan Benito Díaz de Gamarra" --year 1774 --lang la
pdf "Gamarra - Juventuti Americanae (Latin-English facing edition).pdf" gamarra-juventuti-americanae --title "Juventuti Americanae (preface to the Elementa)" --title-en "To the Youth of America" --author "Juan Benito Díaz de Gamarra" --year 1774 --lang la
pdf "Hostos_Tratado_de_Sociologia_parallel_EN.pdf" hostos-tratado-de-sociologia --title "Tratado de sociología" --title-en "Treatise on Sociology" --author "Eugenio María de Hostos" --year 1904 --lang es
pdf "Logica_mexicana_facing.pdf" rubio-logica-mexicana --title "Logica mexicana" --title-en "Mexican Logic" --author "Antonio Rubio" --year 1615 --lang la
pdf "Luz y Caballero - Obras I - Works I (ES-EN facing).pdf" luz-y-caballero-obras-1 --title "Obras, tomo I" --title-en "Works, vol. I" --author "José de la Luz y Caballero" --lang es
pdf "Palagyi_Logik_auf_dem_Scheidewege_facing.pdf" palagyi-logik-auf-dem-scheidewege --title "Die Logik auf dem Scheidewege" --title-en "Logic at the Crossroads" --author "Melchior Palágyi" --year 1903 --lang de
pdf "Palagyi_Ismerettan_alapvetese_facing.pdf" palagyi-ismerettan-alapvetese --title "Az ismerettan alapvetése" --title-en "Foundations of the Theory of Knowledge" --author "Menyhért Palágyi" --year 1904 --lang hu
pdf "Tiberghien_Logique_I_facing.pdf" tiberghien-logique-1 --title "Logique, tome I" --title-en "Logic, vol. I" --author "Guillaume Tiberghien" --year 1865 --lang fr
pdf "Vaz Ferreira - Lógica viva - Living Logic (ES-EN facing).pdf" vaz-ferreira-logica-viva --title "Lógica viva" --title-en "Living Logic" --author "Carlos Vaz Ferreira" --year 1910 --lang es
pdf "Klages - Die psychologischen Errungenschaften Nietzsches (DE-EN).pdf" klages-errungenschaften-nietzsches --title "Die psychologischen Errungenschaften Nietzsches" --title-en "The Psychological Achievements of Nietzsche" --author "Ludwig Klages" --year 1926 --lang de

"$S/py" "$S/corpus.py" index "$C"
