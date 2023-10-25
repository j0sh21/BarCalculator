import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import json

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    getraenke_name = Column(String(255), nullable=False)
    anzahl_getraenke = Column(Integer, nullable=False)
    speisen_name = Column(String(255), nullable=False)
    anzahl_speisen = Column(Integer, nullable=False)
    user = relationship('User', back_populates='orders')
    tisch = Column(String(255), nullable=False)
    abgerechnet = Column(Integer, default=0, nullable=False)

# Funktion zum Laden der Preise aus der Datei (wenn vorhanden)
def lade_preise():
    try:
        with open(daten_datei, "r") as file:
            daten = json.load(file)
            getraenke_preise= daten["getraenke"]
            essen_preise = daten["essen"]
        global money_total
        return getraenke_preise, essen_preise
    except (FileNotFoundError, json.JSONDecodeError):
        return {"getraenke": preise, "essen": essen}  # Verwenden Sie die Standardpreise, wenn keine Datei vorhanden oder Fehler beim Laden auftritt.


# Funktion zum Speichern der aktuellen Preise in der Datei
def speichere_preise():
    daten = {"getraenke": preise, "essen": essen}
    with open(daten_datei, "w") as file:
        json.dump(daten, file, indent=4)




# Funktion zum Berechnen des Gesamtpreises für den ausgewählten Tisch
# Funktion zum Berechnen des Gesamtpreises für den ausgewählten Tisch
def berechne_gesamtpreis_fuer_tisch():
    tisch = tisch_auswahl.get()
    username = "Tony"  # Hier den gewünschten Benutzernamen eintragen
    session_init = connect_db()
    session = session_init()
    user = session.query(User).filter_by(username=username).first()

    if user:
        gesamtpreis_tisch = 0  # Initialisieren Sie den Gesamtpreis für diesen Tisch

        for order in user.orders:
            if order.tisch == tisch and order.abgerechnet == 0:  # Prüfen Sie die 'abgerechnet'-Spalte
                getraenke_name = order.getraenke_name
                anzahl_getraenke = order.anzahl_getraenke
                speisen_name = order.speisen_name
                anzahl_speisen = order.anzahl_speisen

                if anzahl_getraenke:
                    getraenke_preis = preise[getraenke_name] * anzahl_getraenke
                else:
                    getraenke_preis = 0
                if anzahl_speisen:
                    speisen_preis = essen[speisen_name] * anzahl_speisen
                else:
                    speisen_preis = 0
                gesamtpreis_tisch += getraenke_preis + speisen_preis

        gesamtpreis_label.config(text=f"Gesamtpreis für {tisch}: {gesamtpreis_tisch} $", font=("Helvetica", 16))
        notizen_entry.delete(0, "end")  # Leeren Sie das Notizenfeld
        notizen_entry.insert(0, notizen)  # Setzen Sie die Notizen in das Notizenfeld
    else:
        notizen_entry.delete(0, "end")  # Leeren Sie das Notizenfeld
        gesamtpreis_label.config(text="Gesamtpreis: 0 $")


# Funktion zum Anzeigen nicht abgerechneter Bestellungen für den ausgewählten Tisch
def anzeigen_nicht_abgerechnete_bestellungen():
    tisch = tisch_auswahl.get()
    bestellungen = get_bestellungen_fuer_nutzer_und_tisch(1, tisch, 0)

    # Leeren Sie das Textfeld
    bestellungen_text.delete("1.0", "end")

    gesamtpreis_tisch = 0

    for order in bestellungen:
        getraenke_name = order.getraenke_name
        anzahl_getraenke = order.anzahl_getraenke
        speisen_name = order.speisen_name
        anzahl_speisen = order.anzahl_speisen

        if anzahl_getraenke:
            getraenke_preis = preise[getraenke_name] * anzahl_getraenke
        else:
            getraenke_preis = 0
        if anzahl_speisen:
            speisen_preis = essen[speisen_name] * anzahl_speisen
        else:
            speisen_preis = 0
        gesamtpreis_tisch += getraenke_preis + speisen_preis

        text = f"{getraenke_name} ({anzahl_getraenke}x), {speisen_name} ({anzahl_speisen}x)\n"
        bestellungen_text.insert("end", text)

    gesamtpreis_label.config(text=f"Gesamtpreis für {tisch}: {gesamtpreis_tisch} $", font=("Helvetica", 16))


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

    gesamtpreis_label.config(text=f"Preis: {gesamtpreis} $", font=("Helvetica", 16))
    aktualisiere_bestellungen_text()

    # Setzen Sie die Notizen in das Notizenfeld
    notizen_entry.delete(0, "end")
    notizen_entry.insert(0, notizen)

