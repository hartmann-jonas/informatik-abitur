import tkinter as tk
import numpy as np
import time
import random
from Solver import Solver


class LightsOut():
    def __init__(self, root, gridSize, backToMenu):
        # GRID_SIZE und FIELD_SIZE als globale Variablen definieren
        # Damit andere Funktionen auf die Werte zugreifen können
        global GRID_SIZE
        global FIELD_SIZE

        GRID_SIZE = gridSize  # Größe des Spielfelds
        FIELD_SIZE = (500-20)/GRID_SIZE  # Größe der Felder in Pixeln
        print(FIELD_SIZE)

        self.root = root
        self.root.title("Lichter Aus - Spiel")
        
        self.solver = Solver(size=GRID_SIZE)

        self.game = tk.Canvas(self.root, width=GRID_SIZE * FIELD_SIZE, height=GRID_SIZE * FIELD_SIZE)
        self.game.grid(padx=10, pady=10)

        self.fields = {}
        self.generate_states()

        self.build_grid()

        self.move_count = 0
        self.round_count = 1

        self.clicks_label = tk.Label(self.root, text="Züge: 0", font=("Arial", 14))
        self.clicks_label.grid(row=1, column=0, columnspan=GRID_SIZE, pady=10)

        self.rounds_label = tk.Label(self.root, text=f"Runde: {self.round_count}", font=("Arial", 14))
        self.rounds_label.grid(row=2, column=0, columnspan=GRID_SIZE, pady=10)

        self.solve_button = tk.Button(self.root, text="Menü", command=backToMenu)
        self.solve_button.grid(row=3, column=0, pady=10)

        self.solve_button = tk.Button(self.root, text="Lösen", command=self.solve)
        self.solve_button.grid(row=4, column=0, pady=10)

        self.reset_button = tk.Button(self.root, text="Zurücksetzen", command=self.reset)
        self.reset_button.grid(row=5, column=0, pady=10)

    def generate_states(self):
        print("Generiere Zustände")
        # Run counter der die Durchläufe zählt, bis eine lösbare Startkonfiguration gefunden wurde
        run = 1
        # While-Schleife läuft solange, bis eine lösbare Konfiguration gefunden wurde
        while True:
            # Zufällige Konfiguration bestehend aus 0 und 1 generieren
            self.states = np.array([[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])
            # Solver mit der Startkonfiguration aufrufen, gibt die Lösbarkeit und eine mögliche Lösung zurück
            solved = self.solver.solve(self.states)
            print(f"Try: {run}, {solved[1]}, Time: {solved[2]}")
            # Run counter mit jedem Durchlauf erhöhen
            run += 1
            # Wenn der Solver true zurückgibt, also die Konfiguration lösbar ist
            # Dann wird die While-Schleife durchbrochen und anschließend die Konfiguration zurückgegeben
            if solved[1] == True:
                break
        return self.states

    def build_grid(self):
        # Button auf dem Canvas erstellen
        # Beide Schleifen iterieren über die x und y Koordinaten der Felder
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # Wenn der Zustand des jeweiligen Feldes 1 (an) ist, dann wird das Feld gelb gefärbt
                # wenn nicht dann schwarz
                color = 'yellow' if self.states[y][x] == 1 else 'black'
                # Field beschreibt die Rechtecke (Felder) auf dem Spielfeld (game)
                # Diese sind werden mit color, wie oben für das Feld definiert ausgefüllt
                field = self.game.create_rectangle(x * FIELD_SIZE, y * FIELD_SIZE, (x + 1) * FIELD_SIZE, (y + 1) * FIELD_SIZE, fill=color, outline='black', )
                # self.fields ist ein Dictionary, welches den Koordinaten der Felder Nummern (IDs) zuordnet
                self.fields[(x, y)] = field
                # Diese ID wird benötigt um den Feldern (canvas rectangles) Events zuzuordnen
                # Das Event bedeutet hier, dass ein Klich auf das Feld self.toggle(x, y) aufruft
                self.game.tag_bind(field, '<Button-1>', lambda event, x=x, y=y: self.toggle(x, y))

    def toggle(self, x, y):
        # Beim Klicken die angrenzenden Felder umschalten
        # For-Schleife iteriert über die angrenzenden Felder
        for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            # ny und ny sind die Koordinaten des jeweiligen Nachbarnfeldes
            nx, ny = x + dx, y + dy
            # Feld muss innerhalb des Rasters liegen
            # Es wird nur umgeschaltet, wenn das Feld innerhalb des Spielbretts liegt
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                self.states[ny][nx] ^= 1
                self.game.itemconfig(self.fields[(nx, ny)], fill=self.get_color(nx, ny))

        # Zähler erhöhen (+= 1) und Label aktualisieren
        self.move_count += 1
        self.clicks_label.config(text=f"Züge: {self.move_count}")

        # Nach jedem Zug prüfen, ob das Spiel gewonnen wurde
        if self.check_win():
            self.show_win_message()

    def get_color(self, x, y):
        # Gibt die Farbe des Feldes x y basierend auf dem Zustand zurück
        return "yellow" if self.states[y][x] == 1 else "black"

    def check_win(self):
        # Prüfen, ob das Spiel gewonnen wurde (alle Felder sind schwarz)
        return all(not cell for row in self.states for cell in row)

    def show_win_message(self):
        # Kreeiert ein neues Fenster, mit dem Titel "Gewonnen!"
        win_popup = tk.Toplevel(self.root)
        win_popup.title("Gewonnen!")
        # Kurze Nachricht, in wie vielen Zügen Spiel gewonnen wurde
        tk.Label(win_popup, text=f"Du hast in {self.move_count} Zügen gewonnen!", font=("Arial", 14)).pack(pady=10)
        # Lambda um Popup zu schließen und gleichzeitig das Spiel zurückzusetzen
        # Lambda, da mehrere Funktionen bei einem Klick ausgeführt werden sollen
        tk.Button(win_popup, text="OK", command=lambda: [self.reset(), win_popup.destroy()]).pack(pady=5)

    def solve(self):
        print("Lösen")
        print(1/FIELD_SIZE+0.1)
        # Solver mit Zustandsmatrix aufrufen
        keyMatrix = self.solver.solve(self.states)[0]
        # KeyMatrix ist die Lösung, welche Felder umgeschaltet werden müssen
        # For-Schleife iteriert über die Felder der Lösung
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # Wenn das Feld in der KeyMatrix 1 ist (also geschaltet werden muss)
                if keyMatrix[y][x] == 1:
                    # Dann rufe die toggle Funktion auf diesem Feld auf
                    self.toggle(x, y)
                    # Kurze Pause, damit es ersichtlich ist, welches Feld geschaltet wurde
                    time.sleep(1/GRID_SIZE)
                    # Nach jedem Schalten muss die GUI (self.root) aktualisiert werden
                    self.root.update()

    def reset(self):
        print("Zurücksetzen")
        # Züge zurücksetzen
        self.move_count = 0
        # Label aktualisieren
        self.clicks_label.config(text=f"Züge: {self.move_count}")

        self.round_count += 1
        self.rounds_label.config(text=f"Runde: {self.round_count}")
        
        # Neu generierte Zustände für die jeweiligen Felder
        self.states = self.generate_states()
        self.build_grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = LightsOut(root)
    root.mainloop()
