# /usr/bin/env python3
from typing import Set
from codoc.domain.model import Graph, Node, NodeId, Dependency
from codoc.domain.helpers import get_node, get_children
from .types import FilterType


def get_children_of(identifier: str, keep_external_nodes: bool = False) -> FilterType:
    """
    :param identifier: The string identifier of the parent class we want children of
    :param keep_external_nodes: Whether to keep external dependencies of children
    :returns: A filter function that excludes non-children
    :rtype: GraphFilter

    Returns a filter that only returns children of the node given via the identifier.

    The returned filter (function) can then be called with a given graph.

    Example

    .. code-block:: python

       identifier = get_identifier_of_object(myproject.subproject)
       filter_function = get_children_of(identifier)

       filtered_graph = filter_function(graph)



    """
    if not isinstance(identifier, str):
        raise TypeError(f"Identifier has to be a str, was a {type(identifier)}")

    def filter_func(graph: Graph) -> Graph:
        internal_nodes = {
            node for node in graph.nodes if is_node_accepted(node, graph, identifier)
        }
        edges = {
            edge
            for edge in graph.edges
            if is_edge_accepted(edge, internal_nodes, keep_external_nodes)
        }
        if not keep_external_nodes:
            return Graph(nodes=internal_nodes, edges=edges)
        else:
            return Graph(
                nodes={
                    node for node in graph.nodes if is_node_in_edges(node, edges, graph)
                },
                edges=edges,
            )

    return filter_func


# TODO find a way to cache result, i.e dynamic programming
# TODO test these functions individually
def is_node_accepted(node: Node, graph: Graph, allowed_identifier: NodeId) -> bool:
    if node.identifier == allowed_identifier:
        return True

    parent_id = node.parent_identifier
    if not parent_id:
        return False

    parent = get_node(node.parent_identifier, graph)

    return is_node_accepted(parent, graph, allowed_identifier)


def is_edge_accepted(
    edge: Dependency, nodes: Set[Node], keep_external_nodes: bool
) -> bool:
    is_from_node_internal = identifier_in_nodes(edge.from_node, nodes)
    is_to_node_internal = identifier_in_nodes(edge.to_node, nodes)
    if keep_external_nodes:
        return is_from_node_internal or is_to_node_internal
    else:
        return is_from_node_internal and is_to_node_internal


def identifier_in_nodes(identifier: NodeId, nodes: Set[Node]) -> bool:
    return any(identifier == node.identifier for node in nodes)


def is_node_in_edges(node: Node, edges: Set[Dependency], graph: Graph) -> bool:
    is_in_edges = any(
        node.identifier in [edge.from_node, edge.to_node] for edge in edges
    )

    if is_in_edges:
        return True
    # we need to check if a child is here, because then we want to keep the package
    children = get_children(node.identifier, graph)

    if not children:
        return False

    return any(is_node_in_edges(child, edges, graph) for child in children)
