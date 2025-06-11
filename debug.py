import random
GRID_SIZE = 5  # Könnte dynamisch angepasst werden

class LightsOut:
    def generate_states(self):
        # While-Schleife läuft solange, bis eine lösbare Konfiguration gefunden wurde
        while True:
            # Zufällige Konfiguration bestehend aus 0 und 1 generieren
            states = [[random.choice([0, 1]) for _ in range(5)] for _ in range(5)]
                
            # Einfacher Test auf Lösbarkeit durch Summen
            # https://puzzling.stackexchange.com/a/123076
            sum1 = states[0][0]+states[0][1]+states[0][3]+states[0][4]+states[2][0]+states[2][1]+states[2][3]+states[2][4]+states[4][0]+states[4][1]+states[4][3]+states[4][4]
            sum2 = states[0][0]+states[0][2]+states[0][4]+states[1][0]+states[1][2]+states[1][4]+states[3][0]+states[3][2]+states[3][4]+states[4][0]+states[4][2]+states[4][4]
            
            # Wenn beide Summen gerade sind, also die Konfiguration lösbar ist
            if sum1 % 2 == 0 and sum2 % 2 == 0:
                # Dann wird die While-Schleife durchbrochen und anschließend die Konfiguration zurückgegeben
                break
        return states