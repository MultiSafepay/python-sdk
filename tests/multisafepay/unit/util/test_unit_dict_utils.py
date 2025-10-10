# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Utility functions for test unit dict utils."""

from multisafepay.util.dict_utils import (
    merge_recursive,
    remove_null,
    remove_null_recursive,
    dict_empty,
)


def test_merge_recursive_with_non_overlapping_keys():
    """
    Test merging two dictionaries with non-overlapping keys.

    """
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    result = merge_recursive(dict1, dict2)
    assert result == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_merge_recursive_with_overlapping_keys():
    """
    Test merging two dictionaries with overlapping keys.


    """
    dict1 = {"a": 1, "b": {"x": 10}}
    dict2 = {"b": {"y": 20}, "c": 3}
    result = merge_recursive(dict1, dict2)
    assert result == {"a": 1, "b": {"x": 10, "y": 20}, "c": 3}


def test_merge_recursive_with_empty_dict1():
    """
    Test merging an empty dictionary with a non-empty dictionary.

    """
    dict1 = {}
    dict2 = {"a": 1, "b": 2}
    result = merge_recursive(dict1, dict2)
    assert result == {"a": 1, "b": 2}


def test_merge_recursive_with_empty_dict2():
    """
    Test merging a non-empty dictionary with an empty dictionary.


    """
    dict1 = {"a": 1, "b": 2}
    dict2 = {}
    result = merge_recursive(dict1, dict2)
    assert result == {"a": 1, "b": 2}


def test_remove_null_with_no_null_values():
    """
    Test removing null values from a dictionary with no null values.

    """
    data = {"a": 1, "b": 2, "c": 3}
    result = remove_null(data)
    assert result == {"a": 1, "b": 2, "c": 3}


def test_remove_null_with_some_null_values():
    """
    Test removing null values from a dictionary with some null values.


    """
    data = {"a": 1, "b": None, "c": 3}
    result = remove_null(data)
    assert result == {"a": 1, "c": 3}


def test_remove_null_with_all_null_values():
    """
    Test removing null values from a dictionary with all null values.

    """
    data = {"a": None, "b": None}
    result = remove_null(data)
    assert result == {}


def test_remove_null_with_empty_dict():
    """
    Test removing null values from an empty dictionary.

    """
    data = {}
    result = remove_null(data)
    assert result == {}


def test_remove_null_recursive_with_no_null_values():
    """
    Test removing null values from a dictionary with no null values.


    """
    data = {"a": 1, "b": 2, "c": 3}
    result = remove_null_recursive(data)
    assert result == {"a": 1, "b": 2, "c": 3}


def test_remove_null_recursive_with_some_null_values():
    """
    Test removing null values from a dictionary with some null values.

    """
    data = {"a": 1, "b": None, "c": 3}
    result = remove_null_recursive(data)
    assert result == {"a": 1, "c": 3}


def test_remove_null_recursive_with_nested_null_values():
    """
    Test removing null values from a dictionary with nested null values.

    """
    data = {"a": 1, "b": {"x": 10, "y": None}}
    result = remove_null_recursive(data)
    assert result == {"a": 1, "b": {"x": 10}}


def test_remove_null_recursive_with_empty_list():
    """
    Test removing null values from a dictionary with an empty list.

    """
    data = {"a": 1, "b": []}
    result = remove_null_recursive(data)
    assert result == {"a": 1, "b": []}


def test_remove_null_recursive_with_list_of_dicts():
    """
    Test removing null values from a dictionary with a list of dictionaries.

    """
    data = {"a": 1, "b": [{"x": 10, "y": None}, {"z": None}]}
    result = remove_null_recursive(data)
    assert result == {"a": 1, "b": [{"x": 10}]}


def test_remove_null_recursive_multiple_nested_levels_dicts_and_lists():
    """
    Test removing null values from a dictionary with multiple nested levels of dictionaries and lists.

    """
    data = {
        "a": 1,
        "b": {
            "x": 10,
            "y": None,
            "z": [{"m": None}, {"n": 20, "o": [{"p": None, "q": 30}]}],
        },
    }
    result = remove_null_recursive(data)
    assert result == {
        "a": 1,
        "b": {"x": 10, "z": [{"n": 20, "o": [{"q": 30}]}]},
    }


def test_dict_empty():
    """
    Test checking if a dictionary or list is empty.


    """
    assert dict_empty({}) == True
    assert dict_empty({"a": 1}) == False
