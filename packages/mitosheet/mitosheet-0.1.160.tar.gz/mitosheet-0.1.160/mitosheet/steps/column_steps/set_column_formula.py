#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A set_column_formula step, which allows you to set the formula
of a given column in the sheet (and then recalculates this column)
and it's dependents.
"""
from mitosheet.topological_sort import creates_circularity, subgraph_from_starting_column_header, topological_sort_columns
from mitosheet.sheet_functions import FUNCTIONS
from mitosheet.parser import parse_formula
from mitosheet.utils import create_new_step, get_column_filter_type

from mitosheet.errors import (
    make_circular_reference_error, 
    make_no_column_error, 
    make_operator_type_error, 
    make_unsupported_function_error, 
    make_wrong_column_metatype_error
)

SET_COLUMN_FORMULA_DISPLAY_NAME = 'Set Column Formula'

SET_COLUMN_FORMULA_EVENT = 'set_column_formula_edit'
SET_COLUMN_FORMULA_STEP_TYPE = 'set_column_formula'

SET_COLUMN_FORMULA_PARAMS = [
    'sheet_index', # int
    'column_header', # the new column to create
    'old_formula', # the previous formula, or None (if there is None)
    'new_formula', # the new formula for the column
]


def _update_column_formula_in_step(
        step,
        sheet_index,
        column_header,
        old_formula,
        new_formula
    ):
    """
    A  helper function for updating the formula of a column. It assumes
    that the passed information is all _correct_ and will not:
    1. Introduce a circular reference error.
    2. Add an invalid formula.

    It DOES NOT "reexecute" the dataframes, just updates the state variables.
    """

    new_python_code, _, new_dependencies = parse_formula(
        new_formula, 
        column_header
    )

    _, _, old_dependencies = parse_formula(
        old_formula, 
        column_header
    )

    step['column_spreadsheet_code'][sheet_index][column_header] = new_formula
    step['column_python_code'][sheet_index][column_header] = new_python_code

    # Update the column dependency graph
    for old_dependency in old_dependencies:
        step['column_evaluation_graph'][sheet_index][old_dependency].remove(column_header)
    for new_dependency in new_dependencies:
        step['column_evaluation_graph'][sheet_index][new_dependency].add(column_header)


def saturate_set_column_formula_step(
        curr_step,
        event
    ):
    """
    Adds the old formula to the edit event.
    """
    sheet_index = event['sheet_index']
    column_header = event['column_header']
    event['old_formula'] = curr_step['column_spreadsheet_code'][sheet_index][column_header]

def execute_set_column_formula_step(
        curr_step,
        sheet_index,
        column_header,
        old_formula,
        new_formula
    ):
    """
    Sets the column with column_header to have the new_formula, and 
    updates the dataframe as a result.

    Errors if:
    - The given column_header is not a column. 
    - The new_formula introduces a circular reference.
    - The new_formula causes an execution error in any way. 

    In the case of an error, this function rolls back all variables
    variables to their state at the start of this function.
    """
    if column_header not in curr_step['column_metatype'][sheet_index]:
        raise make_no_column_error([column_header])

    # First, we check the column_metatype, and make sure it's a formula
    if curr_step['column_metatype'][sheet_index][column_header] != 'formula':
        raise make_wrong_column_metatype_error(column_header)

    # If nothings changed, there's no work to do
    if (old_formula == new_formula):
        return

    # Then we try and parse the formula
    new_python_code, new_functions, new_dependencies = parse_formula(
        new_formula, 
        column_header
    )
    
    # We check that the formula doesn't reference any columns that don't exist
    missing_columns = new_dependencies.difference(curr_step['column_metatype'][sheet_index].keys())
    if any(missing_columns):
        raise make_no_column_error(missing_columns)

    # The formula can only reference known formulas
    missing_functions = new_functions.difference(set(FUNCTIONS.keys()))
    if any(missing_functions):
        raise make_unsupported_function_error(missing_functions)

    # Then, we get the list of old column dependencies and new dependencies
    # so that we can update the graph
    old_python_code, old_functions, old_dependencies = parse_formula(old_formula, column_header)

    # Before changing any variables, we make sure this edit didn't
    # introduct any circularity
    circularity = creates_circularity(
        curr_step['column_evaluation_graph'][sheet_index], 
        column_header,
        old_dependencies,
        new_dependencies
    )
    if circularity:
        raise make_circular_reference_error()

    # We check out a new step
    new_step = create_new_step(curr_step, SET_COLUMN_FORMULA_STEP_TYPE)

    # Update the column formula, and then execute the new formula graph
    _update_column_formula_in_step(new_step, sheet_index, column_header, old_formula, new_formula)
    _execute(new_step, new_step['dfs'][sheet_index], sheet_index)

    # Finially, update the type of the filters of this column, for all the filters
    # TODO: fix bug where we have to update downstream filter types, but note that
    # it would just be really nice if we didn't have to store the type here, and could
    # just get it dynamically...
    new_type = get_column_filter_type(new_step['dfs'][sheet_index][column_header])
    new_step['column_type'][sheet_index][column_header] = new_type
    new_step['column_filters'][sheet_index][column_header]['filters'] = [
        {'type': new_type, 'condition': filter_['condition'], 'value': filter_['value']} 
        for filter_ in new_step['column_filters'][sheet_index][column_header]['filters']
    ]

    return new_step

def get_details_from_operator_type_error(error):
    """
    We detect operator errors by checking the error string, which has the format:

    If you write 1 + 'true'
    - unsupported operand type(s) for /: 'int' and 'str' 

    If you write 1 + pd.Series(['true'])
    - can only concatenate str (not "int") to str

    If you write 10 ^ pd.Series(['true'])
    - Cannot perform 'rxor' with a dtyped [object] array and scalar of type [bool]
    If you write pd.Series(['true']) ^ 10
    - Cannot perform 'xor' with a dtyped [object] array and scalar of type [bool]

    ^ NOTE: the above two errors makes pretty much no sense at all, but it appears
    to be casting the number to a boolean? So we choose to handle this as a number,
    as this is when you would be 

    Returns None if the passed error is not an operator type error. Otherwise, returns
    a triple of (operator, first argument type, second argument type).
    """
    error_message = str(error)
    # Handle case where standard python primitive types are used incorrectly
    if error_message.startswith('unsupported operand type'):
        # Then, we get the specific operator by checking right before the :
        operator = error_message.split(':')[0].split(' ')[-1].strip()
        # And we get the specific types - see above format for how this parsing works!
        arg_one_type = error_message.split(':')[-1].split('\'')[1]
        arg_two_type = error_message.split(':')[-1].split('\'')[-2]
        return (operator, arg_one_type, arg_two_type)
    # Handle case where pandas dataframes are part of the operator, for a concatenate
    if error_message.startswith('can only concatenate str'):
        # We cannot tell the ordered here (e.g. we don't know if a string was concated
        # to an integer, or the other way around) b/c the error doesn't say so, so we just
        # do our best 
        other_type = error_message.split('"')[1]
        return ('+', 'str', other_type)
    # Handle a ^
    if error_message.startswith('Cannot perform \'rxor\' with a dtyped') or error_message.startswith('Cannot perform \'xor\' with a dtyped'):
        # This error message might be totally wrong, but there is some weird
        # casting that goes on in the error message that makes it hard to tell. As such,
        # we report the most likely error.
        return ('^', 'number', 'str')


    return None


def _execute(step, df, sheet_index):
    """
    Executes the given state variables for  
    """

    topological_sort = topological_sort_columns(step['column_evaluation_graph'][sheet_index])

    for column_header in topological_sort:
        # Exec the code, where the df is the original dataframe
        # See explination here: https://www.tutorialspoint.com/exec-in-python
        try:
            exec(
                step['column_python_code'][sheet_index][column_header],
                {'df': df}, 
                FUNCTIONS
            )
        except TypeError as e:
            # We catch TypeErrors specificially, so that we can case on operator errors, to 
            # give better error messages
            operator_type_error_details = get_details_from_operator_type_error(e)
            if operator_type_error_details is not None:
                # If there is an operator error, we handle it specially, to give the user
                # more information about how to recover
                raise make_operator_type_error(*operator_type_error_details)
            else:
                # If it's not an operator error, we just propagate the error up
                raise e



def transpile_set_column_formula_step(
        step,
        sheet_index,
        column_header,
        old_formula, # NOTE: the change_column_type formula relies on this not being used in the transpile step
        new_formula # same as above
    ):
    """
    Transpiles an set_column_formula step to python code!
    """
    code = []

    # We only look at the sheet that was changed, and sort the columns, taking only
    # those downstream from the changed columns
    subgraph = subgraph_from_starting_column_header(step['column_evaluation_graph'][sheet_index], column_header)
    topological_sort = topological_sort_columns(subgraph)

    # We compile all of their formulas
    for column in topological_sort:
        column_formula_changes = step['column_python_code'][sheet_index][column]
        if column_formula_changes != '':
            # We replace the data frame in the code with it's parameter name!
            column_formula_changes = column_formula_changes.strip().replace('df', f'{step["df_names"][sheet_index]}')
            code.append(column_formula_changes)

    return code


def describe_set_column_formula_step(
        sheet_index,
        column_header,
        old_formula, # NOTE: the change_column_type formula relies on this not being used in the transpile step
        new_formula, # same as above
        df_names=None
    ):

    if df_names is not None:
        df_name = df_names[sheet_index]
        return f'Set {column_header} in {df_name} to {new_formula}'
    return f'Set {column_header} to {new_formula}'


SET_COLUMN_FORMULA_STEP = {
    'step_version': 1,
    'step_display_name': SET_COLUMN_FORMULA_DISPLAY_NAME,
    'event_type': SET_COLUMN_FORMULA_EVENT,
    'step_type': SET_COLUMN_FORMULA_STEP_TYPE,
    'params': SET_COLUMN_FORMULA_PARAMS,
    'saturate': saturate_set_column_formula_step,
    'execute': execute_set_column_formula_step,
    'transpile': transpile_set_column_formula_step,
    'describe': describe_set_column_formula_step
}