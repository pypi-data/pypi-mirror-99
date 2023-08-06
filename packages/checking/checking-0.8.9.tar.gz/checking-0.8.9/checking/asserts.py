"""
This module contains helper functions, implementing various assertions and providing a convenient reporting facility.
Most helpers have *message* parameter which, while optional, is strongly recommended to use.
"""
from typing import Any, Union, Sequence, Sized, Optional

from .helpers.others import short, diff
from .exceptions import SkipTestException
from .exceptions import TestBrokenException


def is_true(obj: Any, message: Optional[str] = None):
    """
    Checks if an object is truthy, counterpart to *is_false()*.

    :param obj: object to evaluate
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if an object is not truthy
    """
    if not obj:
        _message = _mess(message)
        raise AssertionError(f'{_message}'
                             'Expected: True'
                             '\nActual  : False')


def is_false(obj: Any, message: Optional[str] = None):
    """
    Checks if an object is falsy, counterpart to *is_true()*.

    :param obj: object to evaluate
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if an object is not falsy
    """
    if obj:
        _message = _mess(message)
        raise AssertionError(f'{_message}'
                             'Expected: False'
                             '\nActual  : True')


def equals(expected: Any, actual: Any, message: Optional[str] = None):
    """
    Checks if two objects are equal, counterpart to *not_equals()*.

    :param expected: object to evaluate
    :param actual: reference object
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if objects are not equal, detailing the objects and their types
    """
    if (expected is actual) or expected == actual:
        return
    _message = _mess(message)
    differs = diff(expected, actual)
    if differs:
        _message = f'{_message}{differs}\n'
    raise AssertionError(f"{_message}Objects are not equal:\n"
                         f"Expected: '{short(expected, 150)}' <{type(expected).__name__}>\n"
                         f"Actual  : '{short(actual, 150)}' <{type(actual).__name__}>")


def not_equals(expected: Any, actual: Any, message: Optional[str] = None):
    """
    Checks if two objects are not equal, counterpart to *equals()*.

    :param expected: object to evaluate
    :param actual: reference object
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if objects are equal, detailing the objects and their types
    """
    if (expected is actual) or expected == actual:
        _message = _mess(message)
        raise AssertionError(f'Objects are equal:'
                             f'\nExpected: {short(expected)}'
                             f'\nActual  : {short(actual)}')


def is_none(obj: Any, message: Optional[str] = None):
    """
    Checks if an object is None, counterpart to *is_not_none()*.

    :param obj: object to evaluate
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if object is not None, detailing the type of the object
    """
    _message = _mess(message)
    if obj is not None:
        raise AssertionError(f"{_message}Object '{short(obj)}' <{type(obj).__name__}> is not None!")


def is_not_none(obj: Any, message: Optional[str] = None):
    """
    Checks if an object is not None, counterpart to *is_none()*.

    :param obj: object to evaluate
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if object is None
    """
    _message = _mess(message)
    if obj is None:
        raise AssertionError(f'{_message}Unexpected None!')


def test_fail(message: Optional[str] = None):
    """
    Fails and mark as *failed* the test intentionally, detailing the reason.
    Use this instead of asserting a crafted broken condition when you need to fail a test.

    :param message: concrete failure description
    :return: None
    :raise AssertionError: always raises
    """
    raise AssertionError(message if message else 'Test was failed intentionally!')


def test_break(message: Optional[str] = None):
    """
    Break and mark as *broken* the test intentionally, detailing the reason.
    Use this instead of throwing arbitrary exceptions when you need to break a test.

    :param message: concrete failure description
    :return: None
    :raise AssertionError: always raises
    """
    raise TestBrokenException(message if message else 'Test was broken intentionally!')


def test_skip(message: Optional[str] = None):
    """
    Skip and mark a test as *ignored*, detailing the reason.
    Use this function to skip a test when some condition makes a test meaningless.

    :param message: concrete failure description
    :return: None
    :raise AssertionError: always raises
    """
    raise SkipTestException(message if message else 'Test was ignored intentionally!')


def contains(part: Any, whole: Any, message: Optional[str] = None):
    """
    Checks if an object is contained within another object, essentially runs an *a in b* check.
    Counterpart to *not_contains()*.

    :param part: object to search for
    :param whole: container to search in
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if part is not found in whole
    :raise TestBrokenException: if whole is not an iterable,
        whole does not implement __contains__ or there is a type mismatch, e.g. 1 in '123'
    """
    __contains_or_not(part, whole, message=message)


