import numpy as np
import sympy as sp

def mod2_inv(matrix):
    n = matrix.shape[0]
    # Create augmented matrix [A | I]
    augmented = np.concatenate((matrix, np.eye(n, dtype=int)), axis=1)
    print(np.linalg.det(augmented) % 2)
    for i in range(n):
        # Find pivot
        if augmented[i, i] == 0:
            # Swap with a row below that has a 1 in the ith column
            for j in range(i+1, n):
                if augmented[j, i] == 1:
                    augmented[[i, j]] = augmented[[j, i]]
                    break
        else:
            raise ValueError("Matrix is singular and not invertible in mod 2.")
        
        # Eliminate other rows
        for j in range(n):
            if j != i and augmented[j, i] == 1:
                augmented[j] = (augmented[j] + augmented[i]) % 2
    
    # The right half is the inverse
    return augmented[:, n:]

# Example
A = sp.Matrix([[1, 1, 1, 0],
              [1, 1, 0, 1],
              [1, 0, 1, 1],
              [0, 1, 1, 1]])

print(A.det() % 2)  # Check if determinant is non-zero mod 2

A_inv = A.inv_mod(2) #mod2_inv(A)
print("Inverse modulo 2:\n", A_inv)