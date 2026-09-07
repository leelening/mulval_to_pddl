import re


def find_predicate(vertices, index):
    # Look the vertex up by its id (column 0) rather than by row position:
    # MulVAL ids are not guaranteed to be contiguous or sorted.
    matches = vertices.values[vertices.values[:, 0] == index]
    if len(matches) == 0:
        raise KeyError('No vertex with id %r in VERTICES.CSV' % (index,))
    if len(matches) > 1:
        raise KeyError('Duplicate vertex id %r in VERTICES.CSV' % (index,))

    return format_string(matches[0, 1])


def format_string(string):
    string = string.replace(' ', '_')
    string = string.replace('(', '_')
    string = string.replace(')', '_')
    string = string.replace('-', '_')
    string = string.replace('\'', '_')
    string = string.replace(',', '_')
    string = string.replace('.', '_')
    string = re.sub('_+', '_', string)
    string = string.rstrip('_')
    string = string.lower()
    return string


def predecessor(index, arcs, vertices):
    predecessors = str()
    for (source, target) in arcs:
        if source == index:
            predecessors += ' (' + format_string(find_predicate(vertices, target)) + ' ?x)\n'
    return predecessors


def successor(index, arcs, vertices):
    successors = str()
    for (source, target) in arcs:
        if target == index:
            successors += ' (' + format_string(find_predicate(vertices, source)) + ' ?x)\n'
    return successors
