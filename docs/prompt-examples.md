Claude Motion Graphics, alle Prompts aus dem Video
Reihenfolge wie im Video. Alle Tests liefen in Claude Code mit Claude Opus 5.5, jeweils in einem leeren Ordner.


========================================================================
SHOWREEL, der Prompt aus dem Einstieg
========================================================================

Ein einziger Satz, ohne HyperFrames und ohne weitere Vorgaben. Claude baut sich dabei auch das Programm selbst, das die Animation Bild für Bild aufnimmt.

PROMPT:
Make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. Go all out.


========================================================================
TEST 1, aus der Rohaufnahme wird ein fertiger Short
========================================================================

Vorbereitung: Leg deine Rohaufnahme (Talking Head, gern mit Versprechern und doppelten Takes) in einen leeren Ordner.

PROMPT:
In diesem Ordner liegt meine Rohaufnahme für einen YouTube-Short. Mach daraus einen fertigen Short, den ich direkt posten kann, und arbeite durch, bis das Video da ist. Die Grafiken baust du mit HyperFrames, Sounds und Musik erzeugst du selbst.

Ich spreche Sätze oft mehrmals ein, weil ich mich verspreche. Nimm jeweils den letzten sauberen Take, damit nichts doppelt vorkommt und der Short flüssig wirkt.

Zum Look: Auf Shorts entscheidet sich in der ersten Sekunde, ob jemand bleibt, und die Leute bleiben, wenn sie mein Gesicht sehen und gleichzeitig verstehen, worum es geht. Deshalb wechseln drei Layouts: mein Kamerabild im Vollbild, ein Split mit Grafik oben und meiner Kamera als Karte unten, bei der mein freigestellter Kopf über die obere Kartenkante ragt, und Grafik im Vollbild. Der Hook ist ein Split, das Ende gehört der Kamera.

Die Karte im Split sitzt fest unten: Sie reicht bis an den unteren Bildrand und ihre Oberkante liegt bei knapp zwei Dritteln der Bildhöhe. Mein Kopf ragt etwas darüber hinaus, freigestellt und pixelgenau mit dem Bild in der Karte, die Maske ist im Gesicht voll deckend. Mein Kamerabild hat in jedem Split dieselbe Größe und Position, damit ich immer an derselben Stelle stehe.

Zwischen den Layouts wird hart geschnitten, von einem Frame auf den nächsten. Die Kamera-Karte und mein Bild fliegen nie rein oder raus, blenden nicht und skalieren nicht. Das wirkt wie ein Kamerawechsel und hält den Blick auf dem Inhalt. Bewegung gibt es nur in der Grafik selbst.

Die Grafik ist eine helle, ruhige Welt aus weißen Karten mit einer Akzentfarbe, und sie zeigt immer das, worüber ich gerade rede. Zeig dabei das echte Ding statt eines Symbols: Rede ich z.B. über eine Datei, ist es ein Blatt mit lesbarem Inhalt, nicht ein Kreis mit einem Kürzel drin. Rede ich über ein Programm, ist es seine nachgebaute Oberfläche, in der gerade etwas passiert. Je greifbarer, desto besser versteht man es.

Recherchier zu dem, was ich erzähle, selbst im Internet und hol dir echtes Material: offizielle Logos, Screenshots aus der Dokumentation oder von der Webseite. Genau der Satz, auf den es gerade ankommt, bekommt einen Marker, damit man sieht, dass es wirklich so dasteht. Prüf dabei jede Aussage gegen die offizielle Quelle.

Meine Zuschauer sind nicht unbedingt Techniker. Kurzer Text in der Grafik ist gut, etwa ein Dateiname, eine Regel oder eine Statusmeldung, aber lange Absätze oder Code, den man erst lesen muss, verlieren sie.

Untertitel in einer fetten Grotesk mit normaler Rechtschreibung, Wörter erscheinen nacheinander, wenige Wörter auf einmal, wichtige Begriffe in der Akzentfarbe, immer waagerecht mittig. Wo sie stehen, hängt vom Layout ab, damit sie nie mein Gesicht oder die Grafik verdecken: im Split in der Lücke zwischen Grafik und meinem Kopf, bei der Kamera im Vollbild unterhalb meines Gesichts auf Brusthöhe, bei der Grafik im Vollbild unter der Grafik im unteren Drittel.

