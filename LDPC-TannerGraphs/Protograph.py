
import Utils
from TannerGraph import *


'''
This TannerGraph subclass constructs the tanner_graph dictionary as a dictionary of lists of ProtographEntry objects.
This allows each entry to have an entry value not necessarily equal to 1.

Protographs can be read from predefined files in the following mode:
Entries are considered non-zero positions in the Protograph's matrix representation
each entry is listed in the file as follows:
row in matrix, column in matrix, value in matrix
    integers are all single-space separated
'''

class Protograph(TannerGraph):

    # parameters:
    #   args:
    #     - list(list()), a list of entries where each entry is a list of length three. These entry lists contain
    #       their row value at position 0, column value at position 1, and value at position 2
    #     - list(string) where the contained string is the filepath of the predefined protograph
    # return:
    #   a fully constructed Protograph object
    def __init__(self, args):
        TannerGraph.__init__(self, args)

        if len(args) == 1:
            array = read_protograph_array_from_file(args[0])
        else:
            array = args


        self.tanner_graph = Protograph.create_tanner_graph_for_protograph(array)

        self.height = len(self.tanner_graph)
        self.width = self.get_width()

    # return:
    #   the width of a protograph tanner_graph (the superclass get_width does not work here as entry values should no longer by inferred)
    def get_width(self):
        max = 0
        for row in self.tanner_graph:
            for entry in self.getRow(row):
                if entry.index > max:
                    max = entry.index
        return max + 1

    '''
    Constructs a protograph object from the supplied point list
    '''

    # parameters:
    #   points: list, the list of points defining the protograph
    # return:
    #   the tanner_graph which represents the Protograph object
    @staticmethod
    def create_tanner_graph_for_protograph(points):

        protograph = TannerGraph(None)

        num_rows = 0
        for entry in points:
            if entry[0] + 1 > num_rows:
                num_rows = entry[0] + 1

        for row in range(num_rows):
            protograph.addRow()

        for entry in points:
            protograph.getRow(entry[0]).append(ProtographEntry(entry[1], entry[2]))

        return protograph.tanner_graph



    '''
    This method allows the protograph to be queried as if was defined by a matrix structure. This is necessary here and
    not in TannerGraph as Protographs are the only TannerGraphs who's values can be greater than 1.
    '''

    # parameters:
    #   r: int, row index of fetched entry
    #   c: int, col index of fetched entry
    # return:
    #   the value of the entry at location [r, c] in self.tanner_graph
    def get(self, r, c):
        row = self.getRow(r)
        for entry in row:
            if entry.index == c:
                return entry.value
        return 0

    # parameters:
    #   row: int, row of the protograph to analyze
    # return:
    #   max_index: int, maximum index value of all ProtographEntries contained in the row
    def get_max_index(self, row):
        row = self.tanner_graph[row]
        max_index = 0
        for i in range(len(row)):
            if row[i].index > max_index:
                max_index = row[i].index
        return max_index

    # parameters:
    #   index: int, index to be queried
    #   row: int, index in graph of row to be queried
    # return:
    #   boolean: does index exist in row
    def contains_index(self, index, row):
        pulled = self.tanner_graph[row]
        for e in pulled:
            if e.index == index:
                return True
        return False


    def as_matrix(self):
        return get_matrix_representation(self)


'''
Because the superclass as_matrix method cannot work with ProtographEntry objects, Protograph.py must redefine
the construction of its matrix form.
'''

# parameters:
#   protograph: Protograph, the protograph to generate a matrix of
# return:
#   list(list()) representing the protograph code's matrix form
def get_matrix_representation(protograph):
    matrix = []
    for i in range(protograph.height):
        row = []
        if i in protograph.tanner_graph:
            for j in range(protograph.get_max_index(i) + 1):
                if protograph.contains_index(j, i):
                    row.append(protograph.get(i, j))
                else:
                    row.append(0)
        matrix.append(row)
    normalize(matrix)
    return matrix

def write_protograph_to_file(protograph, filepath):
    return None

# parameters:
#   filepath: String, filepath which contains predefined protograph
# return:
#   array: when fed into the protograph constructor a Protograph object is created
def read_protograph_array_from_file(filepath):

    protograph_array = []

    f = open(filepath, 'r')
    entries = [l.rstrip('\n') for l in f.readlines()]
    for entry in entries:
        protograph_array.append([int(i) for i in entry.split(' ')])

    return protograph_array


'''
This class represents a protograph entry; it allows for entry values to be greater than 1
'''


class ProtographEntry:

    def __init__(self, index, value):
        self.value = value
        self.index = index
