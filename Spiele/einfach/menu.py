import tkinter as tk
from game import LightsOut

# Rendert Hauptmenü
def showMenu():
    clearWindow()
    root.title("Lichter Aus - Hauptmenü")
    root.grid()

    # Jede Spalte im Grid auf die gleiche Breite setzen
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)

    # Label für den Titel
    title_label = tk.Label(root, text="Lichter Aus", font=("Arial", 32))
    title_label.grid(row=0, column=1, pady=200)

    # Button zum Starten des Spiels
    start_button = tk.Button(root, text="Spiel starten", command=lambda:startGame())
    start_button.grid(row=1, column=1, pady=10)

    # Button zum Beenden des Spiels
    exit_button = tk.Button(root, text="Beenden", command=root.quit)
    exit_button.grid(row=2, column=1, pady=10)

def startGame():
    clearWindow()
    # Neue Spielinstanz starten
    LightsOut(root, showMenu)

def clearWindow():
    # Alle Widgets im Fenster entfernen
    for widget in root.winfo_children():
        widget.destroy()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x680")
    root.attributes('-fullscreen',True)

    showMenu()

    root.mainloop()

