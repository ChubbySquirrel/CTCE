import numpy as np

def create_list(F):
    indices = np.empty(0) #list of all present indices, no repeats
    counter = np.empty(0) #list of how many of each index there are, one-to-one w indices list
    
    #filling in indices and counters
    for j in range(np.shape(F)[1]):
        for i in range(np.shape(F)[0]):
            if F[i, j] in indices:
                mask = indices[:] == F[i, j]
                index = np.nonzero(mask)[0] #finds the index of indices that contains F[i,j]
                counter[index] += 1 #adds a tally to the index in counter corresponding to F[i,j]
            if F[i, j] not in indices:
                indices = np.append(indices, F[i, j]) #adds F[i,j] to indices
                counter = np.append(counter, 1) #adds a counter for F[i,j]
    return indices, counter

def create_matrix(indices, counter, F):
    dim = len(indices)
    M = np.empty((dim, dim))

    for i in range(dim):
        M[i, i] = counter[i] #putting values from counter along the diagonal

    #adding symmetric -1s for linear terms from the expansion
    for i in range(np.shape(F)[0]):
        a = F[i, 0]
        b = F[i, 1]

        mask = indices[:] == a
        index_a = np.nonzero(mask)[0]

        mask = indices[:] == b
        index_b = np.nonzero(mask)[0]

        M[index_a, index_b] = -1
        M[index_b, index_a] = -1

    return M

def eval_integral(M):
    eigens = np.linalg.eig(M)[0]
    print(eigens)

    #finding the smallest magnitude eigenvalue--this is to delete the zero eigenvalue, but bc of computer it may not show up as 0
    for i in range(len(eigens)):
        if i == 0:
            small = abs(eigens[i])
        if abs(eigens[i]) < small:
            small = abs(eigens[i])
    
    #deleting the smallest (read: zero) eigenvalue
    mask = eigens[:] == small
    small_index = np.nonzero(mask)[0]
    clean_eigens = np.delete(eigens, small_index)

    #multiplying all other eigenvalues to get determinant
    det = 1
    for i in range(len(clean_eigens)):
        det = det*clean_eigens[i]
    
    integral = (2*np.pi/det)**(3/2) #there's prolly a way to make it return an exact expression instead of a decimal, I'll look at that later

    return integral

def main():
    F = np.array([[1, 2], [1, 3], [1, 4]])
    indices = create_list(F)
    print("indices: ", indices)

    counter = indices[1]
    indices = indices[0]

    M = create_matrix(indices, counter, F)
    print("M:", M)

    integral = eval_integral(M)
    print("integral:", integral)

main()