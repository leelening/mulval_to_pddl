import pandas
from common import *
import sys


if __name__ == '__main__':

    lines = list()
    lines.append('(define(domain attack_graph)\n')
    lines.append('    (:requirements :strips)\n\n')

    vertices_file = sys.argv[1]
    arcs_file = sys.argv[2]

    vertices = pandas.read_csv(vertices_file, header=None)
    arcs = pandas.read_csv(arcs_file, header=None)
    arcs = arcs.iloc[:, 0:2].values.tolist()
    arcs = list(tuple(x) for x in arcs)

    classified_vertices = {'AND': set(), 'OR': set(), 'LEAF': set()}

    # classify the nodes
    for v in vertices.values:
        type = v[2]
        classified_vertices[type].add(tuple(v))

    # dict.fromkeys de-duplicates while preserving VERTICES.CSV order, so the
    # generated file is byte-stable across runs (a set is not).
    predicates = list(dict.fromkeys('(' + format_string(v[1]) + ' ?x)\n'
                                    for v in vertices.values if v[2] == 'OR' or v[2] == 'LEAF'))

    lines.append('(:predicates\n')
    lines.append(' '.join(predicates) + '\n')
    lines.append(')\n\n')

    # collection all actions
    actions = dict()
    for v in classified_vertices['AND']:
        actions[v] = dict()
        index = v[0]
        actions[v]['pre'] = predecessor(index, arcs, vertices)
        actions[v]['post'] = successor(index, arcs, vertices)

    for a in sorted(actions, key=lambda v: v[0]):
        lines.append('(:action ' + format_string(str((a[1] +'_' + str(a[0])))) + '\n')
        lines.append(':parameters (?' + 'x' + ')\n')
        lines.append(':precondition (and\n')
        lines.append(actions[a]['pre'] + ')\n')
        lines.append(':effect (and\n')
        lines.append(actions[a]['post'] + ')\n')
        lines.append(')\n\n')

    lines.append(')\n')

    with open("domain.pddl", 'w+') as f:
        f.writelines(lines)