Beim Ton steht meine Stimme immer klar vorn. Sounds nur dort, wo auf dem Bild etwas passiert, dezent und nicht verspielt. Darunter ein warmes, harmonisch sauberes Instrumental, das nach dem Hook einsetzt und sehr leise bleibt: etwa 24 LU unter der Stimme (Stimme um -14 LUFS, Musik um -38 LUFS), mit einem gleichbleibenden Pegel.


========================================================================
TEST 2, Werbespot für ein Produkt, das man nicht anfassen kann
========================================================================

Vorbereitung: In den Ordner gehören eine Datei .env mit deinem ElevenLabs-Key (ELEVENLABS_API_KEY=...) und ein Musiktrack als royalty-free-music.mp3, zum Beispiel von Pixabay. Der Key gehört nur in die .env, nie in den Prompt. Der Spot ist eine Demo und kein offizieller Spot von Excalidraw.

PROMPT:
Mach einen dynamischen Motion-Graphics-Werbespot für Excalidraw+, etwa 30 Sekunden, mit HyperFrames. Zeig damit, was für ein unglaublich guter Motion Designer du bist, als wäre das der Spot, mit dem du dich bei Excalidraw bewirbst. Der Spot lebt in Excalidraws eigener Welt: ihre Zeichenfläche, ihre handgezeichneten Striche (rough.js), ihre Schrift, ihre Farben, ihre echte Oberfläche.

Mach das Gefühl greifbar: Eine Idee im Kopf sieht niemand, mit Excalidraw+ wird sie in Sekunden zu einer Skizze, an der dein Team sofort mitarbeitet. Erzähl das als Geschichte und zeig unterwegs, was Excalidraw+ kann.

Recherchier das Produkt auf plus.excalidraw.com, in der Doku und auf GitHub. Zeig und sag im Spot, was Excalidraw+ laut diesen Quellen kann. Viel Inspiration zum Stil und den Möglichkeiten findest du unter https://plus.excalidraw.com/use-cases. Das Logo holst du dir original von den offiziellen Seiten, die Oberfläche baust du nach echten Screenshots nach, und alle Illustrationen, Skizzen und Szenen zeichnest du selbst im gleichen Stil wie Excalidraw.

Eine deutsche Sprecherstimme kommt über die ElevenLabs-API (Lola, Voice-ID SiMvlSW9cKKHDYT4BzOp, auf Deutsch mit dem Modell eleven_v4), der Key liegt in der .env. Als Hintergrundmusik nimmst du royalty-free-music.mp3 aus dem Ordner. Die Musik läuft leise unter der Stimme (-36 LUFS), die Stimme bleibt immer klar vorn (-14 LUFS). Der fertige Mix landet bei -12 LUFS. Sounds erzeugst du selbst.


========================================================================
TEST 3, animiertes Erklärvideo für eine Schulung
========================================================================

Vorbereitung: In den Ordner gehört eine Datei .env mit deinem ElevenLabs-Key (ELEVENLABS_API_KEY=...). Thema, Quellen und Stimme kannst du für dein eigenes Erklärvideo einfach austauschen.

PROMPT:
Erstelle ein animiertes Erklärvideo für Mitarbeiterschulungen: „So erkennst du eine Phishing-Mail“, etwa 60 Sekunden, 1920x1080, mit HyperFrames. Zeig damit, was für ein unglaublich guter Animator du bist, als wäre das dein Probestück für eine Agentur, die Schulungsvideos für große Firmen macht.

Der Look ist verspielt und illustriert: eigene 2D-Figuren mit Mimik und Gestik, ein freundlicher Stil, wie man ihn aus guten Erklärvideos kennt. Alle Figuren, Illustrationen und Szenen zeichnest du selbst.

Recherchier die Warnzeichen beim BSI und bei der Verbraucherzentrale. Zeig und sag nur, was dort so empfohlen wird.

Die Sprecherstimme ist Alex von ElevenLabs (Voice-ID Dm2pqleCzqJpMQgIh5nm), auf Deutsch mit dem Modell eleven_v4. Der Key liegt in der .env. Den Sprechtext schreibst du selbst, freundlich und klar wie ein guter Trainer, nicht belehrend. Musik und Sounds erzeugst du selbst. Die Musik läuft leise unter der Stimme (-36 LUFS), die Stimme bleibt immer klar vorn (-14 LUFS). Der fertige Mix landet bei -12 LUFS.
