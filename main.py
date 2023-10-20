import tkinter as tk

import json  # Importieren Sie die JSON-Bibliothek, um Daten in einer Datei zu speichern und zu laden.


# Funktion zum Laden der Preise aus der Datei (wenn vorhanden)
def lade_preise():
    try:
        with open(daten_datei, "r") as file:
            daten = json.load(file)
            getraenke_preise= daten["getraenke"]
            essen_preise = daten["essen"]
        return getraenke_preise, essen_preise
    except (FileNotFoundError, json.JSONDecodeError):
        return {"getraenke": preise, "essen": essen}  # Verwenden Sie die Standardpreise, wenn keine Datei vorhanden oder Fehler beim Laden auftritt.


# Funktion zum Speichern der aktuellen Preise in der Datei
def speichere_preise():
    daten = {"getraenke": preise, "essen": essen}
    with open(daten_datei, "w") as file:
        json.dump(daten, file, indent=4)




# Funktion zum Berechnen des Gesamtpreises für den ausgewählten Tisch
def berechne_gesamtpreis_fuer_tisch():
    tisch = tisch_auswahl.get()
    if tisch in tisch_bestellungen:
        bestellungen = tisch_bestellungen[tisch]
        gesamtpreis_tisch = 0  # Initialisieren Sie den Gesamtpreis für diesen Tisch

        for bestellung in bestellungen:
            getraenke_name, anzahl_getraenke, speisen_name, anzahl_speisen, _ = bestellung
            if anzahl_getraenke:
                getraenke_preis = preise[getraenke_name] * anzahl_getraenke
            else:
                getraenke_preis = 0
            if anzahl_speisen:
                speisen_preis = essen[speisen_name] * anzahl_speisen
            else:
                speisen_preis = 0
            gesamtpreis_tisch += getraenke_preis + speisen_preis

        gesamtpreis_label.config(text=f"Gesamtpreis für {tisch}: {gesamtpreis_tisch} $")
        notizen_entry.delete(0, "end")  # Löschen Sie den Inhalt des Notizenfelds
        notizen_entry.insert(0, notizen)  # Setzen Sie die Notizen in das Notizenfeld
    else:
        notizen_entry.delete(0, "end")  # Löschen Sie den Inhalt des Notizenfelds
        gesamtpreis_label.config(text="Gesamtpreis: 0 $")


# Funktion, um den Gesamtpreis zu berechnen
def berechne_preis():
    getraenke_name = getraenke_auswahl.get()
    speisen_name = speisen_auswahl.get()
    anzahl_getraenke = getraenke_anzahl_entry.get()
    anzahl_speisen = speisen_anzahl_entry.get()
    notizen = notizen_entry.get()  # Notizen aus dem Notizenfeld

    getraenke_preis = preise[getraenke_name] * int(anzahl_getraenke) if anzahl_getraenke else 0
    speisen_preis = essen[speisen_name] * int(anzahl_speisen) if anzahl_speisen else 0
    gesamtpreis = getraenke_preis + speisen_preis

    gesamtpreis_label.config(text=f"Gesamtpreis: {gesamtpreis} $")
    aktualisiere_bestellungen_text()

    # Setzen Sie die Notizen in das Notizenfeld
    notizen_entry.delete(0, "end")
    notizen_entry.insert(0, notizen)


# Funktion zum Aktualisieren des Textfelds mit den Bestellungen
def aktualisiere_bestellungen_text():
    tisch = tisch_auswahl.get()
    if tisch in tisch_bestellungen:
        bestellungen = tisch_bestellungen[tisch]
        bestellungen_text.delete("1.0", "end")  # Lösche den aktuellen Text

        for bestellung in bestellungen:
            getraenke_name, anzahl_getraenke, speisen_name, anzahl_speisen, _ = bestellung
            text = f"{getraenke_name} ({anzahl_getraenke} Stück), {speisen_name} ({anzahl_speisen} Stück)\n"
            bestellungen_text.insert("end", text)


