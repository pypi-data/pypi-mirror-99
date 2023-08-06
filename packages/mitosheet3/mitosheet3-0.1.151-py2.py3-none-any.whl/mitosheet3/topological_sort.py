#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains function for running a topological sort on a graph with
the representation {node: set(adj nodes)}. Note that all
nodes must be in the graph, even if they have no adj nodes, and
should just have an empty set in this case.
"""
from copy import deepcopy

from .errors import EditError, make_circular_reference_error


def visit(column_evaluation_graph, node, visited, finished_order, visited_loop):
    """
    Recursive helper function for topological sort. Throws an
    circular_reference_error if there is a loop.
    """
    # Mark the node as visited
    visited[node] = True

    # And record we visited it during this tree of calls to visit
    visited_loop.add(node)

    for adj_node in column_evaluation_graph[node]:
        if not visited[adj_node]:
            visit(column_evaluation_graph, adj_node, visited, finished_order, visited_loop)
        elif adj_node in visited_loop:
            # If we have visited this node in this subtree, there is a loop
            raise make_circular_reference_error()

    # Remove so we can visit again from elsewhere
    visited_loop.remove(node)
    # And mark this node as finished
    finished_order.append(node)


def topological_sort_columns(column_evaluation_graph):
    """
    Topologically sorts by DFSing the graph, recording the finish order, and
    then returning nodes in reversed finish order.
    """
    visited = {node: False for node in column_evaluation_graph}
    finish_order = []
    # Visit each node in the graph
    for node in column_evaluation_graph:
        if not visited[node]:
            # Keep track of the nodes visited during this set
            # of recursive calls, so we can detect cycles
            visited_loop = set()
            visit(
                column_evaluation_graph,
                node,
                visited,
                finish_order,
                visited_loop
            )

    # Reverse finish order for DFS == topological sort
    finish_order.reverse()
    return finish_order

def subgraph_from_starting_column_header(column_evaluation_graph, starting_column_header):
    """
    Filters down the column_evaluation_graph to just the nodes that can be reached
    from the starting_point, including the starting_point itself.

    This results in us transpiling less code, as we only transpile code that changes
    after a given starting column changes.
    """
    column_evaluation_subgraph = dict()

    nodes_in_subgraph = set([starting_column_header])
    while len(nodes_in_subgraph) > 0:
        curr_node = nodes_in_subgraph.pop()
        column_evaluation_subgraph[curr_node] = column_evaluation_graph[curr_node]
        nodes_in_subgraph.update(column_evaluation_subgraph[curr_node])

    return column_evaluation_subgraph


def creates_circularity(
        column_evaluation_graph,
        address,
        old_dependencies,
        new_dependencies
    ):
    """
    Given a column_evaluation_graph, checks if removing the
    old_dependencies and adding the new_dependencies to this address
    will introduce a circular reference; without modifing the
    column_evaluation_graph!

    Returns False if there is not a circular reference, and returns
    True if there is a circular reference.
    """
    # Copy, so we don't modify
    _column_evaluation_graph = deepcopy(column_evaluation_graph)

    for old_dependency in old_dependencies:
        _column_evaluation_graph[old_dependency].remove(address)
    for new_dependency in new_dependencies:
        _column_evaluation_graph[new_dependency].add(address)

    try:
        # Errors if there is no toplogical sort possible
        topological_sort_columns(_column_evaluation_graph)

        return False
    except EditError as e:
        # Reports this error
        return True
    except Exception as e:
        # TODO: handle this case with a general error?
        return True