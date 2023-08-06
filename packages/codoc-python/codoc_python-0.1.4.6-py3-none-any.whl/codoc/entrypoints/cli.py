#!/usr/bin/env python3
"""
The Command Line Interface for
the Codoc SDK.


Mainly used to publish your views to the webapp.
"""
import sys
import os
import fire

from codoc.service.finder.files import (
    get_all_codoc_files,
)

from codoc.service.finder.config import get_config

from codoc.service.finder.views import get_views_in_file, get_views_in_folder

NO_API_ERROR = """
API Key is not supplied.
Please set 'CODOC_API_KEY' as an environmental variable

Alternatively consult the documentation at https://codoc.org
"""


class CliHandler:
    """
    The Command Line Interface for
    the Codoc SDK.


    Mainly used to publish your views to the webapp.
    """

    def __init__(self, path="codoc_views"):
        self._path = path

    def publish(self):
        """
        Publish all graphs in the current package
        """

        sys.path.append(os.getcwd())
        try:
            config = get_config(self._path)
        except Exception as e:
            return f"Could not load config ({e})"

        try:
            graph = config.bootstrap()
        except Exception as e:
            return f"config could not run bootstrap ({e})"

        api_key = os.getenv("CODOC_API_KEY")
        if not api_key:
            return NO_API_ERROR

        files = get_all_codoc_files(self._path)
        views = [view for f in files for view in get_views_in_file(f)]
        resp = []
        for view in views:
            resp.append(f"Publishing {view.label}...")
            pk = view(graph=graph, api_key=api_key)
            url = get_url_for_graph(pk)
            resp.append(f"published at {url}")

        return "\n".join(resp)

    def list_views(self):
        """
        returns a list of all the views found.
        """
        views = get_views_in_folder(self._path)
        if not views:
            return "No views found"
        sep = " - "
        return sep + ("\n" + sep).join(v.__name__ for v in views)

    def list_files(self):
        """
        returns a list of all the codoc related files found.
        """
        files = get_all_codoc_files(self._path)
        if not files:
            return "No files found"
        sep = " - "
        return sep + ("\n" + sep).join(f.name for f in files)


def get_url_for_graph(pk: int) -> str:
    return f"https://codoc.org/app/graph/{pk}"


def _main():
    fire.Fire(CliHandler)


if __name__ == "__main__":
    _main()
