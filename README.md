# EWOBadges

## Compilierte Version:
* [EwoBadges.exe](https://github.com/KuntzeM/EWOBadges/blob/master/dist/EWOBadges.exe)
* Demos Dateien und Hintergrundbild: [dist](https://github.com/KuntzeM/EWOBadges/tree/master/dist)

Aktuelle Version: 1.1
(c) Mathias Kuntze,  mathias.kuntze@tu-ilmenau.de


#### Changelog

17.09.2016 v1.2
* Bilder für Vorder- und Rückseite können seperat ausgewählt werden
* auf Rückseite wird Titel nicht mehr angezeigt (Titel => z.B. Tutor)
* es müssen nicht mehr alle Personen Daten eingegeben werden
    * wird nur Studiengang oder Jahr angegeben, dann wird kein Simikolon mehr angezeigt
* durch Angabe keiner Personen Daten können nun "Blanko" Badges generiert werden

16.09.2016 v1.1
* Vorder- und Rückseite werden nebeneinander dargestellt
* Ausgabe erfolgt auf A4 - Seite mit bis zu vier Badges
* Namen werden vergrößert dargestellt (max. font size: 70)
* PDF Metainformationen hinzugefügt



#### Tab 1
* Hintergrundbild der Badges auswählen
    * Bild kann per Photoshop erzeugt werden
    * gelbes Bild für Tutoren liegt hier bei
* Titel der Badges eingeben
    * z.B. Tutor, Orga, VIP
    * Text wird automatisch generiert

#### Tab 2
* Liste aller Namen und Daten muss eingelesen werden
    * benötigtes Format: csv (als .csv oder .txt)
    * jede Zeile stellt eine Person dar
    * Informationen werden per Komma getrennt 
    * Beispiel-Datei liegt bei: `namen.csv`
    
Beispiel: `Vorname Nachname;Spitzname;Studiengang;Matrikel`

* Alternative: Personen können direkt in Tabelle eingetragen werden
    * Anzahl ist auf vier begrenzt
* per Datei eingelesene Daten können in der Tabelle bearbeitet werden


#### Tab 3
* auf Klick des Buttons wird das PDF erzeugt und mit dem Standard-PDF-Reader geöffnet
* jede Seite des PDFs umfasst eine Badgeseite
* per Ducker Einstellungen können mehrere Badges auf eine A4-Seite gedruckt werden