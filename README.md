[![de](https://img.shields.io/badge/language-german-green.svg)](https://gitlab.gwdg.de/fsrphys/tagesordnung-updater/blob/main/README.md)
[![en](https://img.shields.io/badge/language-english-blue.svg)](https://gitlab.gwdg.de/fsrphys/tagesordnung-updater/blob/main/README.en.md)


# Tagesordnung Updater
Der Tagesordnung Updater veröffentlicht die Tagesordnung des FSR Physiks auf seiner Website. Die Tagesordnung wird außerdem auf Englisch übersetzt und auf der englischen Website veröffentlicht.


## Vorbereitung
Nachdem das Projekt heruntergeladen wurde, müssen von allen Beispiel-Dateien mit Namen `dateiname.example.endung` Kopien mit Namen `dateiname.endung` erstellt und ausgefüllt werden.

Um das Skript auszuführen, benötigt man [Docker](https://docs.docker.com/get-docker/). Solange alles funktioniert sollten aber keine Docker-Kenntnisse nötig sein, sondern nur die untenstehenden Befehle.


## Verwendung
Um den Tagesordnung Updater zu starten, führt man im Projekt-Ordner folgenden Befehl aus:
```bash
sudo docker compose up -d
```
Das Skript wird daraufhin gestartet und läuft im Hintergrund. Der Docker Container startet sich bei Problemen von alleine neu, es sei denn, er wurde manuell beendet.

Man beendet den Tagesordnung Updater mit dem Befehl
```bash
sudo docker compose down
```

Wenn etwas am Programm geändert wurde, muss der Container neu gebaut werden. Dafür beendet man den Tagesordnung Updater zuerst und startet ihn dann wie gewohnt, benutzt aber folgenden Befehl:
```bash
sudo docker compose up --build -d
```


## Konfiguration
### Website-Vorlage
Die Website wird aus der Website-Vorlage generiert, die automatisch mit den Informationen gefüllt wird. Die Vorlage kann in der Datei `page.html` für die deutsche Seite und `page.en.html` für die englische Seite angepasst werden. Dabei können einige Variable genutzt werden, indem diese in geschweiften Klammern geschrieben werden. Unterstützt werden:
- `Datum`: Das Datum der Sitzung
- `TO`: Die Tagesordnung der Sitzung als numerierte Liste
