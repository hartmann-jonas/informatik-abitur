import tkinter as tk
import random

GRID_SIZE = 5  # Könte dynamisch angepasst werden
# (Fensterbreite - Padding vom Spielfeld) / Größe des Grids (5 Felder)
FIELD_SIZE = (500-20)/GRID_SIZE  # Größe der Felder in Pixeln


class LightsOut:
    def __init__(self, root, backToMenu):
        # Hauptfenster übergeben
        self.root = root

        # Startvariablen definieren
        self.move_count = 0
        self.round_count = 0

        # Spielfenster erstellen
        self.showGame(backToMenu)

        # Zustände des Spiels initialisieren
        self.fields = {}
        self.states = self.generate_states()

        # Spielfeld aufbauen
        self.build_grid()

    def generate_states(self):
        print("Generiere Zustände")
        # Run counter der die Durchläufe zählt, bis eine lösbare Startkonfiguration gefunden wurde
        run = 1

        # While-Schleife läuft solange, bis eine lösbare Konfiguration gefunden wurde
        while True:
            # Zufällige Konfiguration bestehend aus 0 und 1 generieren
            states = [[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                
            # Einfacher Test auf Lösbarkeit durch Summen
            # https://puzzling.stackexchange.com/a/123076
            sum1 = states[0][0]+states[0][1]+states[0][3]+states[0][4]+states[2][0]+states[2][1]+states[2][3]+states[2][4]+states[4][0]+states[4][1]+states[4][3]+states[4][4]
            sum2 = states[0][0]+states[0][2]+states[0][4]+states[1][0]+states[1][2]+states[1][4]+states[3][0]+states[3][2]+states[3][4]+states[4][0]+states[4][2]+states[4][4]
            
            # Run counter mit jedem Durchlauf erhöhen
            print(f"Try: {run}")
            run += 1
            
            # Wenn beide Summen gerade sind, also die Konfiguration lösbar ist
            if sum1 % 2 == 0 and sum2 % 2 == 0:
                # Dann wird die While-Schleife durchbrochen und anschließend die Konfiguration zurückgegeben
                break
        return states

    def build_grid(self):
        # Button für Kacheln auf dem Spielfeld erstellen
        # Beide Schleifen iterieren über die x und y Koordinaten der Kacheln
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # Wenn der Zustand des jeweiligen Kachel 1 (an) ist, dann wird das Feld gelb gefärbt
                # wenn nicht dann schwarz
                color = self.get_color(x, y)
                # Field beschreibt die Rechtecke (Kacheln) auf dem Canvas
                # Diese sind werden mit color, wie oben für das Kachel definiert ausgefüllt
                field = self.game.create_rectangle(x * FIELD_SIZE, y * FIELD_SIZE, (x + 1) * FIELD_SIZE, (y + 1) * FIELD_SIZE, fill=color, outline='black')
                self.game.grid_configure(row=0, column=0, columnspan=GRID_SIZE)
                # self.fields ist ein Dictionary, welches den Koordinaten den Kacheln Nummern (IDs) zuordnet
                self.fields[(x, y)] = field
                # Diese ID wird benötigt um den Kacheln (canvas rectangles) Events zuzuordnen
                # Das Event bedeutet hier, dass ein Klick auf das Feld self.toggle(x, y) aufruft
                self.game.tag_bind(field, '<Button-1>', lambda event, x=x, y=y: self.toggle(x, y))

    # Toggle-Funktion um die Kacheln umschalten
    def toggle(self, x, y):
        # Beim Klicken die angrenzenden Kacheln umschalten
        # For-Schleife iteriert über die angrenzenden Kacheln
        for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            # nx und ny sind die Koordinaten der jeweiligen Nachbarkacheln
            nx, ny = x + dx, y + dy
            # Das Feld muss innerhalb des Rasters liegen
            # Es wird nur umgeschaltet, wenn das Feld innerhalb des Spielbretts liegt
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                # XOR-Operator wird als Umschalter verwendet
                self.states[ny][nx] ^= 1
                self.game.itemconfig(self.fields[(nx, ny)], fill=self.get_color(nx, ny))

        # Zähler erhöhen (+= 1) und Label aktualisieren
        self.move_count += 1
        self.clicks_label.config(text=f"Züge: {self.move_count}")

        # Nach jedem Zug prüfen, ob das Spiel gewonnen wurde
        if self.check_win():
            self.show_win_message()

    # Gibt die Farbe der Kachel x y zurück
    def get_color(self, x, y):
        # Wenn der Zustand des Feldes 1 ist yellow, sonst black
        return "yellow" if self.states[y][x] == 1 else "black"

    # Prüft ob das Spiel gewonnen wurde
    def check_win(self):
        # Prüfen, ob das Spiel gewonnen wurde (alle Felder sind schwarz)
        return all(not cell for row in self.states for cell in row)

    # Popup-Fenster für Gewinnnachricht
    def show_win_message(self):
        # Kreeiert ein neues Fenster, mit dem Titel "Gewonnen!"
        win_popup = tk.Toplevel(self.root)
        win_popup.title("Gewonnen!")
        # Kurze Nachricht, in wie vielen Zügen Spiel gewonnen wurde
        tk.Label(win_popup, text=f"Du hast in {self.move_count} Zügen gewonnen!", font=("Arial", 14)).pack(pady=10)
        # Rundenanzahl um 1 erhöhen
        self.round_count += 1
        self.rounds_label.config(text=f"Runde: {self.round_count}")
        # Lambda um Popup zu schließen und gleichzeitig das Spiel zurückzusetzen
        # Lambda, da mehrere Funktionen bei einem Klick ausgeführt werden sollen
        tk.Button(win_popup, text="OK", command=lambda: [self.reset(), win_popup.destroy()]).pack(pady=5)

    # Reset-Funktion für das Spielfeld, generiert neue Startkonfiguration
    def reset(self):
        print("Zurücksetzen")
        # Züge zurücksetzen
        self.move_count = 0
        # Fields leeren
        self.fields = {}
        # Label aktualisieren
        self.clicks_label.config(text="Züge: 0")

        # Neu generierte Zustände für die jeweiligen Felder
        self.states = self.generate_states()
        # Baut das neue Spielfeld mit den neuen Zuständen auf
        self.build_grid()

    # Canvas für Spiel erstellen
    def showGame(self, backToMenu):
        # Ändert den Titel des Fensters
        self.root.title("Lichter Aus - Spiel")
        # Erstellt das Spielfeld als Canvas
        # Breite und Höhe werden aus Anzahl mal der Größe der Felder berechnet
        self.game = tk.Canvas(self.root, width=GRID_SIZE * FIELD_SIZE, height=GRID_SIZE * FIELD_SIZE)
        # Fügt das Canvas Element dem Grid hinzu
        self.game.grid(padx=10, pady=10)

        self.clicks_label = tk.Label(self.root, text="Züge: 0", font=("Arial", 14))
        self.clicks_label.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, pady=10)

        self.rounds_label = tk.Label(self.root, text="Runde: 0", font=("Arial", 14))
        self.rounds_label.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE, pady=10)

        self.solve_button = tk.Button(self.root, text="Menü", command=backToMenu)
        self.solve_button.grid(row=GRID_SIZE + 2, column=0, columnspan=GRID_SIZE, pady=10)
    
        self.reset_button = tk.Button(self.root, text="Zurücksetzen", command=self.reset)
        self.reset_button.grid(row=GRID_SIZE + 3, column=0, columnspan=GRID_SIZE, pady=10)