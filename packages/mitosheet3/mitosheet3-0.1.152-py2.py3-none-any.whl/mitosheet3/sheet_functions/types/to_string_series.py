#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
For going to a string series.
"""

from typing import Tuple, Union
import pandas as pd
import numpy as np

from mitosheet.sheet_functions.types.utils import get_mito_type


def to_string_series(
        unknown_object,
        on_uncastable_arg_element=('default', np.NaN), #Union[Literal['error'], Tuple[Literal['default'], any]]
    ):
    """
    Converts the given object to a string series. Note that on_uncastable_arg_element
    is irrelevant here, as anything can be turned into a string!
    """
    from_type = get_mito_type(unknown_object)

    # If it is not a series, we put it in a series, and get the type again
    if not from_type.endswith('series'):
        return pd.Series([str(unknown_object)], dtype='str')

    if from_type == 'boolean_series':
        return unknown_object.astype('str')
    elif from_type == 'datetime_series':
        return unknown_object.dt.strftime('%Y-%m-%d %X')
    elif from_type == 'number_series':
        return unknown_object.astype('str')
    elif from_type == 'string_series':
        # We need to cast here, because object series are treated
        # as string series, and may contain other types
        return unknown_object.astype('str')
    else:
        return None