# 📚 Book Alchemy

Eine kleine Flask-Webanwendung zur Verwaltung von Büchern und Autoren.\
Die App wurde als Lernprojekt für Flask, SQLAlchemy und einfache
Webentwicklung erstellt.

------------------------------------------------------------------------

## 🚀 Features

-   **Autoren hinzufügen** (Name, Geburtsdatum, Todesdatum)
-   **Bücher hinzufügen** (Titel, ISBN, Erscheinungsjahr,
    Autoren-Referenz)
-   **Alle Bücher anzeigen**
-   **Sortierung** nach:
    -   Titel (asc/desc)
    -   Autor (asc/desc)
-   **Volltextsuche** über:
    -   Buchtitel
    -   Autorname
    -   ISBN
-   **Buch löschen**
    -   Falls der Autor danach keine Bücher mehr besitzt, wird dieser
        automatisch mitgelöscht
-   **Flash-Messages** für Erfolg/Fehler
-   SQLite-Datenbank

------------------------------------------------------------------------

## 🧱 Tech Stack

-   **Python 3**
-   **Flask**
-   **Flask SQLAlchemy**
-   **SQLite**
-   HTML (Jinja2 Templates)

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Repository klonen

``` bash
git clone https://github.com/m-tababi/book-alchemy.git
cd book-alchemy
```

### 2. Virtuelle Umgebung erstellen (optional, empfohlen)

``` bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 3. Abhängigkeiten installieren

``` bash
pip install flask flask_sqlalchemy
```

### 4. Datenbank erstellen

``` bash
python
>>> from app import app
>>> from data_models import db
>>> with app.app_context():
...     db.create_all()
```

------------------------------------------------------------------------

## ▶️ Anwendung starten

``` bash
python app.py
```

Die App läuft dann unter:

    http://127.0.0.1:5002/

------------------------------------------------------------------------

## 🗂️ Projektstruktur

    book-alchemy/
    │
    ├── app.py                  
    ├── data_models.py          
    ├── data/
    │   └── library.sqlite      
    │
    ├── templates/
    │   ├── home.html
    │   ├── add_author.html
    │   └── add_book.html
    │
    └── static/                 

------------------------------------------------------------------------

## 🔍 Funktionen im Detail

### 🔸 Sortieren

    /?sort=title&direction=asc
    /?sort=author&direction=desc

### 🔸 Suche

Eingabe durchsucht: - Titel - Autor - ISBN

### 🔸 Löschen

Wenn ein Buch gelöscht wird, wird ggf. auch der Autor gelöscht, falls
keine Bücher mehr existieren.

------------------------------------------------------------------------

## 🙌 Credits

Projekt umgesetzt von **Mohamed Tababi**.

------------------------------------------------------------------------

## 📜 Lizenz

Open Source Projekt.
