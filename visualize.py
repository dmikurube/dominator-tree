#!/usr/bin/env python

import json
import sys

from collections import OrderedDict  # pylint: disable=E0611,W0611


NODE_TYPE = 0
NODE_NAME = 1
NODE_ID = 2
NODE_SELF_SIZE = 3
NODE_EDGE_COUNT = 4
NODE_FIELDS_COUNT = 5

EDGE_TYPE = 0
EDGE_NAME = 1
EDGE_TO_NODE = 2
EDGE_FIELDS_COUNT = 3


def main(argv):
  if len(argv) < 2:
    return 1

  with open(sys.argv[1], 'r') as f:
    heapsnapshot = json.load(f, object_pairs_hook=OrderedDict)
  heapsnapshot_name = sys.argv[1].partition('.')[0]

  snapshot_nodes = heapsnapshot['nodes']
  snapshot_edges = heapsnapshot['edges']
  edges = []

  snapshot_edge_cursor = 0
  for i in range(0, len(snapshot_nodes) / NODE_FIELDS_COUNT):
    for j in range(snapshot_nodes[(i * NODE_FIELDS_COUNT) + NODE_EDGE_COUNT]):
      edges.append((i,
                    snapshot_edges[snapshot_edge_cursor *
                                   EDGE_FIELDS_COUNT +
                                   EDGE_TO_NODE] / NODE_FIELDS_COUNT))
      snapshot_edge_cursor += 1

  with open(heapsnapshot_name + '.dot', 'w') as f:
    print >> f, 'digraph %s{' % heapsnapshot_name
    for edge in edges:
      print >> f, '    %d -> %d;' % edge
    print >> f, '}'


  # g = pydot.graph_from_edges(edges, directed=1)
  # g.write_jpeg('graph_from_edges_dot.jpg', prog='sfdp')
  # g.write_dot('sample.dot')

  # Use sfdp instead of dot for large graphs:
  # sfdp -x -Tpng data.dot > data.png
  # http://stackoverflow.com/questions/238724/visualizing-undirected-graph-thats-too-large-for-graphviz
  # http://stackoverflow.com/questions/13417411/laying-out-a-large-graph-with-graphviz

  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv))
