#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
For going to a datetime series.
"""

from typing import Tuple, Union
import pandas as pd
import numpy as np

from mitosheet.sheet_functions.types.utils import get_mito_type

def to_datetime_series(
        unknown_object,
        on_uncastable_arg_element=('default', np.NaN), # Union[Literal['error'], Tuple[Literal['default'], any]]
    ):
    """
    Converts the given object to a datetime series.
    """
    from_type = get_mito_type(unknown_object)

    # If it is not a series, we put it in a series, and get the type again
    if not from_type.endswith('series'):
        unknown_object = pd.Series([unknown_object])
        from_type = get_mito_type(unknown_object)

    if from_type == 'boolean_series':
        return None
    elif from_type == 'datetime_series':
        return unknown_object
    if from_type == 'number_series':
        return None
    elif from_type == 'string_series':
        # TODO: improve this to work element wise!
        return pd.to_datetime(unknown_object)
    else:
        return None