# Funktion zum Speichern der Bestellungen auf den Tisch
def bestellung_speichern():
    global aktuell_ausgewaehlter_tisch
    global notizen
    tisch = tisch_auswahl.get()
    getraenke_name = getraenke_auswahl.get()
    speisen_name = speisen_auswahl.get()
    anzahl_getraenke = getraenke_anzahl_entry.get()
    anzahl_speisen = speisen_anzahl_entry.get()
    notizen = notizen_entry.get()  # Notizen aus dem Notizenfeld

    if tisch not in tisch_bestellungen:
        tisch_bestellungen[tisch] = []

    # Überprüfen, ob bereits Bestellungen für diesen Tisch vorhanden sind
    bestellungen_fuer_tisch = tisch_bestellungen[tisch]
    gefunden = False

    for index, bestellung in enumerate(bestellungen_fuer_tisch):
        getraenke_alt, anzahl_getraenke_alt, speisen_alt, anzahl_speisen_alt, _ = bestellung
        if getraenke_alt == getraenke_name and speisen_alt == speisen_name:
            # Bestellung gefunden, füge die Anzahl hinzu
            bestellungen_fuer_tisch[index] = (
            getraenke_name, int(anzahl_getraenke_alt) + int(anzahl_getraenke), speisen_name,
            int(anzahl_speisen_alt) + int(anzahl_speisen), notizen)
            gefunden = True
            break

    if not gefunden:
        # Bestellung nicht gefunden, füge sie hinzu, und setze die Anzahl auf 0, wenn das Feld leer ist
        tisch_bestellungen[tisch].append((
                                         getraenke_name, int(anzahl_getraenke) if anzahl_getraenke else 0, speisen_name,
                                         int(anzahl_speisen) if anzahl_speisen else 0, notizen))

    if not tisch in tisch_notizen:
        tisch_notizen[tisch] = ""

    tisch_notizen[tisch] = notizen  # Aktualisieren der Notizen für den Tisch

    aktuell_ausgewaehlter_tisch = tisch

    # Aktualisiere das Textfeld mit den Bestellungen
    aktualisiere_bestellungen_text()
    # Aktualisiere das Textfeld mit den Bestellungen und den Gesamtpreis
    aktualisiere_ausgewaehlten_tisch()
    berechne_preis()

    # Leere die Eingaben für Anzahl, Getränke und Speisen
    getraenke_auswahl.set("")
    speisen_auswahl.set("")
    getraenke_anzahl_entry.delete(0, "end")
    speisen_anzahl_entry.delete(0, "end")
    #notizen_entry.delete(0, "end")  # Leere das Notizenfeld


# Funktion zum Leeren des Tischs
def tisch_leeren():
    tisch = tisch_auswahl.get()
    if tisch in tisch_bestellungen:
        del tisch_bestellungen[tisch]

    if tisch in tisch_notizen:
        del tisch_notizen[tisch]

    # Aktualisiere das Textfeld mit den Bestellungen und den Gesamtpreis
    aktualisiere_ausgewaehlten_tisch()
    berechne_preis()


# Funktion zum Aktualisieren der ausgewählten Tischbestellungen
def aktualisiere_ausgewaehlten_tisch(*args):
    global aktuell_ausgewaehlter_tisch
    tisch = tisch_auswahl.get()
    if tisch in tisch_bestellungen:
        bestellungen = tisch_bestellungen[tisch]
        bestellungen_text.delete("1.0", "end")  # Lösche den aktuellen Text

        gesamtpreis_tisch = 0  # Initialisieren Sie den Gesamtpreis für diesen Tisch

        for bestellung in bestellungen:
            getraenke_name, anzahl_getraenke, speisen_name, anzahl_speisen, notizen = bestellung

            if anzahl_getraenke:
                getraenke_preis = preise[getraenke_name] * anzahl_getraenke
            else:
                getraenke_preis = 0
            if anzahl_speisen:
                speisen_preis = essen[speisen_name] * anzahl_speisen
            else:
                speisen_preis = 0
            gesamtpreis_tisch += getraenke_preis + speisen_preis

            text = f"{getraenke_name} ({anzahl_getraenke} Stück), {speisen_name} ({anzahl_speisen} Stück)\n"
            bestellungen_text.insert("end", text)

        gesamtpreis_label.config(text=f"Gesamtpreis für {tisch}: {gesamtpreis_tisch} $")

        # Aktualisieren des Notizenfelds mit den Notizen für diesen Tisch
        notizen_entry.delete(0, "end")
        notizen_entry.insert(0, tisch_notizen[tisch])

    else:
        bestellungen_text.delete("1.0", "end")
        gesamtpreis_label.config(text="Gesamtpreis: 0 $")
        notizen_entry.delete(0, "end")  # Leere das Notizenfeld

    # Aktualisiere die Anzeige
    app.update()

