import re
import sys
import collections

def parse_netlist(filename):

    '''Parse a subset of the netlist format used by SPICE and
    other circuit simulators.

    (V,I,R,N) = parse_netlist(FILENAME) opens the netlist file
    FILENAME and returns several lists of Element objects. V is a list
    of independent voltage sources, I contains independent current
    sources, and R contains passive resistive elements. N is an
    integer indicating the number of (non-ground) nodes in the
    netlist.  Each of the Element objects stored in the V, I, and R
    lists has the following member fields:

      name  - a string naming the element
      src   - the source node for the element (node 0 is always ground)
      dst   - the destination node for the element (node 0 is always ground)
      value - for voltage sources, the voltage in volts
              for current sources, the current in amperes
              for passive resistors, the resistance in ohms.

    The file format is simple. Each line consists of a string name,
    followed by three numbers. If the name starts with V or I, the
    element is assumed to be a voltage or current source,
    respectively. Otherwise, it is assumed to be a passive resistive
    element.  The next three numbers indicate the source, destination,
    and value of the element.  For example, the file

      Vg 1 0 4
      Vx 3 2 6
      R1 1 2 1
      R2 2 0 4
      R3 3 0 2
      It 1 2 1

    would return two voltage sources, one current source, three resistors,
    and a total of N=3 nodes (aside from ground).
    '''

    infile = open(filename,'r')
    line_counter = 1

    V = []
    I = []
    R = []
    n = 0

    Element = collections.namedtuple('Element', ['name', 'src', 'dst', 'value'])

    for line in infile:

        m = re.match(r'(\w+)\s+'\
                     '([0-9]+)\s+'\
                     '([0-9]+)\s+'\
                     '([+-]?[0-9]+(.[0-9]+)?([eE][0-9]+)?)', line)
        if not m:
            raise RuntimeError('parse error at line {0}'.format(line_counter))

        line_counter += 1

        e = Element(m.group(1), int(m.group(2)), int(m.group(3)), float(m.group(4)))

        n = max(n, max(e.src, e.dst))

        if e.name[0].upper() == 'V':
            V.append(e)
        elif e.name[0].upper() == 'I':
            I.append(e)
        else:
            R.append(e)

    return V, I, R, n


# Do some testing
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Please supply a single circuit specification filename as an argument'
        sys.exit(0)

    [V, I, R, n] = parse_netlist(sys.argv[1])

    print 'V =', V
    print 'I =', I
    print 'R =', R
    print 'n =', n
