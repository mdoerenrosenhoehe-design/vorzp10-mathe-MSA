# ZP10 Mathematik NRW – MSA Training 2027

Eine vollständig statische, responsive Lernplattform zur Vorbereitung auf die Zentrale Prüfung 10 Mathematik in NRW auf MSA-Niveau.

## Enthalten

- 10 Themenbereiche
- 1.080 Trainingsaufgaben (108 je Thema)
- 80 MSA-Challenges
- 120 Karteikarten
- Quiz mit 20 Fragen und ansteigender Schwierigkeit
- Zuordnungsspiel mit 10 Paaren
- Prüfungstraining mit 3-Versuche-Hilfesystem
- adaptive Aufgabenauswahl anhand der lokalen Fehlerstatistik
- 20 vollständige Prüfungssimulationen mit Teil 1 und Teil 2
- Timer, automatische Abgabe und Auswertung
- Lernempfehlungen und Fortschrittsdashboard
- dauerhafte Speicherung im Browser ohne Login
- Paddy-KI-Lernhilfe in einem neuen Tab
- PWA/Offline-Cache nach dem ersten Laden
- QR-Code-Generator für die veröffentlichte Adresse
- eigene Formelübersicht für das Training

## Schnellstart lokal

Da alle Daten als JavaScript-Dateien eingebunden sind, lässt sich `index.html` direkt öffnen. Für die PWA-/Service-Worker-Funktion ist ein lokaler Webserver besser:

```bash
python -m http.server 8000
```

Danach im Browser `http://localhost:8000` öffnen.

## Veröffentlichung mit GitHub Pages

1. Auf GitHub ein neues Repository anlegen, z. B. `zp10-msa-mathe`.
2. Den **gesamten Inhalt dieses Projektordners** in das Repository hochladen. `index.html` muss direkt im Hauptverzeichnis liegen.
3. Im Repository `Settings` → `Pages` öffnen.
4. Unter `Build and deployment` als Quelle `Deploy from a branch` auswählen.
5. Branch `main` und Ordner `/ (root)` auswählen und speichern.
6. Nach kurzer Wartezeit zeigt GitHub Pages die öffentliche Adresse an.
7. Diese Adresse auf der Website im Bereich **QR-Code** eintragen und den QR-Code erzeugen.

Wichtig: Bei einem Projekt-Repository lautet die Adresse in der Regel `https://BENUTZERNAME.github.io/REPOSITORY/`. Die Dateien verwenden ausschließlich relative Pfade und funktionieren daher auch in einem Unterverzeichnis.

## Prüfungssimulation

Die bereitgestellten offiziellen Vorgaben 2027 legen die Zweiteilung und die Hilfsmittel fest. Die aktuelle offizielle Verfahrensregelung sieht für MSA Mathematik 120 Minuten reguläre Bearbeitungszeit vor: 30 Minuten Teil 1, 90 Minuten Teil 2. Nicht genutzte Zeit aus Teil 1 kann in Teil 2 weiterverwendet werden. Zusätzlich stehen 10 Minuten Bonuszeit zur Verfügung, die in Mathematik flexibel auf beide Teile verteilt werden können. Die Simulation arbeitet deshalb mit maximal 130 Minuten und beendet Teil 1 spätestens nach 40 Minuten.

Da die genaue Durchführung jährlich per Verfügung geregelt wird, sollte vor dem realen Einsatz im Prüfungsjahr 2027 noch einmal die dann veröffentlichte Rundverfügung geprüft werden. Die Zeiten befinden sich zentral in `data/meta.js` und können dort bei Bedarf angepasst werden.

## Datenschutz / Speicherung

Es gibt keine Anmeldung und keinen Server für Lernstände. Die Daten werden nur im Browser unter dem Schlüssel `zp10-msa-progress-v1` in `localStorage` gespeichert. Wer Browserdaten löscht oder ein anderes Gerät verwendet, beginnt dort mit einem neuen Lernstand.

## Aufgaben-Datenbank

Die Daten liegen getrennt vom Programmcode:

- `data/topics.js` – Themen
- `data/tasks.js` – reguläre Aufgaben
- `data/challenges.js` – MSA-Challenges
- `data/flashcards.js` – Karteikarten
- `data/exams.js` – 20 Prüfungssimulationen
- `data/meta.js` – Prüfungsparameter und Metadaten

Der Generator `tools/build_data.py` erzeugt die Daten reproduzierbar. `tools/validate.py` prüft IDs, Umfang, Antwortdaten und Prüfungsstruktur.

## Qualitäts- und Copyright-Hinweis

Frühere Original-ZP10-Aufgaben wurden **nicht** in die veröffentlichbare Website kopiert. Die Standardsicherung NRW erlaubt deren Bereitstellung ausschließlich im dafür vorgesehenen Lehr-/Lernrahmen und untersagt eine weitergehende Veröffentlichung auf einer öffentlichen Website. Die hier enthaltenen Aufgaben sind deshalb eigenständige Neuentwicklungen, die sich nur an Struktur, Kompetenzen und Anspruch der analysierten MSA-Prüfungen orientieren.

Die automatische Prüfungsauswertung eignet sich für das Training. Offene Begründungen werden über Schlüsselbegriffe ausgewertet; die 3 Punkte für Maßeinheiten und 6 Punkte für Darstellungsleistung sind in der Simulation lediglich eine automatische Trainingsschätzung und ersetzen keine Lehrkraftkorrektur.

## Wartung

Wenn du neue Aufgaben hinzufügst, achte mindestens auf: eindeutige ID, Thema, Unterthema, Kompetenz, Schwierigkeit, Typ, Aufgabenstellung, Antwort, Hinweise, Lösungsweg und Punkte. Führe danach aus:

```bash
python tools/validate.py
```
