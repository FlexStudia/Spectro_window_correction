# coding: utf-8

"""
    This model contains a tool for working with array-like objects.
"""

# PACKAGES
import numpy as np
from bisect import bisect_right


def is_array_empty(arr):
    """
        Checks if a given array is empty and prints a warning if it is.

    :param arr: np.array:
        The array to check
    :return: bool:
        True if the array is empty, False otherwise.
    """
    try:
        if not isinstance(arr, np.ndarray) and not isinstance(arr, list):
            return True
        if type(arr) == list:
            if arr == [] or arr == [0] * len(arr):
                return True
        if isinstance(arr, np.ndarray):
            if np.array_equal(arr, np.array([])) or np.array_equal(arr, np.zeros(len(arr))) or np.array_equal(arr, np.array([[]])):
                return True
        return False
    except Exception as e:
        raise Exception(f"Critical error in is_array_empty: {str(e)}") from e


def is_ascending(arr):
    """
        Checks if a given array or list is in ascending order.

    :param arr: numpy.ndarray or list
        input array or list to be checked for ascending order
    :return: bool
        boolean value indicating whether the input array or list is in ascending order.
        If arr is not numpy.ndarray neither list it returns False.
    """
    try:
        if not isinstance(arr, np.ndarray) and not isinstance(arr, list):
            return False
        if type(arr) == list:
            return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
        if isinstance(arr, np.ndarray):
            return np.all(arr[:-1] <= arr[1:])
        return False
    except Exception as e:
        raise Exception(f"Critical error in is_ascending: {str(e)}") from e


def is_positive(arr):
    """
        Checks if all elements in a given array are strictly positive (>0).

    :param arr: numpy.ndarray or list
        input array or list to be checked
    :return: bool
        A boolean value indicating whether all elements in the input array are positive.
        If arr is not numpy.ndarray neither list it returns False.
    """
    try:
        if not isinstance(arr, np.ndarray) and not isinstance(arr, list):
            return False
        if type(arr) == list:
            return all(x > 0 for x in arr)
        if isinstance(arr, np.ndarray):
            return np.all(arr > 0)
        return False
    except Exception as e:
        raise Exception(f"Critical error in is_positive: {str(e)}") from e


def all_values_are_included_1D_in_2D(arr, column, arr_container):
    """
        Check if all values in `arr` are included in the specified column of `arr_container`.

        This function verifies whether every element in the input array `arr` is present in the
        specified `column` of the 2D array `arr_container`.

        :param arr: list or array-like
            The array containing values to check for inclusion.
        :param column: int
            The column index of `arr_container` against which `arr` values are checked.
        :param arr_container: array-like
            A 2D array where the inclusion check is performed on the specified column.

        :return: bool
            Returns True if all elements in `arr` are found in the specified column of `arr_container`,
            otherwise returns False.
    """
    try:
        column_content = arr_container[:, column]
        return np.all(np.isin(arr, column_content))
    except Exception as e:
        raise Exception(f"Critical error in all_values_are_included: {str(e)}") from e


def all_values_are_included_2D_in_1D(arr, column, arr_container):
    """
        Check if all values in `arr` are included in the specified column of `arr_container`.

        This function verifies whether every element in the input array `arr` is present in the
        specified `column` of the 2D array `arr_container`.

        :param arr: 2D np.ndarray
            The array containing values to check for inclusion.
        :param column: int
            The column index of arr to check in arr_container.
        :param arr_container: 1D np.ndarray
            A 1D array where the inclusion check is performed.

        :return: bool
            Returns True if all elements in `arr` are found in the specified column of `arr_container`,
            otherwise returns False.
    """
    try:
        column_content = arr[:, column]
        return np.all(np.isin(arr, column_content))
    except Exception as e:
        raise Exception(f"Critical error in all_values_are_included: {str(e)}") from e


def extract_a_column(arr, column_index):
    """
        Extracts a specified column from the input array.

        This function takes a 2D NumPy array and an integer representing a column index, and returns the specified column as a new array.

    :param arr: np.ndarray
    	The 2D array from which the column will be extracted.
    :param column_index: int
    	The index of the column to extract.

    :return: np.ndarray
    	The extracted column as a 1D array.
    """
    try:
        return np.array(arr[:, column_index])
    except Exception as e:
        raise Exception(f"Critical error in extract_a_column: {str(e)}") from e


def closest_values_in_a_list(a_list, a_value):
    """
        Find the closest lower and upper values in a list relative to a given value.

        This function takes a list of numbers and a value, sorts the list, and then identifies
        the closest lower and upper values in the list relative to the given value. If there is no
        lower or upper value in the list, the respective result will be NaN.

    :param a_list: list
        The list of numeric values to search through.
    :param a_value: numeric
        The value for which the closest lower and upper values are sought.

    :return: tuple
        A tuple containing the closest lower and upper values relative to the given value.
    """
    try:
        sorted_list = sorted(a_list)
        i = bisect_right(sorted_list, a_value)
        closest_lower = sorted_list[i - 1] if i > 0 else np.nan
        closest_upper = sorted_list[i] if i != len(sorted_list) else np.nan
        return closest_lower, closest_upper
    except Exception as e:
        raise Exception(f"Critical error in closest_values_in_a_list: {str(e)}") from e


def is_a_value_inside_the_given_column_in_data(value, arr, column_index):
    """
        Checks if a value exists within the specified column of a 2D array.

        This function evaluates whether a given value is within the range defined by
        the minimum and maximum values of a specified column in a 2D numpy array.

    :param value: float
    	The value to check in relation to the column.
    :param arr: numpy.ndarray
    	The 2D array containing data.
    :param column_index: int
    	The index of the column within the data to check.

    :return: bool
    	True if the value is within the range of the column, otherwise False.
    """
    try:
        column_content = arr[:, column_index]
        min_value = np.min(column_content)
        max_value = np.max(column_content)
        return min_value <= value <= max_value
    except Exception as e:
        raise Exception(f"Critical error in is_a_value_inside_the_given_column_in_data: {str(e)}") from e


def are_all_values_inside_the_given_column_in_data(arr, column_index, arr_container):
    """
        Checks if all values in a specified column of an array are within the bounds of another given array.

    :param arr: 2D np.ndarray
        The array from which values in the specified column will be checked.
    :param column_index: int
        The index of the column in 'arr' to be checked.
    :param arr_container: 1D np.ndarray
        The array whose minimum and maximum values define the bounds.

    :return: bool
        Returns True if all values in the specified column are within the min and max values of 'arr_container'; otherwise, returns False.
    """
    try:
        column_content = arr[:, column_index]
        min_value = np.min(arr_container)
        max_value = np.max(arr_container)
        for value in column_content:
            if not min_value <= value <= max_value:
                return False
        return True
    except Exception as e:
        raise Exception(f"Critical error in are_all_values_inside_the_given_column_in_data: {str(e)}") from e

def find_closest_index(array, value):
    """
    	Finds the index of the element in an array that is closest to a given value.

    	This function computes the absolute difference between each element in the array and the given value, then finds the index of the minimum difference.

    :param array: array-like
        The array in which to search for the closest value.
    :param value: float
        The value to which the closest element in the array is sought.

    :return index: int
        The index of the element in the array that is closest to the given value.
    """
    try:
        return (np.abs(array - value)).argmin()
    except Exception as e:
        raise Exception(f"Critical error in find_closest_index: {str(e)}") from e