# Funktion zum Abrufen der Bestellungen für einen bestimmten Nutzer und Tisch
def get_bestellungen_fuer_nutzer_und_tisch(nutzername, tisch, abgerechnet):
    # Ersetzen Sie 'your_username', 'your_password', 'your_host', 'your_port' und 'your_database' durch Ihre eigenen Werte
    db_username = 'bar'
    db_password = 'hAKi0M12cMAX72NVgBee'
    db_host = '85.215.47.24'  # Zum Beispiel: 'localhost'
    db_port = '3306'  # Zum Beispiel: '3306'
    db_name = 'bar'

    # Erstellen Sie die Verbindungs-URL
    db_url = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Erstellen Sie die Engine
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Führen Sie eine Abfrage in der Datenbank durch, um die Bestellungen für den angegebenen Nutzer und Tisch abzurufen
    bestellungen = session.query(Order).filter_by(user_id=nutzername, tisch=tisch, abgerechnet=abgerechnet).all()

    # Schließen Sie die Datenbankverbindung
    session.close()

    return bestellungen
def aktualisiere_bestellungen_text():
    tisch = tisch_auswahl.get()
    if tisch in tisch_bestellungen:


        bestellungen = tisch_bestellungen[tisch]
        bestellungen_text.delete("1.0", "end")  # Lösche den aktuellen Text

        gesamtpreis_tisch = 0  # Initialisieren Sie den Gesamtpreis für diesen Tisch

        session_init = connect_db()
        session = session_init()

        bestellungen = session.query(Order).filter_by(user_id=1, tisch=tisch, abgerechnet=0).all()

        if bestellungen:
            for order in bestellungen:
                getraenke_name = order.getraenke_name
                anzahl_getraenke = order.anzahl_getraenke
                speisen_name = order.speisen_name
                anzahl_speisen = order.anzahl_speisen

                if anzahl_getraenke:
                    getraenke_preis = preise[getraenke_name] * anzahl_getraenke
                else:
                    getraenke_preis = 0
                if anzahl_speisen:
                    speisen_preis = essen[speisen_name] * anzahl_speisen
                else:
                    speisen_preis = 0
                gesamtpreis_tisch += getraenke_preis + speisen_preis

                text = f"{getraenke_name} ({anzahl_getraenke}x), {speisen_name} ({anzahl_speisen}x)\n"
                bestellungen_text.insert("end", text)

            gesamtpreis_label.config(text=f"Gesamtpreis für {tisch}: {gesamtpreis_tisch} $", font=("Helvetica", 16))
            notizen_entry.delete(0, "end")  # Leeren Sie das Notizenfeld
        else:
            gesamtpreis_label.config(text=f"Gesamtpreis für {tisch}: 0 $", font=("Helvetica", 16))
            notizen_entry.delete(0, "end")

            session.close()
    else:
        bestellungen_text.delete("1.0", "end")
        gesamtpreis_label.config(text="Gesamtpreis: 0 $", font=("Helvetica", 16))
        notizen_entry.delete(0, "end")
    app.update()


def tisch_auswahl_geaendert(event):
    selected_table = tisch_auswahl.get()

    session_init = connect_db()
    session = session_init()

    user = session.query(User).filter_by(username="Tony").first()

    if not user:
        user = User(username="Tony", password="hAKi0M12cMAX72NVgBee")
        session.add(user)
        session.commit()

    user_id = 1
    current_tisch = selected_table  # You need to define selected_table

    orders = session.query(Order).filter_by(user_id=user_id, abgerechnet=0, tisch=current_tisch).all()

    session.close()

    order_texts = []
    for order in orders:
        order_text = f"Order ID: {order.id}\nGetraenke: {order.getraenke_name}, Anzahl: {order.anzahl_getraenke}\nSpeisen: {order.speisen_name}, Anzahl: {order.anzahl_speisen}\nTisch: {order.tisch}\nAbgerechnet: {order.abgerechnet}\n\n"
        order_texts.append(order_text)

    # Clear the existing text in bestellungen_text
    bestellungen_text.delete('1.0', 'end')

    # Insert the order texts into the bestellungen_text widget
    for order_text in order_texts:
        bestellungen_text.insert('end', order_text)

