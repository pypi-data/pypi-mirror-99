#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
The Mito package, which contains functions for creating a Mito sheet. 

To generate a new sheet, simply run:

import mitosheet
mitosheet.sheet()

If running mitosheet.sheet() just prints text that looks like `MitoWidget(...`, then you need to 
install the JupyterLab extension manager by running:

jupyter labextension install @jupyter-widgets/jupyterlab-manager@2;

Run this command in the terminal where you installed Mito. It should take 5-10 minutes to complete.

Then, restart your JupyterLab instance, and refresh your browser. Mito should now render.

NOTE: if you have any issues with installation, please email book a demo time at https://hubs.ly/H0FL1920
"""

import os
import pandas as pd
import json
from pathlib import Path

from ._version import __version__

from mitosheet3.example import MitoWidget, sheet
from mitosheet3.errors import CreationError, EditError
from mitosheet3._version import __version__

# Export all the sheet functions
from mitosheet3.sheet_functions import *
# And the functions for changing types
from mitosheet3.sheet_functions.types import *

from .nbextension import _jupyter_nbextension_paths


if __name__ == 'mitosheet':
    from mitosheet3.user.user import initialize_user
    # Make sure the user is created and up to date, whenever mitosheet is imported
    initialize_user()

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]

