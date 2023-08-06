#!/usr/bin/env python3
from typing import Set
from pathlib import Path

allowed_prefixes = ["codoc_", "view_", "codocs_"]


def get_all_codoc_files(path: str = None) -> Set[Path]:
    return {f for f in get_all_python_files(path) if is_codoc_file(f)}


def is_codoc_file(f: Path) -> bool:
    return any(f.name.startswith(prefix) for prefix in allowed_prefixes)


def get_all_python_files(path: str = None) -> Set[Path]:
    return {f for f in get_all_files(path) if f.suffix == ".py"}


def get_all_files(path: str = None) -> Set[Path]:
    if path is None:
        path = Path.cwd()
    folders = {Path(path)}
    files = set()
    while folders:
        folder = folders.pop()
        children = {f for f in Path(folder).iterdir()}

        folders |= {f for f in children if f.is_dir()}
        files |= {f for f in children if f.is_file()}
    return files
