#!/usr/bin/env python3

from codoc.service.parsing.node import get_description, get_identifier_of_object
from codoc.service import filters
from codoc.service.export.codoc_view import view

import codoc.service


@view(
    label="Parsing in Codoc Python",
    description="""
This graph showcases the inter dependencies of the parsing,
as well as the direct dependencies of
the internal aspects.
\n\n
"""
    + get_description(codoc.service),
)
def view_parsing(graph):
    return filters.exclude_modules(
        filters.get_children_of(get_identifier_of_object(codoc.service.parsing))(graph)
    )


@view(
    label="Graph Generation in Codoc Python",
)
def view_graph_rendering(graph):
    """
    This graph showcases the inter dependencies of the graph,
    as well as the direct dependencies of
    the internal aspects.
    \n\n
    """
    return filters.exclude_modules(
        filters.get_children_of(
            get_identifier_of_object(codoc.service.graph), keep_external_nodes=True
        )(graph)
    )
