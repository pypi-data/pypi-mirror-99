# -*- coding: utf-8 -*-
# --------------------------
# Copyright © 2014 -            Qentinel Group.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------

"""Keywords for table elements.

Table elements are used to show many kinds of data. Tables have cells in
contain rows and columns. Cells can contain all kinds of elements. Cells
are usually refenced by coordinates or unique neighbouring values.
"""
from QWeb.internal.exceptions import QWebInstanceDoesNotExistError, QWebValueMismatchError, \
    QWebValueError
from QWeb.internal.actions import execute_click_and_verify_condition
from QWeb.internal import decorators, util, element
from QWeb.internal.lists import List

ACTIVE_LIST = None


@decorators.timeout_decorator
def use_list(locator, anchor="1", timeout=0, parent=None, child=None, **kwargs):  # pylint: disable=unused-argument
    r"""Define list for all other list keywords.

    Sets active table for other keywords.

    Examples
    --------
    .. code-block:: robotframework

         UseList            //*[@class\="list"]
         UseList            list                selector=class
         UseList            Calendar            Qentinel
         #Calendar is inside of ordered list instead of ul (ul=default):
         UseList            Calendar            Qentinel    tag=ol


    Parameters
    ----------
    locator : str
        Text that locates the list. If text is inside of unordered list
        then list is selected. If there is no known texts in list
        xpath can be used to locate correct list. If wanted list is multiple amount
        of whatever web elements with some common attribute, xpath can be used
        to select those elements. When using XPaths, the equal sign "=" must be
        escaped with a "\".
    anchor : str
        Index number or text near the locator element.
        If the page contains many places where the locator is then anchor is used
        to select the wanted item.
    timeout : str | int
        How long we search before failing. Default = Search Strategy default timeout (10s)
    kwargs :
        Accepted kwargs: tag = html_tag to identify if list is ordered or unordered one.
    """
    global ACTIVE_LIST  # pylint:disable=global-statement
    ACTIVE_LIST = List.from_list_instance(locator, anchor, parent=parent, child=child, **kwargs)


def verify_length(expected_length):
    """Verify lists length."""
    if _list_exists():
        active = ACTIVE_LIST.update_list()
        list_length = len(active.web_list)
        if int(expected_length) == list_length:
            return
        raise QWebValueMismatchError(
            'Expected length "{}" didn\'t match to list length "{}".'
            .format(expected_length, list_length))


@decorators.timeout_decorator
def verify_list(text, index=None, timeout=0):  # pylint: disable=unused-argument
    """Verify list contains given text.

    Examples
    --------
    .. code-block:: robotframework

        UseList         Qentinel
        VerifyList      Pace Robot              #list contains given text (text can be anywhere)
        VerifyList      Test Automation     2   #List index 2 contains given text
    """
    if _list_exists():
        active = ACTIVE_LIST.update_list()
        if index:
            index = _check_index(index)
        if active.contains(text, index):
            return
        raise QWebValueError('List didn\'t contain text "{}"'.format(text))


@decorators.timeout_decorator
def click_list(index, timeout=0, js=True, **kwargs):  # pylint: disable=unused-argument
    """Click list element with in given index.

    Examples
    --------
    .. code-block:: robotframework

        ClickList       1
        ClickList       1       tag=div
    """
    if _list_exists():
        active = ACTIVE_LIST.update_list()
        if index:
            index = _check_index(index)
            web_element = element.get_element_to_click_from_list(
                active.web_element_list, index, **kwargs)
            if execute_click_and_verify_condition(web_element, timeout=timeout, js=js, **kwargs):
                return


def verify_no_list(text, index=None):
    """Verify that text is not in the list.

    Examples
    --------
    .. code-block:: robotframework

        UseList         Qentinel
        VerifyNoList    Pace Robot              #Text is not in list
        VerifyNoList    Test Automation     2   #List index 2 not containing text
    """
    if _list_exists():
        active = ACTIVE_LIST.update_list()
        if index:
            index = _check_index(index)
        if not active.contains(text, index):
            return
        raise QWebValueMismatchError('List contains text "{}"'.format(text))


def get_list(index=None, **kwargs):
    """Verify that text is not in the list.

    Examples
    --------
    .. code-block:: robotframework

        UseList         Qentinel
        ${LIST}         GetList         #Get list to variable
        ${VAL}          GetList      2  #Get value from list index 2
        #Get substring from list index 1
        ${VAL}          GetList      1  between=word???another

    Parameters
    ----------
    index : if given, gets text only from that index.
    kwargs :
        |  Accepted kwargs:
        |       between : str/int - Start???End - Return all chars between texts Start and End.
        |       from_start : int - Return x amount of chars. Starting from first char
        |       from_end : int - Return x amount of chars. Starting from last char
        |       include_locator : True - Starting text is part of returned string
        |       exclude_post : False - Ending text is part of returned string
        |       int : True - Return integer instead of string
        |       float : int - Return float instead of string
    """
    active = ACTIVE_LIST.update_list()
    if index:
        index = _check_index(index)
        text = active.web_list[index]
        return util.get_substring(text, **kwargs)
    return active.web_list


def _list_exists():
    if isinstance(ACTIVE_LIST, List) is False:
        raise QWebInstanceDoesNotExistError('List has not been defined with UseList keyword')
    return True


def _check_index(index):
    try:
        if int(index) - 1 < len(ACTIVE_LIST.web_list):
            return int(index) - 1
        raise QWebValueError('Index can\'t be bigger than length of the list')
    except TypeError:
        raise QWebValueError('Index has to be number')