# Funktion zum Leeren des Tischs
def tisch_leeren():
    tisch = tisch_auswahl.get()
    username = "1"  # Hier den gewünschten Benutzernamen eintragen

    if tisch in tisch_bestellungen:
        session_init = connect_db()
        session = session_init()

        for order in session.query(Order).filter_by(user_id=username, tisch=tisch, abgerechnet=0):
            order.abgerechnet = 1
        session.commit()
        session.close()

        # Iterieren Sie durch die Bestellungen und entfernen Sie diejenigen, die dem Benutzernamen entsprechen
        tisch_bestellungen[tisch] = [bestellung for bestellung in tisch_bestellungen[tisch] if bestellung[4] != username]

    if tisch in tisch_notizen:
        tisch_notizen[tisch] = ""  # Leeren Sie die Notizen für diesen Tisch unter Berücksichtigung des Benutzernamens

    # Aktualisieren Sie das Textfeld mit den Bestellungen und den Gesamtpreis
    aktualisiere_ausgewaehlten_tisch()
    berechne_preis()

# Funktion zum Aktualisieren der ausgewählten Tischbestellungen
def aktualisiere_ausgewaehlten_tisch(*args):
    global aktuell_ausgewaehlter_tisch
    anzeigen_nicht_abgerechnete_bestellungen()
    tisch = tisch_auswahl.get()

    if tisch in tisch_bestellungen:
        bestellungen = tisch_bestellungen[tisch]
        bestellungen_text.delete("1.0", "end")  # Lösche den aktuellen Text

        gesamtpreis_tisch = 0  # Initialisieren Sie den Gesamtpreis für diesen Tisch
        session_init = connect_db()
        session = session_init()
        user = session.query(User).filter_by(username="Tony").first()
        if user:
            for order in user.orders:
                getraenke_name = order.getraenke_name
                anzahl_getraenke = order.anzahl_getraenke
                speisen_name = order.speisen_name
                anzahl_speisen = order.anzahl_speisen

                if anzahl_getraenke:
                    getraenke_preis = preise[getraenke_name] * anzahl_getraenke
                else:
                    getraenke_preis = 0
                if anzahl_speisen:
                    speisen_preis = essen[speisen_name] * anzahl_speisen
                else:
                    speisen_preis = 0
                gesamtpreis_tisch += getraenke_preis + speisen_preis

                text = f"{getraenke_name} ({anzahl_getraenke}x), {speisen_name} ({anzahl_speisen}x)\n"
                bestellungen_text.insert("end", text)

            gesamtpreis_label.config(text=f"Gesamtpreis für {tisch}: {gesamtpreis_tisch} $", font=("Helvetica", 16))

            # Aktualisieren des Notizenfelds mit den Notizen für diesen Tisch
            notizen_entry.delete(0, "end")
            notizen_entry.insert(0, tisch_notizen[tisch])

        session.close()
    else:
        bestellungen_text.delete("1.0", "end")
        gesamtpreis_label.config(text="Gesamtpreis: 0 $", font=("Helvetica", 16))
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
    lade_preise()

#Speichere bestellung in DB
def bestellung_speichern():
    bestellung_speichern_old()
    global aktuell_ausgewaehlter_tisch
    tisch = tisch_auswahl.get()
    getraenke_name = getraenke_auswahl.get()
    speisen_name = speisen_auswahl.get()
    anzahl_getraenke = int(getraenke_anzahl_entry.get())
    anzahl_speisen = int(speisen_anzahl_entry.get())
    aktuell_ausgewaehlter_tisch = tisch
    session_init = connect_db()
    session = session_init()

    user = session.query(User).filter_by(username="Tony").first()

    if not user:
        user = User(username="Tony", password="hAKi0M12cMAX72NVgBee")
        session.add(user)
        session.commit()

    order = Order(user=user, getraenke_name=getraenke_name, anzahl_getraenke=anzahl_getraenke,
                  speisen_name=speisen_name, anzahl_speisen=anzahl_speisen, tisch=tisch, abgerechnet=0)
    session.add(order)
    session.commit()

    getraenke_anzahl_entry.delete(0, "end")
    speisen_anzahl_entry.delete(0, "end")

    aktualisiere_bestellungen_text()
    aktualisiere_ausgewaehlten_tisch()
    berechne_preis()
    session.close()


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

def update_trinkgeld():
    global money_total
    new = int(money.get())
    money_total += new
    trinkgeld.config(text=f"{money_total} $", font=("Helvetica", 12))

def connect_db():

    # Ersetzen Sie 'your_username', 'your_password', 'your_host', 'your_port' und 'your_database' durch Ihre eigenen Werte
    db_username = 'bar'
    db_password = 'hAKi0M12cMAX72NVgBee'
    db_host = '85.215.47.24'  # Zum Beispiel: 'localhost'
    db_port = '3306'  # Zum Beispiel: '3306'
    db_name = 'bar'

    # Erstellen Sie die Verbindungs-URL
    db_url = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Erstellen Sie die Engine
    engine = create_engine(db_url)
    session = sessionmaker(bind=engine)
    # Testen Sie die Verbindung, indem Sie eine Verbindung herstellen und sofort wieder schließen
    try:
        connection = engine.connect()
        print("Erfolgreich mit der Datenbank verbunden.")
        connection.close()
        return session
    except Exception as e:
        print(f"Fehler bei der Verbindung zur Datenbank: {str(e)}")


