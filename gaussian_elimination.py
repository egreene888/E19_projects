import numpy as np

""" Solves linear systems of the form Ax = b using Gaussian elimination """ 

######################################################################
# Perform forward elimination step of Gaussian elimination

def forward_elimination(A,b):
    m,n = A.shape
    assert(m == n)
    # A, b = pivot(A, b)
    # For each diagonal element i
    for i in range(n):
        # print A
        A, b = pivot(A, b)
        # A[i,i] is our "pivot" element, which will appear in a quotient below.
        # it had better not be zero.
        assert( A[i,i] != 0 )
        # For each subsequent row j
        for j in range(i+1, n):

            # Perform the operation row_j = row_j - A[j,i] / A[i,i] * row_i
            factor = A[j,i] / A[i,i]

            # For each column k
            for k in range(n):
                # Note the range above could be range(i,n) but we want
                # to force getting zeros in A for clarity.
                A[j,k] -= factor * A[i,k]

            # Perform the operation b_j = b_j - A[j,i] / A[i,i] * b_i
            b[j] -= factor * b[i]

#####################################################################
# A function for the pivoting step of gaussian elimination
def pivot(A, b):
    # move the rows around so that there are no zeros on the diagonal
    m, n = A.shape
    for i in range(m):
        # find the largest number in the column.
        large_i = i
        for j in range(i, m):
            if abs(A[j, i]) > abs(A[large_i, i]):
                large_i = j
        # print large_i
        # swap rows i and large_i if i != large_i
        if i != large_i:
            swapa = np.copy(A[large_i, :])
            A[large_i, :] = A[i, :]
            A[i, :] = swapa
            # A[large_i, :], A[i, :] = A[i, :], A[large_i, :] <-- doesn't work
            swapb = np.copy(b[large_i])
            b[large_i] = b[i]
            b[i] = swapb
            # b[large_i], b[i] = b[i], b[large_i]
    return A, b

######################################################################
# Perform back substitution step of Gaussian elimination

def back_substitution(A,b):

    m,n = A.shape
    assert(m == n)

    x = np.empty_like(b)

    # For each row i from n-1 to 0
    for i in reversed(range(n)):

        total = b[i]

        # For each column greater than i
        for j in range(i+1,n):
            total -= A[i,j]*x[j]

        assert(A[i,i] != 0)

        x[i] = total / A[i,i]

    return x

######################################################################

def gaussian_elimination(A, b):

    AA = A.copy()
    bb = b.copy()

    forward_elimination(AA, bb)
    # print AA
    # print bb
    return back_substitution(AA, bb)

######################################################################
def main():
    """
    A = np.matrix( [[   0,  3,  2,  1],
                    [   4,  0,  7,  5],
                    [   8,  2,  0,  2],
                    [   0,  1,  2,  0]], dtype = 'float')

    b = np.matrix([-3, 2, -2, -5], dtype = 'float').transpose()

    x = gaussian_elimination(A, b)
    """
    A = np.matrix(  [[  0,  2,  6,  1,  2],
                    [   2,  0,  3,  2,  4],
                    [   9,  5,  0,  3,  5],
                    [   4,  8,  4,  0,  8],
                    [   1,  0,  0,  4,  0]], dtype = 'float')
    b = np.matrix(  [7, -13,    7,  -4, -8], dtype = 'float').transpose()
    x = gaussian_elimination(A, b)

    print 'A=\n', A
    print
    print 'b=', b.transpose()
    print 'x=', x.transpose()
    print  'right answer = ', (np.linalg.inv(A) * b).transpose()
    print 'residual:', np.linalg.norm(A*x - b)**2

if __name__ == '__main__':
    main()
