"""
solve_netlist.py

Evan Greene and Anthony Lowery
2017/03/18
"""
import numpy as np
from parse_netlist import parse_netlist
from gaussian_elimination import gaussian_elimination

def solve_netlist(V, I, R, N):
    """ transforms the output of parse_netlist into a solved linear system
    using modified nodal analysis. Creates a matrix equation, then solves it
    using Gaussian elimination.
    """

    """
    V represents a list of voltage sources. Each voltage source has a list
    of four elements, name, source, destination, and value (in Volts).

    I represents a list of current sources. The current sources likewise have
    name, source, destination, and value (in Amps).

    R represents a list of resistors, with name, source, destination, and
    value, (in Ohms).

    N is the number of nodes, not including ground
    """
    # create these variables so that we can call Resistor[src] instead of
    # having to remember the order of the information.
    name = 0
    src = 1
    dst = 2
    val = 3

    # set up the values of m and n.
    m = len(V)
    n = N

    """
    The idea here is to create a linear equation given by Ax = z.
    A consists of four submatrices, A = [[G, B], [ C, D]].

    Create the G matrix.
    the G matrix is an n x n matrix where the diagonal elements are the sum
    of the conductances connected to node n, and the off-diagonal elements
    are the negative conductances of the connection between the two nodes.
    """
    G = np.zeros([n, n])

    for resistor in R:
        # print 'G = ', G
        if resistor[src] != 0:
            G[resistor[src] - 1, resistor[src] - 1] += 1.0 / resistor[val]
        if resistor[dst] != 0:
            G[resistor[dst] - 1, resistor[dst] - 1] += 1.0 / resistor[val]
        if resistor[dst] != 0 and resistor[src] != 0:
            G[resistor[src] - 1, resistor[dst] - 1] -= 1.0 / resistor[val]
            G[resistor[dst] - 1, resistor[src] - 1] -= 1.0 / resistor[val]


    """
    Create the B matrix.
    The b matrix is an n x m matrix with only 1, 0 and -1 as elements.

    If the positive terminal of voltage source i is connected to node k, then
    element (k, i) has value 1.

    If the negative element of the voltage source i is connected to node k,
    then element (k, i) has value -1.

    Otherwise, all elements are zero.
    """
    # create an n x n matrix filled with zeros.
    B = np.zeros([n, m])

    for i in range(len(V)): # loop through each voltage source
        if V[i][src] != 0:
            B[V[i][src] - 1, i] = 1.0 # assign the positive terminal to be 1
        if V[i][dst] != 0:
            B[V[i][dst] - 1, i] = -1.0 #assign the negative terminal to be -1

    """
    create the C matrix
    The C matrix is a m x n matrix with only 0, 1 and -1 elements.

    For each independent voltage source, if the positive terminal of the ith
    voltage source is connected to node k, the element, (i, k) is 1.

    If the negative terminal of the ith voltage source is connected to node k,
    then element (i, k) is -1.

    For each op-amp let the positive terminal be at node k and the negative
    terminal be at node j. The corresponding ith row of the C matrix has a
    1 at the positive terminal --location (i, k), and a -1 at the negative
    terminal -- location (j, k)

    Otherwise, the elements of C are zero. """

    # if there are no op amps, then C = B^T.
    C = np.zeros([m, n])

    for i in range(len(V)):
        if V[i][src] != 0:
            C[i-1, V[i][src]- 1] = 1.0 # assign the positive terminal to be 1
        if V[i][dst] != 0:
            C[i-1, V[i][dst] - 1] = -1.0 # assign the negative terminal to be -1
        # we're not looking at Op Amp circuits here, so we're done.

    """
    create the D matrix.

    The D matrix is an m x m matrix composed entirely of zeros.
    """
    D = np.zeros([m, m])

    # print 'G has shape {} \nB has shape {} \nC has shape {} \nD has shape {}'.format(\
    #     G.shape, B.shape, C.shape, D.shape)
    # part1 = np.concatenate((G, B), axis = 1)
    # print 'part1 has shape {}'.format(part1.shape)
    # part2 = np.concatenate((C, D), axis = 1)
    # print 'part2 has shape {}'.format(part2.shape)
    # A = np.concatenate((part1, part2), axis = 0)
    A = np.concatenate((np.concatenate((G, B), axis = 1), \
        np.concatenate((C, D), axis = 1)), axis = 0)

    """
    Now we need to develop the Z matrix.
    The Z matrix is developed as the combination of two smaller matrices i and e

    The i matrix is a 1 x n
    """

    eye = np.zeros(n)
    # can't very well use i (reserved for loops) or I (already used for current)
    for index in range(len(I)): # using i might get confusing.
        if I[index][dst] != 0:
            eye[I[index][dst] - 1] += I[index][val]
        if I[index][src] != 0:
            eye[I[index][src] - 1] -= I[index][val]


    """
    The e matrix is a 1 x m matrix with each element corresponding to a
    voltage source. If the element in the e matrix corresponds to an independent
    voltage source, it is set equal to the value of that voltage source.
    If the element corresponds to an op-amp, it is set to zero.
    """
    e = np.zeros(m)
    for index in range(len(V)):
        if V[index][src] != 0:
            e[index - 1] = V[index][val]

    # print 'i has shape {} \ne has shape {} \n'.format(eye.shape, e.shape)
    Z = np.concatenate((eye, e), axis = 0 )

    """
    The x matrix (found from Ax = Z) consists of two submatrices v and j.

    The v matrix is an n x 1 matrix of node voltages. Each element in v[i]
    corresponds to the equivalent node i+1 (there is no entry for ground, i = 0)

    The j matrix is an m x 1 matrix of currents, with one entry for the current
    through each voltage source.
    """

    return A, Z, gaussian_elimination(A, Z)

def main():
    V, I, R, n = parse_netlist('example2.txt')
    A, z, x = solve_netlist(V, I, R, n)

    for index in range(n):
        print 'The voltage at node {} is {} V'.format(index + 1, x[index])
    for index in range(len(V)):
        print 'The current through voltage source {} is {} A'.format(V[index][0], x[index + n])


if __name__ == '__main__':
    main()
