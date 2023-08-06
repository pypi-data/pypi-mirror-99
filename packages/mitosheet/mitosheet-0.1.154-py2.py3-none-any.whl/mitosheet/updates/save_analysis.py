#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Saves the analysis with the passed name.
"""

from mitosheet.save_utils import write_analysis

SAVE_ANALYSIS_UPDATE_EVENT = 'save_analysis_update'
SAVE_ANALYSIS_UPDATE_PARAMS = ['analysis_name']

def execute_save_analysis_update(
        wsc,
        analysis_name
    ):
    """
    Saves the analysis with the passed name
    """
    write_analysis(wsc, analysis_name)


SAVE_ANALYSIS_UPDATE = {
    'event_type': SAVE_ANALYSIS_UPDATE_EVENT,
    'params': SAVE_ANALYSIS_UPDATE_PARAMS,
    'execute': execute_save_analysis_update
}