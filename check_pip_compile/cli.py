#!/usr/bin/env python

# Core Library modules
import datetime
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Third party modules
import click

# First party modules
import check_pip_compile


@click.version_option(version=check_pip_compile.__version__)
@click.command()
@click.argument(
    "paths", type=click.Path(exists=True, file_okay=True, dir_okay=False), nargs=-1
)
@click.option('-o', '--output-file', required=True)
def entry_point(paths, output_file):
    """Check if pip-compile needs to be run."""
    succeeded = True
    for in_file in paths:
        txt_file: Optional[str] = output_file
        if not txt_file or not os.path.isfile(txt_file):
            txt_file = None
        tmp = check_file(in_file, txt_file)
        succeeded = succeeded and tmp
    if not succeeded:
        sys.exit(-1)

def check_file(in_file: Optional[str], txt_file: Optional[str]) -> bool:
    """Return True, if it's ok."""
    succeeded = True
    if in_file is None:
        print(f"WARNING: {txt_file} has no corresponding in file")
    elif txt_file is None:
        print(f"Run 'pip-compile {in_file}', as no corresponding txt file exists")
        succeeded = False
    else:
        in_age = datetime.datetime.fromtimestamp(os.path.getmtime(in_file))
        txt_age = datetime.datetime.fromtimestamp(os.path.getmtime(txt_file))
        if in_age > txt_age:
            print(
                f"Run 'pip-compile {in_file}' ({in_age}), as {txt_file} ({txt_age}) might be outdated"
            )
            succeeded = False
    return succeeded


def get_corresponding_txt_file(in_file: str, compiled_file: str) -> str:
    if in_file.endswith("setup.py"):
        txt_file = in_file[: -len("setup.py")] + "requirements.txt"
    else:
        txt_file = compiled_file
    return txt_file