# Funktion zum Speichern der Bestellungen auf den Tisch
def bestellung_speichern_old():
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


def create_tables():
    engine = create_engine('mysql+mysqlconnector://bar:hAKi0M12cMAX72NVgBee@85.215.47.24:3306/bar')
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # GUI erstellen
    app = tk.Tk()
    app.title("Element Bar & Lounge")

    # Dateiname für die Speicherung der Essens- und Getränkepreise
    daten_datei = "preise.json"
    create_tables()
    # Getränke- und Speisenpreise
    preise, essen = lade_preise()

    money_total = 0

    # Aktuelle Bestellungen für die Tische
    tisch_bestellungen = {}
    tisch_notizen = {}  # Ein Wörterbuch, um Notizen für jeden Tisch zu speichern

    # Aktuell ausgewählter Tisch
    aktuell_ausgewaehlter_tisch = None

    # Tischauswahl
    tisch_label = tk.Label(app, text="Tisch:", font=("Helvetica", 12))
    tisch_label.grid(row=0, column=0)

    tisch_auswahl = tk.StringVar()
    tisch_dropdown = tk.OptionMenu(app, tisch_auswahl, "Tisch 1", "Tisch 2", "Tisch 3", "Tisch 4", "Tisch 5", "Tisch 6",
                                   "Tisch 7", "Außer Haus", command=aktualisiere_ausgewaehlten_tisch)
    tisch_dropdown.grid(row=0, column=1)
    tisch_dropdown.bind("<Configure>", tisch_auswahl_geaendert)

    # Getränkeauswahl
    getraenke_label = tk.Label(app, text="Getränke:", font=("Helvetica", 12))
    getraenke_label.grid(row=1, column=0)

    getraenke_auswahl = tk.StringVar()
    getraenke_dropdown = tk.OptionMenu(app, getraenke_auswahl, *preise.keys())
    getraenke_dropdown.grid(row=1, column=1)

    getraenke_anzahl_label = tk.Label(app, text="Anzahl:", font=("Helvetica", 12))
    getraenke_anzahl_label.grid(row=2, column=0)

    getraenke_anzahl_entry = tk.Entry(app)
    getraenke_anzahl_entry.grid(row=2, column=1)

    # Speisenauswahl
    speisen_label = tk.Label(app, text="Speisen:", font=("Helvetica", 12))
    speisen_label.grid(row=3, column=0)

    speisen_auswahl = tk.StringVar()
    speisen_dropdown = tk.OptionMenu(app, speisen_auswahl, *essen.keys())
    speisen_dropdown.grid(row=3, column=1)

    speisen_anzahl_label = tk.Label(app, text="Anzahl:", font=("Helvetica", 12))
    speisen_anzahl_label.grid(row=4, column=0)

    speisen_anzahl_entry = tk.Entry(app)
    speisen_anzahl_entry.grid(row=4, column=1)

    # Notizenfeld
    notizen_label = tk.Label(app, text="Notizen:", font=("Helvetica", 12))
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
    bestellungen_text.grid(row=9, column=0)

    # Label für den Gesamtpreis
    gesamtpreis_label = tk.Label(app, text="Gesamtpreis: 0 $", font=("Helvetica", 16))
    gesamtpreis_label.grid()

    # Button zum Berechnen des Gesamtpreises für den ausgewählten Tisch
    berechnen_tisch_button = tk.Button(app, text="Rechnung Bitte", command=berechne_gesamtpreis_fuer_tisch)
    berechnen_tisch_button.grid(row=9, column=1)

    # Button zum Leeren des Tischs
    tisch_leeren_button = tk.Button(app, text="Tisch leeren", command=tisch_leeren)
    tisch_leeren_button.grid(row=10, column=1)

    # Button für die Optionen
    optionen_button = tk.Button(app, text="Optionen", command=optionen_menu)
    optionen_button.grid(row=11, column=1)

    # Button für Trinkgelder
    trinkgeld_button = tk.Button(app, text="Trinkgeld", command=update_trinkgeld)
    trinkgeld_button.grid(row=12, column=1)

    # Label für Trinkgelder
    trinkgeld = tk.Label(app, text="0 $", font=("Helvetica", 16))
    trinkgeld.grid()

    money = tk.IntVar()
    money = tk.Entry(app)
    money.grid()

    app.mainloop()
