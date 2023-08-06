#!/usr/bin/env python3
from typing import Optional, Set

from codoc.domain.model import Graph, Node


class ParentNotFoundException(Exception):
    def __init__(self, current_node: Node, graph: Graph):
        super().__init__(
            f"Could not find parent '{current_node.parent_identifier}' of '{current_node}'"
            f"\nAll identifiers: {[n.identifier for n in graph.nodes]}"
        )


class NodeIdentifierNotFoundException(Exception):
    def __init__(self, identifier: str, graph: Graph):
        all_identifiers = [n.identifier for n in graph.nodes]
        msg = f"Could not find identifier '{identifier}'\n {all_identifiers=}"
        super().__init__(msg)


def get_node(identifier: str, graph: Graph) -> Node:
    try:
        return next(node for node in graph.nodes if node.identifier == identifier)
    except StopIteration:
        raise NodeIdentifierNotFoundException(identifier, graph)


def contains_node(identifier: str, graph: Graph) -> bool:
    return any(node.identifier == identifier for node in graph.nodes)


def contains_dependency_between(
    identifier_from: str, identifier_to: str, graph: Graph
) -> bool:
    return any(
        edge.from_node == identifier_from and edge.to_node == identifier_to
        for edge in graph.edges
    )


def has_children(identifier: str, graph: Graph) -> bool:
    return any(node.parent_identifier == identifier for node in graph.nodes)


def get_children(identifier: str, graph: Graph) -> Set[Node]:
    return set(node for node in graph.nodes if node.parent_identifier == identifier)


def get_parent_node(current_node: Node, graph: Graph) -> Optional[Node]:
    if current_node.parent_identifier is None:
        return None
    try:
        return get_node(current_node.parent_identifier, graph)
    except NodeIdentifierNotFoundException:
        raise ParentNotFoundException(current_node, graph)