# Funktion zum Öffnen des Preise-Menüs
def optionen_menu():
    global optionen_fenster
    optionen_fenster = tk.Toplevel(app)
    optionen_fenster.title("Optionen")


    # Änderung und Hinzufügung von Getränken
    getraenke_optionen_label = tk.Label(optionen_fenster, text="Getränkeoptionen:")
    getraenke_optionen_label.grid()
    row = 1  # Startzeile im Grid
    for getraenk, preis in preise.items():
        # Label für Getränkenamen
        getraenke_name_label = tk.Label(optionen_fenster, text="Name für " + getraenk + ":")
        getraenke_name_label.grid(row=row, column=0)
        getraenke_name_label.grid_configure(padx=5, pady=5)  # Abstand hinzufügen

        # Eingabe für Getränkenamen
        getraenke_name_entry = tk.Entry(optionen_fenster)
        getraenke_name_entry.insert(0, getraenk)
        getraenke_name_entry.grid(row=row, column=1)
        getraenke_name_entries[getraenk] = getraenke_name_entry

        # Label für Getränkepreise
        getraenke_preis_label = tk.Label(optionen_fenster, text="Preis für " + getraenk + ":")
        getraenke_preis_label.grid(row=row, column=2)
        getraenke_preis_label.grid_configure(padx=5, pady=5)  # Abstand hinzufügen

        # Eingabe für Getränkepreise
        getraenke_preis_entry = tk.Entry(optionen_fenster)
        getraenke_preis_entry.insert(0, str(preis))
        getraenke_preis_entry.grid(row=row, column=3)
        getraenke_preis_entries[getraenk] = getraenke_preis_entry

        row += 1



    # Änderung und Hinzufügung von Speisen (analog zu Getränken)
    speisen_optionen_label = tk.Label(optionen_fenster, text="Speisenoptionen:")
    speisen_optionen_label.grid(row=0, column=0, columnspan=4)  # Erste Zeile mit vier Spalten

    row = 1  # Startzeile im Grid

    for speise, preis in essen.items():
        # Label für Speisenname
        speisen_name_label = tk.Label(optionen_fenster, text="Name für " + speise + ":")
        speisen_name_label.grid(row=row, column=0)
        speisen_name_label.grid_configure(padx=5, pady=5)  # Abstand hinzufügen

        # Eingabe für Speisenname
        speisen_name_entry = tk.Entry(optionen_fenster)
        speisen_name_entry.insert(0, speise)
        speisen_name_entry.grid(row=row, column=1)
        speisen_name_entries[speise] = speisen_name_entry

        # Label für Speisenpreise
        speisen_preis_label = tk.Label(optionen_fenster, text="Preis für " + speise + ":")
        speisen_preis_label.grid(row=row, column=2)
        speisen_preis_label.grid_configure(padx=5, pady=5)  # Abstand hinzufügen

        # Eingabe für Speisenpreise
        speisen_preis_entry = tk.Entry(optionen_fenster)
        speisen_preis_entry.insert(0, str(preis))
        speisen_preis_entry.grid(row=row, column=3)
        speisen_preis_entries[speise] = speisen_preis_entry

        row += 1

    # Button zum Speichern der Preise und Namen
    speichern_optionen_button = tk.Button(optionen_fenster, text="Optionen speichern", command=speichern_optionen)
    speichern_optionen_button.grid()


# Funktion zum Speichern der Preise und Namen aus dem Optionen-Menü
def speichern_optionen():
    # Änderungen und Hinzufügungen von Getränken
    for getraenk, entry in getraenke_name_entries.items():
        neuer_name = entry.get()
        if neuer_name != getraenk:
            preise[neuer_name] = preise.pop(getraenk)

    for getraenk, entry in getraenke_preis_entries.items():
        preis = entry.get()
        preise[getraenk] = float(preis)

    # Hinzufügen eines neuen Getränks
    if neues_getraenk_name_entry:
        neues_getraenk_name = neues_getraenk_name_entry.get()
    if neues_getraenk_preis_entry:
        neues_getraenk_preis = neues_getraenk_preis_entry.get()
    if neues_getraenk_name_entry and neues_getraenk_preis:
        preise[neues_getraenk_name] = float(neues_getraenk_preis)

    # Änderungen und Hinzufügungen von Speisen (analog zu Getränken)
    for speise, entry in speisen_name_entries.items():
        neuer_name = entry.get()
        if neuer_name != speise:
            essen[neuer_name] = essen.pop(speise)

    for speise, entry in speisen_preis_entries.items():
        preis = entry.get()
        essen[speise] = float(preis)
    if neues_speise_name_entry:
        neues_speise_name = neues_speise_name_entry.get()
    if neues_speise_preis_entry:
        neues_speise_preis = neues_speise_preis_entry.get()
    if neues_speise_name_entry and neues_speise_preis_entry:
        essen[neues_speise_name] = float(neues_speise_preis)

    speichere_preise()
    app.update()  # Aktualisieren Sie die Anwendung, um die Änderungen anzuzeigen

    optionen_fenster.destroy()


