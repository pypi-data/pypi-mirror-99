#!/usr/bin/env python3
import codoc.domain.model
from codoc.service import filters
from codoc.service.export.codoc_view import view
from codoc.service.parsing.node import get_identifier_of_object


@view(
    label="Domain Model",
)
def view_domain_model(graph):
    """
    This view presents the basic domain model of the
    [Codoc](https://codoc.org/) system.

    It shows the core models.

    To actually utilize the classes, look at the service layer.
    """
    graph = filters.get_children_of(
        get_identifier_of_object(codoc.domain.model), keep_external_nodes=False
    )(graph)

    return filters.class_diagram_filter(graph)
