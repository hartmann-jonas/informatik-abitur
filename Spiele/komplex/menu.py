import tkinter as tk
from game import LightsOut

# Rendert Hauptmenü
def showMenu():
    clearWindow()
    root.title("Lichter Aus - Hauptmenü")
    root.grid()

    for i in range(3):
        root.grid_columnconfigure(i, weight=1)

    # Label für den Titel
    title_label = tk.Label(root, text="Lichter Aus", font=("Arial", 32))
    title_label.grid(row=0, column=1, pady=80)

    # Label für die Feldgröße
    size_label = tk.Label(root, text="Feldgröße:", font=("Arial", 12))
    size_label.grid(row=1, column=1, pady=10)

    # Eingabefeld für die Feldgröße
    size_entry = tk.IntVar(value = 2)
    tk.Spinbox(root, from_=1, to=100, increment=1, width=5, textvariable=size_entry).grid(row=2, column=1, pady=10)
    # Button zum Starten des Spiels
    start_button = tk.Button(root, text="Spiel starten", command=lambda:startGame(size_entry.get()))
    start_button.grid(row=3, column=1, pady=10)

    # Button zum Beenden des Spiels
    exit_button = tk.Button(root, text="Beenden", command=root.quit)
    exit_button.grid(row=4, column=1, pady=10)

def startGame(size_entry):
    # Größe des Spielfelds aus dem Eingabefeld holen
    gridSize = size_entry
    # Fenster zurücksetzen
    clearWindow()
    # Neue Spielinstanz starten
    LightsOut(root, gridSize, showMenu)

def clearWindow():
    # Alle Widgets im Fenster entfernen
    for widget in root.winfo_children():
        widget.destroy()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x750")
    #root.attributes('-fullscreen',True)

    showMenu()

    root.mainloop()

