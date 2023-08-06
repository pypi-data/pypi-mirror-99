#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports an error box that can be used to pass the errors
we need. 

Further exports helper functions for creating errors
of different flavors. We wrap these functions in the same
EditError box to avoid creating too many new classes!

See more about why we use errors here: 
https://stackoverflow.com/questions/16138232/is-it-a-good-practice-to-use-try-except-else-in-python
"""
import traceback
from typing import Set, List

class CreationError(Exception):
    """
    An error that occurs during a mito.sheet call, on creation
    of the mito widget. 
    """
    def __init__(self, type_, header, to_fix):
        """
        Creates a creation error. 

        type_: the error id string.
        header: the header of the error message to be displayed.
        to_fix: instructions on how to handle or fix the error.
        """
        self.type_ = type_ # we have an _ to avoid overwriting the build in type
        self.header = header
        self.to_fix = to_fix

class EditError(Exception):
    """
    An error that occurs during the processing of an editing event.
    """
    def __init__(self, type_, header, to_fix):
        """
        Creates a creation error. 

        type_: a string that is the error type. 
        header: the header of the error message to be displayed.
        to_fix: instructions on how to handle or fix the error.
        """
        self.type_ = type_ # we have an _ to avoid overwriting the build in type
        self.header = header
        self.to_fix = to_fix

def make_no_sheet_error(sheet_indexes: Set[str]):
    """
    Helper function for creating a no_sheet_error.

    Occurs when a user edits a formula with a reference to a sheet that does not exist.
    """
    to_fix = f'There is an issue behind the scenes with that operation, we\'ll get it fixed as soon as possible!'

    return EditError(
        'no_sheet_error', 
        'No Sheet Exists',
        to_fix
    )

def make_no_column_error(column_headers: Set[str]):
    """
    Helper function for creating a no_column_error.

    Occurs when a user edits a formula with a reference to a column that does not exist.
    """
    if len(column_headers) == 1:
        to_fix = f'Sorry, there is no column with the name {next(iter(column_headers))}. Did you type it correctly?'
    else:
        to_fix = f'Sorry, there are no column with the names {", ".join(column_headers)}. Did you type them correctly?'

    return EditError(
        'no_column_error', 
        'No Column Exists',
        to_fix
    )

def make_column_exists_error(column_header: str):
    """
    Helper function for creating a column_exists_error.

    Occurs when:
    -  the user adds a column that already exists in the dataframe.
    """
    return EditError(
        'column_exists_error', 
        'Column Already Exists',
        f'Sorry, a column already exists with the name {column_header}. Try picking a different name!'
    )

def make_invalid_formula_error(formula: str, to_fix=None):
    """
    Helper function for creating a invalid_formula_error.

    Occurs when:
    -  the user edits a cell to an expression that cannot be parsed.
    """
    if to_fix is None:
        to_fix = f'Sorry, the formula \'{formula}\' is invalid. Did you type it correctly?'

    return EditError(
        'invalid_formula_error',
        'Invalid Formula',
        to_fix
    )

def make_circular_reference_error():
    """
    Helper function for creating a circular_reference_error.

    Occurs when:
    -  an edit introduces a circular reference.
    """
    return EditError(
        'circular_reference_error',
        'Circular Reference',
        f'Sorry, circular references are not supported currently.'
    )

def make_wrong_column_metatype_error(column_header: str):
    """
    Helper function for creating a wrong_column_metatype_error.

    Occurs when:
    -  a user edits a column to a formula when it is not a formula type column.
    """
    return EditError(
        'wrong_column_metatype_error',
        'Wrong Column Type',
        f'Sorry, the column {column_header} is a data column. We don\'t currently support changing it to a formula.'
    )

def make_invalid_column_headers_error(column_headers: List[str]):
    """
    Helper function for creating a invalid_column_headers_error.

    Occurs when:
    -  a user creates (or renames) a column(s) that has an invalid name.
    """
    to_fix = f'All headers in the dataframe must contain at least one letter and no symbols other than numbers and "_". Invalid headers: {", ".join(column_headers)}'

    return EditError(
        'invalid_column_header_error',
        'Invalid Column Header',
        to_fix
    )

def make_execution_error():
    """
    Helper function for creating a execution_error.

    Occurs when:
    -  running an existing analysis on the parameters passed to the mito sheet throw an error.
    """
    # TODO: this to_fix message is _just terrible_
    return EditError(
        'execution_error',
        'Execution Error',
        f'Sorry, there was an error during executing this code.'
    )

def make_function_execution_error(function):
    """
    Helper function for creating a function_execution_error.

    Occurs when:
    -  An error occurs inside of a mito sheet function
    """
    # TODO: this to_fix message is _just terrible_
    return EditError(
        'execution_error',
        f'Error Executing {function}',
        f'Sorry, there was an error in the {function}. Please check the documentation to make sure you called it correctly.'
    )

def make_unsupported_function_error(functions: Set[str]):
    """
    Helper function for creating a unsupported_function_error.

    Occurs when:
    -  the user's new formula containing a function that is not supported by mito.
    """
    # TODO: we could fix up this to_fix, lol.
    if len(functions) == 1:
        to_fix = f'Sorry, mito does not currently support the function {next(iter(functions))}. To request it, shoot us an email!'
    else:
        to_fix = f'Sorry, mito does not currently support the functions {", ".join(functions)}. To request it, shoot us an email!'

    return EditError(
        'unsupported_function_error',
        'Unsupported Function',
        to_fix
    )

def make_invalid_column_delete_error(column_header, dependents):
    """
    Helper function for creating a invalid_column_delete_error.

    Occurs when:
    -  the user deletes a column that is referenced by other columns
    """
    # We make sure it's a list, for easy accessing!
    dependents = list(dependents)

    # We make the error message read nicely!
    if len(dependents) == 1:
        dependent_string = f'column {dependents[0]}'
    elif len(dependents) == 2:
        dependent_string = f'columns {dependents[0]} and {dependents[1]}'
    else:
        dependent_string = f'columns {", ".join(dependents[: -1])}, and {dependents[-1]}'

    return EditError(
        'invalid_column_delete_error',
        'Column Has Dependents',
        f'{column_header} cannot be deleted, as it is referenced in {dependent_string}. Please remove these references before deleting.'
    )

def make_invalid_arguments_error(function):
    """
    Helper function for creating a invalid_arguments_error.

    Occurs when:
    -  the user calls a sheet function with incorrect arguments
    """
    return EditError(
        'invalid_arguments_error',
        f'Invalid Arguments to {function}',
        f'It looks like you passed the wrong arguments to {function}. Try checking out the documentation to see correct usage!'
    )

def make_invalid_aggregation_error():
    """
    Helper function for creating a invalid_aggregation_error.

    Occurs when:
    -  the user tries to .agg with a function on a column that has the wrong type (e.g. 'mean' on a
        column of strings).
    """
    return EditError(
        'invalid_aggregation_error',
        f'Invalid Aggregation Function',
        f'Sorry, you tried to aggregate with a function that could not be applied to that type of column. Please try again!'
    )

def make_invalid_filter_error(filter_value, correct_type):
    """
    Helper function for creating a invalid_filter_error.

    Occurs when:
    - A user tries to create a filter with an invalid value (e.g. a string, when filtering numbers
      or a non-date when filtering dates).
    """

    if correct_type == 'datetime':
        correct_format = 'as YYYY-MM-DD.'
    elif correct_type == 'number':
        correct_format = 'that is a number.'
    else:
        correct_format = 'that is valid.'

    return EditError(
        'invalid_filter_error',
        f'Invalid Filter',
        f'Sorry, the value {filter_value} is not a valid value for that {correct_type} filter. Please enter a value {correct_format}!'
    )

def make_invalid_sort_error(column_header):
    """
    Helper function for creating a invalid_sort_error.

    Occurs when:
    - A user tries to sort a dataframe on a column of mixed types 
    (e.g. a column with strings and floats).
    """

    return EditError(
        'invalid_sort_error',
        f'Invalid Sort',
        f'Sorry, the column {column_header} has mixed data types. Please make sure the column has one datatype before trying to sort.'
    )

def make_df_exists_error(df_name):
    """
    Helper function for creating a df_exists_error.

    Occurs when:
    - A user tries to create a dataframe with the name of an already existing
    dataframe in the sheet.
    """

    return EditError(
        'df_exists_error',
        f'Dataframe Exists',
        f'Sorry, the dataframe {df_name} already exists. Please pick a different name.'
    )

def make_invalid_column_type_change_error(column_header, old_column_type, new_column_type):
    """
    Helper function for creating a invalid_column_type_change_error.

    Occurs when:
    - A user tries to change the type of one column to an incompatible type (e.g. from
      a number to a datetime, which is impossible).
    """

    return EditError(
        'invalid_column_type_change_error',
        f'Invalid Type Change',
        f'Sorry, the column {column_header} has a type {old_column_type}, which cannot be changed to the type {new_column_type}.'
    )

def make_invalid_pivot_error():
    """
    Helper function for creating a invalid_pivot_error.

    Occurs when:
    -  the user runs a pivot that is invalid in some way.
    """
    # TODO: this to_fix message is _just terrible_
    return EditError(
        'invalid_pivot_error',
        'Pivot Error',
        f'Sorry, there was an error computing your pivot. Please try a different pivot!'
    )

def make_duplicated_pivot_column_error(column_header):
    """
    Helper function for creating duplicated_pivot_column_error

    Occurs when:
    - the user adds a column to both the row and the value section of the pivot table
        which is not covered by a special case
    """
    return EditError(
        'duplicated_column_in_pivot_error',
        f'Invalid Pivot Configuration',
        f'Sorry, the column {column_header} is used twice. Please remove it from one section.'
    )

ARG_FULL_NAME = {
    'int': 'number',
    'float': 'number',
    'str': 'string',
    'bool': 'boolean'
}

def make_operator_type_error(operator, arg_one_type, arg_two_type):
    """
    Helper function for creating a operator_type_error.

    Occurs when:
    - user uses an operator to add/mul/div (etc) invalid types. E.g. they do: 1 + "hi",
      or pd.Series(['hi']) / 10.
    """

    # Provide a helpful error message, if possible, for the case of a number and a string
    # (which is the most common of these errors).
    if (arg_one_type == 'str' and (arg_two_type == 'int' or arg_two_type == 'float')) or \
        (arg_two_type == 'str' and (arg_one_type == 'int' or arg_one_type == 'float')):
        to_fix = f'Sorry, you tried to {operator} on a string and a number. Please wrap the number argument in a call to the VALUE function.'
    else:
        # Otherwise, handle errors in a non-specific way - this is a catch all for the rest of operator type errors
        type_one_full_name = ARG_FULL_NAME[arg_one_type] if arg_one_type in ARG_FULL_NAME else arg_one_type
        type_two_full_name = ARG_FULL_NAME[arg_two_type] if arg_two_type in ARG_FULL_NAME else arg_two_type
        # TODO: once we have a step that changes the column type, we should update this error to be more helpful
        to_fix = f'Sorry, you tried to use {operator} on a {type_one_full_name} and a {type_two_full_name}. Please change the type of one of these columns to be compatible.'

    return EditError(
        'operator_type_error',
        f'Error with {operator}',
        to_fix
    )

def get_recent_traceback_as_list():
    """
    Helper function for getting the traceback of the most recent error.
    
    This, in turns, gives us a stack trace for any error that we want
    to log with detail, in a format that is sendable to mixpanel.

    We get this as a list of strings, as mixpanel truncates strings at 255 chars
    and thus we avoid things getting chopped this way.
    """
    return traceback.format_exc().split('\n')
