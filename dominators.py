#!/usr/bin/env python

# LCA (least common ancestors):
# http://www.ics.uci.edu/~eppstein/PADS/LCA.py

# Union-find:
# http://www.ics.uci.edu/~eppstein/PADS/UnionFind.py


import json
import sys

from LCA import LCA
from UnionFind import UnionFind

from collections import OrderedDict  # pylint: disable=E0611,W0611


def is_reachable(node, root, edges, parents, reachable, stack):
  if reachable[node]:
    return True

  height = 0
  stack[height] = node

  while parents[stack[height]] != root:
    parent = parents[stack[height]]
    height += 1
    stack[height] = parent

  while height >= 0:
    reachable[stack[height]] = True
    height -= 1

  return True


def verify_spanning_tree(root, edges, parents, postorder):
  reachable = [ False ] * (len(parents) + 1)
  working_stack = [ -1 ] * (len(parents) + 1)

  for node in range(len(parents) + 1):  # Iterate all nodes.
    if node == root:
      print "Root: %d" % root
      continue
    is_reachable(node, root, edges, parents, reachable, working_stack)
  print "All nodes are reachable to the root."

  edge_table = [ set() ] * (len(parents) + 1)
  for edge in edges:
    edge_table[edge[0]].add(edge[1])
  for node, parent in parents.iteritems():
    if node not in edge_table[parent]:
      raise "A tree edge (%d, %d) is not included in the original graph."
  print "All tree edges are included in the original graph."

  visited_count = 0
  visited = [ False ] * (len(parents) + 1)
  for node_postorder in range(len(parents) + 1):  # Iterate all nodes.
    node_ordinal = postorder[node_postorder]
    if node_ordinal == root:
      if visited_count != len(parents):
        raise "Not ordered in post-order: root is not at last."
      break  # check count
    visited[node_ordinal] = True
    visited_count += 1
    if visited[parents[node_ordinal]]:
      raise "Not ordered in post-order."
  print "Ordered in post-order."

  return True


def prepare_GD2(root, edges, parents, lca):
  total = [ 0 ] * (len(parents) + 1)
  arcs = [ [] ] * (len(parents) + 1)
  for edge in edges:
    total[edge[1]] += 1
    arcs[lca(edge[0], edge[1])].append((edge[0], edge[1]))
  return total, arcs


def GD2(root, edges, parents, postorder, total, arcs):
  for node_postorder in range(len(parents) + 1):  # Iterate all nodes.
    node = postorder[node_postorder]
    pass


def main(argv):
  with open('edges.json', 'r') as edges_f:
    edges = json.load(edges_f, object_pairs_hook=OrderedDict)['edges']
  with open('postorder.json', 'r') as postorder_f:
    raw_postorder = json.load(postorder_f, object_pairs_hook=OrderedDict)
    postorder = {}
    for post, ordinal in raw_postorder.iteritems():
      postorder[int(post)] = ordinal
  with open('parents.json', 'r') as parents_f:
    raw_parents = json.load(parents_f, object_pairs_hook=OrderedDict)
    roots = []
    parents = {}
    for src, dst in raw_parents.iteritems():
      src = int(src)
      if src == dst:
        roots.append(src)
        continue
      parents[src] = dst
    if len(roots) > 1:
      raise "Multiple roots."

  verify_spanning_tree(roots[0], edges, parents, postorder)
  lca = LCA(parents)

  total, arcs = prepare_GD2(roots[0], edges, parents, lca)

  dominators = GD2(root, edges, parents, postorder, total, arcs)

  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv))
