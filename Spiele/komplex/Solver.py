import numpy as np
import time

class Solver:
    def __init__(self, size):
        self.size = size
        self.n = size * size
        # Übergangsmatrix initialisieren
        self.transitionMatrix = self.build_matrix()

    def build_matrix(self):
        # Übergangsmatrix (Welche Lampe schaltet welche Lampen) erstellen
        A = np.zeros((self.n, self.n), dtype=int)
        for i in range(self.n):
            A[i][i] = 1
            row, col = divmod(i, self.size)
            for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
                if 0 <= r < self.size and 0 <= c < self.size:
                    A[i][r * self.size + c] = 1
        return A

    # Inverse der Übergangsmatrix in mod2
    def get_solutionMatrix(self, A, b):
        n = len(b)
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i+1, n):
                    if A[j][i] == 1:
                        A[[i, j]] = A[[j, i]]
                        b[i], b[j] = b[j], b[i]
                        break
            for j in range(i+1, n):
                if A[j][i] == 1:
                    A[j] ^= A[i]
                    b[j] ^= b[i]
        # Rückwärtseinsetzen
        x = np.zeros(n, dtype=int)
        for i in reversed(range(n)):
            x[i] = (b[i] ^ sum(A[i][j] & x[j] for j in range(i+1, n))) % 2
        return x


    # Prüft ob die Zustandsmatrix lösbar ist
    # Gibt die Lösung uns die Lösbarkeit zurück
    def solve(self, grid):
        # Startzeit für die Berechnung
        timeStart = time.time()
        isSolvable = False
        # Zustandsmatrix, die gelöst werden soll
        # 2D Array in 1D numpy Array umwandeln
        stateVector = np.array([cell for row in grid for cell in row], dtype=int)
        # Lösungsmatrix für gegebenes Feld
        solutionMatrix = self.get_solutionMatrix(self.transitionMatrix.copy(), stateVector.copy())

        # Überprüfen ob die Lösung gültig ist
        # Übergangsmatrix * Lösung + Startzustand = Nullvektor b
        # M x + a = b (Test auf Lösbarkeit)
        testMatrix = np.add(np.linalg.matmul(self.transitionMatrix, solutionMatrix), stateVector)
        np.mod(testMatrix, 2, out=testMatrix)

        # Ist true, wenn die errechnete Lösung nur aus 0en besteht
        # Wenn true, dann ist das Feld lösbar
        allZeros = not np.any(testMatrix)

        # Ist true, wenn die Startkonfiguration nicht nur 0en enthält
        # Dann wäre das Spielbrett bereits gelöst
        startMatrix = np.any(stateVector)

        # Wenn beide Bedingungen erfüllt sind, dann ist das Spielbrett lösbar
        if allZeros and startMatrix:
            isSolvable = True

        # 1D Array in 2D umwandeln
        solutionMatrix = np.reshape(solutionMatrix, (self.size, self.size))

        timeEnd = time.time()
        return[solutionMatrix, isSolvable, timeEnd - timeStart]