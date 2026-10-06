# Material- und Prüfungsanalyse – ZP10 Mathematik NRW, MSA 2027

## Grundlage

Für das Projekt wurden die im bereitgestellten Sammel-PDF enthaltenen offiziellen Vorgaben 2027, die MSA-Formelsammlung, Beispielaufgaben für den hilfsmittelfreien Prüfungsteil, die Prüfungen bzw. Auswertungsunterlagen 2024–2026 sowie die bereitgestellten Vorbereitungsseiten ausgewertet. Die 2027-Vorgaben stehen im Sammel-PDF auf den Seiten 174–175.

## Prüfungsstruktur 2027

Die offiziellen 2027-Vorgaben beschreiben zwei Prüfungsteile. Teil 1 prüft Basiskompetenzen in voneinander unabhängigen Teilaufgaben und wird ohne Taschenrechner und Formelsammlung bearbeitet. Zugelassen sind nur Zirkel und Geodreieck. Teil 2 enthält komplexere, kontextgebundene Aufgaben mit mehreren Teilaufgaben und verknüpft Inhalts- und Prozesskompetenzen. Hier sind Zirkel, Geodreieck, MSA-Formelsammlung und Taschenrechner zugelassen.

Die aktuell veröffentlichte Verfahrensregelung/FAQ führt für Mathematik MSA 120 Minuten reguläre Bearbeitungszeit an: 30 Minuten als vorgesehene Zeit für Teil 1 und 90 Minuten für Teil 2. Nicht genutzte Zeit aus Teil 1 kann in Mathematik für Teil 2 verwendet werden. Zusätzlich steht eine Bonuszeit von 10 Minuten zur Orientierung zur Verfügung, die in Mathematik flexibel auf beide Teile verteilt werden kann. Deshalb verwendet die Simulation eine maximale Gesamtzeit von 130 Minuten und begrenzt Teil 1 auf höchstens 40 Minuten. Vor Einsatz im Prüfungsjahr 2027 sollte die jährlich aktualisierte Durchführungsvorschrift noch einmal gegengeprüft werden.

## Typische Struktur der vergangenen MSA-Prüfungen

Die Auswertungen 2024–2026 zeigen ein stabiles Raster: Teil 1 umfasst 18 Punkte. Teil 2 umfasst insgesamt 54 mathematische Punkte in drei umfangreichen Kontextaufgaben. Zusätzlich werden 3 Punkte für den Umgang mit Maßeinheiten und 6 Punkte für die Darstellungsleistung vergeben; damit ergeben sich 81 Punkte. Die konkrete Aufteilung der 54 Punkte auf die drei Kontextaufgaben kann variieren (z. B. 2025: 16/19/19 statt 18/18/18).

Teil 1 verwendet kurze, voneinander unabhängige Aufgaben mit Darstellungswechseln und teilweise argumentativen Anteilen. In den jüngsten Prüfungen kamen u. a. Größenumrechnung, Tabellenkalkulation, Prozentrechnung, Flächen/Umfang, Gleichungen und LGS, lineare bzw. exponentielle Funktionen, Potenzen/Wurzeln, Schätzen, elementare Wahrscheinlichkeit und Statistik vor.

Teil 2 arbeitet deutlich kontextgebundener. Beispiele aus den ausgewerteten Prüfungen sind exponentielles Wachstum und Funktionsvergleich, Körpergeometrie und Modellierung, Wahrscheinlichkeiten, Dateninterpretation sowie das Beurteilen und Begründen von Modellannahmen. Typisch ist, dass Teilaufgaben aufeinander aufbauen oder verschiedene Inhaltsbereiche innerhalb eines Sachkontextes verbunden werden.

## MSA-Niveau gegenüber EESA

Für den MSA wurden Aufgaben gezielt so angelegt, dass nicht nur Routineverfahren abgefragt werden. Kennzeichnend sind:

- mehrschrittige Lösungswege und stärkerer Transfer,
- komplexere Sachzusammenhänge, in denen relevante Informationen zuerst ausgewählt werden müssen,
- Begründungen, Überprüfungen und Beurteilungen statt reiner Ergebnisproduktion,
- Interpretation von Graphen, Tabellen und Ergebnissen im Kontext,
- mathematisches Modellieren und das Hinterfragen von Modellgrenzen,
- Verknüpfungen mehrerer Bereiche, z. B. Geometrie + Prozentrechnung oder Funktionen + Statistik,
- im MSA zusätzlich relevante Inhalte wie quadratische Funktionen/Gleichungen, Trigonometrie, umfangreichere Körpergeometrie und exponentielle Modelle.

## Themen- und Kompetenzkatalog der Website

Die Trainingsplattform bündelt die analysierten Anforderungen in zehn Lernbereiche:

1. Zahlen, Potenzen & Wurzeln
2. Terme, Gleichungen & lineare Gleichungssysteme
3. Prozent- & Zinsrechnung
4. Lineare Funktionen & Zuordnungen
5. Quadratische Funktionen
6. Exponentielles Wachstum
7. Ebene Geometrie & Trigonometrie
8. Körper & räumliche Geometrie
9. Daten & Statistik
10. Wahrscheinlichkeit

Prozessbezogen werden insbesondere Operieren, Darstellen, Modellieren, Problemlösen, Argumentieren und Interpretieren berücksichtigt. Im Prüfungstraining und in den MSA-Challenges liegt der Schwerpunkt bewusst auf Modellierung, Transfer und Begründung.

## Aufgabenentwicklung

Die alten Prüfungen wurden nur als Strukturanalyse verwendet. Es wurden keine alten Zentralprüfungsaufgaben oder geschützten Abbildungen in die Website übernommen. Jeder Themenbereich besitzt 108 neu generierte Trainingsaufgaben aus mindestens zwölf unterschiedlichen Aufgabenfamilien sowie acht zusätzliche Challenges. Parametrisierte Varianten werden durch unterschiedliche Aufgabentypen und Kontexte ergänzt; der Pool besteht damit nicht nur aus einer einzigen Aufgabe mit veränderten Zahlen.

Für die Prüfungssimulation wurden 20 vollständige Varianten erstellt. Jeder Teil 1 umfasst sechs kurze Aufgaben zu 3 Punkten. Jeder Teil 2 umfasst drei neue Kontextaufgaben mit jeweils sechs Teilaufgaben zu insgesamt 54 Punkten. Die automatische Bewertung der 9 übergreifenden Punkte ist ausdrücklich nur eine Trainingsschätzung, weil eine Website die Qualität einer handschriftlichen Darstellung nicht vollständig beurteilen kann.

## Technische Umsetzung

Die Plattform ist statisch und für GitHub Pages geeignet. Lernstand, Quizwerte, Kartenstatus, Aufgabenergebnisse und Prüfungshistorie werden ohne Anmeldung im Browser (`localStorage`) gespeichert. Die Seite funktioniert responsiv und touchfreundlich. Ein Service Worker ermöglicht nach dem ersten Laden die Nutzung der Kernbestandteile als PWA auch bei instabiler Verbindung.