if __name__ == "__main__":
    # GUI erstellen
    app = tk.Tk()
    app.title("Element Bar & Lounge")

    # Dateiname für die Speicherung der Essens- und Getränkepreise
    daten_datei = "preise.json"

    # Getränke- und Speisenpreise
    preise, essen = lade_preise()

    # Aktuelle Bestellungen für die Tische
    tisch_bestellungen = {}
    tisch_notizen = {}  # Ein Wörterbuch, um Notizen für jeden Tisch zu speichern

    # Aktuell ausgewählter Tisch
    aktuell_ausgewaehlter_tisch = None

    # Tischauswahl
    tisch_label = tk.Label(app, text="Tisch auswählen:")
    tisch_label.grid(row=0, column=0)

    tisch_auswahl = tk.StringVar()
    tisch_dropdown = tk.OptionMenu(app, tisch_auswahl, "Tisch 1", "Tisch 2", "Tisch 3", "Tisch 4", "Tisch 5", "Tisch 6",
                                   "Tisch 7", "Tisch 8", command=aktualisiere_ausgewaehlten_tisch)
    tisch_dropdown.grid(row=0, column=1)

    # Getränkeauswahl
    getraenke_label = tk.Label(app, text="Getränke auswählen:")
    getraenke_label.grid(row=1, column=0)

    getraenke_auswahl = tk.StringVar()
    getraenke_dropdown = tk.OptionMenu(app, getraenke_auswahl, *preise.keys())
    getraenke_dropdown.grid(row=1, column=1)

    getraenke_anzahl_label = tk.Label(app, text="Anzahl:")
    getraenke_anzahl_label.grid(row=2, column=0)

    getraenke_anzahl_entry = tk.Entry(app)
    getraenke_anzahl_entry.grid(row=2, column=1)

    # Speisenauswahl
    speisen_label = tk.Label(app, text="Speisen auswählen:")
    speisen_label.grid(row=3, column=0)

    speisen_auswahl = tk.StringVar()
    speisen_dropdown = tk.OptionMenu(app, speisen_auswahl, *essen.keys())
    speisen_dropdown.grid(row=3, column=1)

    speisen_anzahl_label = tk.Label(app, text="Anzahl:")
    speisen_anzahl_label.grid(row=4, column=0)

    speisen_anzahl_entry = tk.Entry(app)
    speisen_anzahl_entry.grid(row=4, column=1)

    # Notizenfeld
    notizen_label = tk.Label(app, text="Notizen:")
    notizen_label.grid(row=5, column=0)

    notizen_entry = tk.Entry(app)
    notizen_entry.grid(row=5, column=1)

    # Funktion zum Öffnen des Preise-Menüs
    # Globale Variablen für die Eingabefelder der Preise
    getraenke_preis_entries = {}
    speisen_preis_entries = {}

    getraenke_name_entries = {}
    speisen_name_entries = {}

    neues_speise_name_entry = {}
    neues_speise_preis_entry = {}

    neues_getraenk_name_entry = {}
    neues_getraenk_preis_entry = {}



    # Button zum Berechnen des Gesamtpreises
    berechnen_button = tk.Button(app, text="Sofort Zahlen", command=berechne_preis)
    berechnen_button.grid(row=8, column=1)

    # Button zum Speichern der Bestellung
    speichern_button = tk.Button(app, text="Hinzufügen", command=bestellung_speichern)
    speichern_button.grid(row=7, column=1)



    # Textfeld für Bestellungen
    bestellungen_text = tk.Text(app, height=10, width=40)
    bestellungen_text.grid()

    # Label für den Gesamtpreis
    gesamtpreis_label = tk.Label(app, text="Gesamtpreis: 0 $")
    gesamtpreis_label.grid()

    # Button zum Berechnen des Gesamtpreises für den ausgewählten Tisch
    berechnen_tisch_button = tk.Button(app, text="Rechnung Bitte", command=berechne_gesamtpreis_fuer_tisch)
    berechnen_tisch_button.grid()

    # Button zum Leeren des Tischs
    tisch_leeren_button = tk.Button(app, text="Tisch leeren", command=tisch_leeren)
    tisch_leeren_button.grid()

    # Button für die Optionen
    optionen_button = tk.Button(app, text="Optionen", command=optionen_menu)
    optionen_button.grid()

    app.mainloop()