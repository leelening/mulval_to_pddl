from common import *
import pandas
import sys

if __name__ == '__main__':
    lines = list()
    lines.append('(define(problem pb1)\n')
    lines.append('  (:domain attack_graph)\n')
    lines.append('(:objects s)\n\n')

    vertices_file = sys.argv[1]

    vertices = pandas.read_csv(vertices_file, header=None)
    classified_vertices = {'AND': set(), 'OR': set(), 'LEAF': set()}

    # classify the nodes
    for v in vertices.values:
        type = v[2]
        classified_vertices[type].add(tuple(v))

    temp = str()
    for v in sorted(classified_vertices['LEAF'], key=lambda v: v[0]):
        temp += '(' + format_string(v[1]) + ' s)\n'

    lines.append('(:init\n')
    lines.append(temp)
    lines.append('\n)\n\n')

    # in order to have all the transitions, we need all OR nodes to be true
    lines.append('(:goal (and\n')
    temp = str()
    for v in sorted(classified_vertices['OR'], key=lambda v: v[0]):
        temp += '(' + format_string(v[1]) + ' s)\n'
    lines.append(temp)
    lines.append(')\n')
    lines.append(')\n\n')

    lines.append(')\n')

    with open("problem.pddl", 'w+') as f:
        f.writelines(lines)
