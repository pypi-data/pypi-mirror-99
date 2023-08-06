#!/usr/bin/env python3
from codoc.service import filters
from codoc.service.export.codoc_view import view


@view(
    label="Module View of the Codoc SDK",
)
def view_modules(graph):
    """
    This view contains all the modules that our system contain.
    """
    return filters.exclude_functions(filters.exclude_classes(graph))