def not_contains(part: Any, whole: Any, message: Optional[str] = None):
    """
    Checks if an object is not contained within another object, essentially runs an *a not in b* check.
    Counterpart to *equals()*.

    :param part: object to search for
    :param whole: container to search in
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if part is found in whole
    :raise TestBrokenException: if whole is not an iterable,
        whole does not implement *__contains__* or there is a type mismatch, e.g. 1 in '123'
    """
    __contains_or_not(part, whole, is_contains=False, message=message)


def is_zero(actual: Union[int, float]):
    """
    Checks if an object is equal to zero.

    :param actual: object to evaluate
    :return: None
    :raise AssertionError: if object is not equal to zero
    """
    _check_argument_is_number(actual, 'is_zero')
    if actual != 0:
        raise AssertionError(f"'{short(actual)}' <{type(actual).__name__}> is not equal to zero!")


def is_positive(actual: Union[int, float, Sequence]):
    """
    Checks if an object or object's length (if the object is a Sequence) is greater than zero.

    :param actual: object to evaluate
    :return: None
    """
    if isinstance(actual, (int, float)):
        if actual <= 0:
            raise AssertionError(f"'{short(actual)}' <{type(actual).__name__}> is not positive!")
    else:
        if _get_length_if_sized(actual) <= 0:
            raise AssertionError(f"Length of '{short(actual)}' <{type(actual).__name__}> is not positive!")


def is_negative(actual: Union[int, float]):
    """
    Checks if an object is less than zero.

    :param actual: object to evaluate
    :return: None
    """
    _check_argument_is_number(actual, 'is_negative')
    if actual >= 0:
        raise AssertionError(f"'{short(actual)}' <{type(actual).__name__}> is not negative!")


def is_empty(container: Sized, message: Optional[str] = None):
    """
    Checks if a container is empty (the length of a container is equal to zero).
    Counterpart to *is_not_empty()*.

    :param container: object to evaluate
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if object is not empty (has length greater than zero)
    :raise TestBrokenException: if object has ho length attribute
    """
    _message = _mess(message)
    if _get_length_if_sized(container):
        raise AssertionError(f"{_message}'{short(container)}' <{type(container).__name__}> is not empty!")


def is_not_empty(container: Sized, message: Optional[str] = None):
    """
    Checks if a container is not empty (the length of a container is greater than zero).
    Counterpart to *is_empty()*.

    :param container: object to evaluate
    :param message: concrete failure description
    :return: None
    :raise AssertionError: if object is empty (has length equal to zero)
    :raise TestBrokenException: if object has ho length attribute
    """
    _message = _mess(message)
    if not _get_length_if_sized(container):
        raise AssertionError(f"{_message}'{short(container)}' <{type(container).__name__}> is empty!")


def __contains_or_not(part, whole, is_contains: Optional[bool] = True, message: Optional[str] = None):
    try:
        if is_contains and part in whole:
            return
        if not is_contains and part not in whole:
            return
    except TypeError as e:
        if 'requires' in e.args[0]:
            raise TestBrokenException(f"Cannot execute 'contains' check, incompatible objects:"
                                      f"\nPart : '{short(part)}' <{type(part).__name__}>"
                                      f"\nWhole: '{short(whole)}' <{type(whole).__name__}>")
        raise TestBrokenException(f"Cannot execute 'contains' check, 'whole' is not an iterable:"
                                  f"\nWhole: '{short(whole)}' <{type(whole).__name__}>")

    _message = _mess(message)
    add_ = 'contains' if not is_contains else "doesn't contain"
    raise AssertionError(f"{_message}Object '{short(whole, 150)}' <{type(whole).__name__}> {add_} "
                         f"object '{short(part)}' <{type(part).__name__}>!")


def _mess(message: str) -> str:
    return f'{message}\n' if message else ''


def _get_length_if_sized(container: Sized) -> int:
    """
    Returns the length of a container.

    :param container: container to evaluate
    :return: length of the container
    :raise TestBrokenException: if object has ho length attribute
    """
    try:
        return len(container)
    except TypeError:
        raise TestBrokenException(f"Cannot execute emptiness test:"
                                  f"\n'{short(container)}' <{type(container).__name__}> has no 'len' attribute!")


def _check_argument_is_number(actual, name: str):
    if not isinstance(actual, (int, float)):
        raise TestBrokenException(f"Cannot execute '{name}', wrong type:"
                                  f"\nExpected: Union[int, float]"
                                  f"\nActual  : '{short(actual)}' <{type(actual).__name__}>")
