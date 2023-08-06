# pylint: disable=too-many-lines

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

"""Keywords for text elements.

Text elements are considered to be elements that have visible text. Input
elements are not considered text elements even though they might have visible
text.
"""
from pynput.keyboard import Controller
import pyperclip
from QWeb.internal.actions import scroll, execute_click_and_verify_condition, hover_to, \
    text_appearance, scroll_dynamic_web_page, scroll_first_scrollable_parent_element
from QWeb.internal import element, decorators, util, download, text as internal_text
from QWeb.internal.config_defaults import CONFIG
from QWeb.internal.exceptions import QWebValueError, QWebEnvironmentError, QWebTimeoutError,\
    QWebElementNotFoundError, QWebDriverError
from robot.api import logger
import os


@decorators.timeout_decorator
def verify_text(text, timeout=0, anchor="1", **kwargs):  # pylint: disable=unused-argument
    """Verify page contains given text.

    Keyword waits until timeout has passed. If timeout is not specified, it
    uses default timeout that can be adjusted with DefaultTimeout keyword.

    VerifyText does not require for the text to be unique.

    Examples
    --------
    .. code-block:: robotframework

        VerifyText        Canis

    In the above example the test will wait until "Canis" exists on the page or default
    timeout has passed.

    If you wish to increase the wait time

    .. code-block:: robotframework

       VerifyText        Canis       20  # Waits 20 seconds

    If you want to change default timeout

    .. code-block:: robotframework

       DefaultTimeout    2m
       VerifyText        Canis      # Waits 2 minutes

    Parameters
    ----------
    text : str
        Text to be verified.
    timeout : str | int
        How long we try to find text before failing. Default 10 (seconds)
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text.
        window_find : True - When WindowFind is used VerifyText is not looking
        texts for dom, but simulates ctrl+f like search to current viewport.

    Raises
    ------
    QWebElementNotFoundError
        If page does not contain text

    Uses . (dot) in the xpath to represent the text in the node. Using dot
    instead of text() since text() does not handle cases where the text is
    in both the a parent node and in its child node.
    """
    kwargs['css'] = False
    window_find = util.par2bool(kwargs.get('window_find', CONFIG['WindowFind']))
    if window_find:
        web_elements = internal_text.find_text(text)
    else:
        web_elements = internal_text.get_element_by_locator_text(text, anchor, **kwargs)
    if web_elements:
        return


@decorators.timeout_decorator
def verify_no_text(text, timeout=0, **kwargs):  # pylint: disable=unused-argument
    """Verify that page does not contain given text.

    Keyword waits until timeout has passed. If timeout is not specified, it
    uses default timeout that can be adjusted with DefaultTimeout keyword.

    Examples
    --------
    .. code-block:: robotframework

        VerifyNoText        Canis

    In the above example the test will wait 10 seconds until checks if the
    Canis exist on the page

    If you wish to increase the wait time

    .. code-block:: robotframework

       VerifyNoText        Canis       20  # Waits 20 seconds

    If you want to change default timeout

    .. code-block:: robotframework

       DefaultTimeout      2m
       VerifyNoText        Canis      # Waits 2 minutes

    Parameters
    ----------
    text : str
        Text to be verified.
    timeout : str | int
        How long we wait for text to disappear before failing.
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text

    Raises
    ------
    QWebValueError
        If page does not contain text

    Searches using XPath contains function so that substrings are also
    looked through.

    Uses . (dot) in the xpath to represent the text in the node. Using dot
    instead of text() since text() does not handle cases where the text is
    in both the a parent node and in its child node.
    """
    kwargs['css'] = False
    web_elements = internal_text.get_element_by_locator_text(
        text, allow_non_existent=True, **kwargs)
    if not web_elements:
        return
    raise QWebValueError('Page contained the text "{}" after timeout'.format(
        text))


@decorators.timeout_decorator
def verify_text_count(text, expected_count, timeout=0, **kwargs):  # pylint: disable=unused-argument
    """Verify page contains given text given times.

    Keyword waits until timeout has passed. If timeout is not specified, it
    uses default timeout that can be adjusted with DefaultTimeout keyword.

    VerifyTextCount does not require for the text to be unique.

    Examples
    --------
    .. code-block:: robotframework

        VerifyTextCount        Canis     3

    In the above example the test will wait until "Canis" exists on the page or default
    timeout has passed.

    If you wish to increase the wait time

    .. code-block:: robotframework

       VerifyTextCount        Canis       3      20  # Waits 20 seconds

    If you want to change default timeout

    .. code-block:: robotframework

       SetConfig              DefaultTimeout   2m
       VerifyTextCount        Canis      3     # Waits 2 minutes

    Parameters
    ----------
    text : str
        Text to be verified.
    expected_count : str | int
        How many times text must be shown on page
    timeout : str | int
        How long we try to find text before failing. Default 10 (seconds)
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text

    Raises
    ------
    QWebValueError
        If page does not contain text expected number of times

    Uses . (dot) in the xpath to represent the text in the node. Using dot
    instead of text() since text() does not handle cases where the text is
    in both the a parent node and in its child node.
    """
    expected_count = int(expected_count)
    kwargs['css'] = False
    webelements = internal_text.get_all_text_elements(text, **kwargs)
    element_count = len(webelements)

    if element_count == expected_count:
        return
    raise QWebValueError('Page contained {0} texts instead of {1} after timeout'
                         .format(element_count, expected_count))


@decorators.timeout_decorator
def get_text_count(text, timeout=0, **kwargs):  # pylint: disable=unused-argument
    """Get count of appearances for given text.

    Keyword waits until timeout has passed. If timeout is not specified, it
    uses default timeout that can be adjusted with DefaultTimeout keyword.

    GetTextCount does not require for the text to be unique.
    Return count of appearances for given tex.

    Examples
    --------
    .. code-block:: robotframework

        ${COUNT}    GetTextCount        Canis

    In the above example the test will wait until "Canis" exists on the page or default
    timeout has passed.

    If you wish to increase the wait time

    .. code-block:: robotframework

       ${COUNT}    GetTextCount      Canis  20  # Waits 20 seconds

    Parameters
    ----------
    text : str
        Text to be verified.
    timeout : str | int
        How long we try to find text before failing. Default 10 (seconds)
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text
    """
    kwargs['css'] = False
    web_elements = internal_text.get_all_text_elements(text, **kwargs)
    return len(web_elements)


@decorators.timeout_decorator
def click_text(text, anchor="1", timeout=0, parent=None,
               child=None, js=None, **kwargs):
    """Click text on web page.

    Keyword looks for an exact match and if not found uses xpath defined in
    Search Strategy. If the given text corresponds to multiple elements, it
    clicks the first element.

    If you want to click other element than the first one found, you need to
    use anchor or index.

    Keyword tries to click element until it succeeds or timeout has passed.
    If timeout is not specified, it uses default timeout that can be adjusted
    with DefaultTimeout keyword.

    Examples
    --------
    .. code-block:: robotframework

        ClickText        Canis

    In the above example the ClickText keyword will click the word Canis.
    If there are multiple instances of the word Canis on the page, first one
    will be clicked unless 'anchor' is given. You can
    specific which one should be clicked by either:

    - a number or
    - a word that is near to the word Canis

    For example

    .. code-block:: robotframework

        ClickText    Canis    3     # clicks the third "Canis" on the page
        ClickText    Canis    Dog   # clicks the "Canis" near to the word "Dog"

    If you want to specify how long ClickText tries, you need to add both anchor
    and timeout.

    .. code-block:: robotframework

        ClickText    Canis    1     20s   # Tries to click the first "Canis" for 20s

    If clickable element is child or parent of locator element use child/parent
    attribute + elements tagname to pick right element

    .. code-block:: robotframework

        ClickText   Canis     parent=span # Clicks Canis element's first parent with span -tag
        ClickText   Canis     child=a     # First childnode with a -tag

    .. code-block:: robotframework

        ClickText   Canis     js=true     #Use Javascript click instead of Selenium

    Parameters
    ----------
    text : str
        Text to be clicked.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long we wait element to appear and click to succeed
    parent : str
        tag name for clickable parent.
    child : str
        tag name for clickable child.
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text
    """
    anchor = str(anchor)
    web_element = internal_text.get_element_by_locator_text(
        text, anchor, parent=parent, child=child, **kwargs)
    if execute_click_and_verify_condition(web_element, timeout=timeout, js=js):
        return


def scan_click(text, text_to_appear, anchor="1", timeout=0, interval=None,
               parent=None, child=None, js=False, **kwargs):  # pylint: disable=unused-argument
    """Click text until a text appears.

    This keyword is required on slow pages where it takes time for a button
    listener to start. This clicks button and waits until text appears.

    For example

    .. code-block:: robotframework

        ScanClick    Cart    Cart contents
        ScanClick    Cart    Cart contents    1          5s
        ScanClick    Cart    Cart contents    Main Cart  20s   3s

    Parameters
    ----------
    text : str
        Text to be clicked.
    text_to_appear : str
        Text that appears after click
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long button is clicked if text does not appear
    interval : str
        How long to wait until text appear before clicking again
    parent : str
        tag name for clickable parent.
    child : str
        tag name for clickable child.
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text.
        el_type=item
        text(default) = find element by visible text | item = find item type element
    """
    el_type = kwargs.get('el_type', 'text')
    if el_type.lower() != 'text':
        click_item_until(text_to_appear, text, anchor, timeout, interval, js=False, **kwargs)
    else:
        click_until(text_to_appear, text, anchor, timeout,
                    interval, parent=None, child=None, js=False, **kwargs)


def skim_click(text, text_to_disappear='', anchor="1", timeout=0, interval=None,
               parent=None, child=None, js=False, **kwargs):
    """Click text until a text disappears.

    This keyword is required on slow pages where it takes time for a button
    listener to start. This clicks button and waits until text disappears.

    If text_to_disappear is not entered, it keyword will wait until text
    clicked disappears.

    For example

    .. code-block:: robotframework

        SkimClick    Cart
        SkimClick    Cart    Cart            1    5s
        SkimClick    Cart    Cart contents
        SkimClick    Cart    Go to cart      5s
        SkimClick    Cart    Cart            1    20s    5s

    Parameters
    ----------
    text : str
        Text to be clicked.
    text_to_disappear : str
        Text that appears after click
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long to button is clicked if text has not disappeared
    interval : str
        How long to wait until text disappears
    parent : str
        tag name for clickable parent.
    child : str
        tag name for clickable child.
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text
        el_type = 'item':
        text(default) = find element by visible text | item = find item type element
    """
    el_type = kwargs.get('el_type', 'text')
    if text_to_disappear == '':
        text_to_disappear = text
    if el_type.lower() != 'text':
        click_item_while(text_to_disappear, text, anchor, timeout, interval, js=js, **kwargs)
    else:
        click_while(text_to_disappear, text, anchor, timeout, interval, parent, child, js, **kwargs)


@decorators.timeout_decorator
def hover_text(text, anchor="1", timeout="0", **kwargs):  # pylint: disable=unused-argument
    """Hover over text.

    Keyword will fail if text is not visible. You should use VerifyText before HoverText
    if you are not sure text is already visible.

    Examples
    --------
    .. code-block:: robotframework

        HoverText        Canis

    Hover can be chained. For example

    .. code-block:: robotframework

        HoverText        Canis
        HoverText        Canis sub

    Parameters
    ----------
    text : str
        Text to be hovered-over.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long to button is clicked if text has not disappeared
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text
    """
    web_element = internal_text.get_element_by_locator_text(text, anchor, **kwargs)
    hover_to(web_element, timeout=timeout)


@decorators.timeout_decorator
def hover_item(locator, anchor="1", timeout="0", **kwargs):  # pylint: disable=unused-argument
    """Hover over text.

    Hover over web element.

    Examples
    --------
    .. code-block:: robotframework

        HoverItem        attrVal

    Hover can be chained. For example

    .. code-block:: robotframework

        HoverItem        attrVal
        HoverItem        attrVal sub

    Parameters
    ----------
    locator : str
        Element to be hovered-over.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long to button is clicked if text has not disappeared
    Accepted kwargs:
        css=False/off: Use this to bypass css search when finding elements
        by visible text
    """
    web_element = internal_text.get_item_using_anchor(locator, anchor, **kwargs)
    hover_to(web_element, timeout=timeout)


@decorators.timeout_decorator
def is_text(text, timeout="0.1s", **kwargs):
    """Return True/False if text is found on the screen.

    Used to get text presence to variable. This keyword returns after text is found.

    Returns True if text is found. Returns False if text is not found within timeout.

    If timeout is not set, keyword returns immediately.

    Examples
    --------
    .. code-block:: robotframework

        $note_visible=  IsText        Paused
        $note_visible=  IsText        Paused     5s

    Parameters
    ----------
    text : str
        Text to be searched from the screen.

    timeout : str | int
        How long we wait for text to appear before returning. Default 0.1s

    Returns
    -------
    Bool : True or False
    """
    try:
        return text_appearance(text, text_appear=True, timeout=timeout, **kwargs)
    except (QWebTimeoutError, QWebValueError):
        return False


@decorators.timeout_decorator
def is_no_text(text, timeout="2s", **kwargs):
    """Return True/False if text is found on the screen.

    Used to get text presence info to variable. This keyword returns if text is not visible or
    when it disappears.

    If text does not disappear, keyword returns False after timeout is exceeded.

    If timeout is not set, keyword returns immediately.

    Examples
    --------
    .. code-block:: robotframework

        $note_visible=  IsText        Paused
        $note_visible=  IsText        Paused     5s

    Parameters
    ----------
    text : str
        Text to be searched from the screen.

    timeout : str | int
        How long we wait for text to disappear before returning. Default 0.1s

    Returns
    -------
    Bool : True or False
    """
    try:
        return text_appearance(text, text_appear=False, timeout=timeout, **kwargs)
    except (QWebValueError, QWebTimeoutError):
        return False


@decorators.timeout_decorator
def verify_element_text(locator, text_to_find, timeout=0, anchor="1", **kwargs):
    r"""Verify that element contains specified text.

    Examples
    --------
    .. code-block:: robotframework

        VerifyElementText       //input[@value\="Button3"]      ButtonText
        VerifyElementText       ipsum    dolore

    Parameters
    ----------
    locator : str
        Visible text, some attribute of wanted element or Xpath expression without xpath= prefix.
        When using XPaths, the equal sign "=" must be escaped with a "\".
    text_to_find : str
        The text we are trying to verify from the element.
    timeout : int
        How long we wait that element is found before failing.
    anchor : str
        Text near the element to be clicked or index.
    kwargs :
        |  Accepted kwargs:
        |       strict : bool - Verify that the texts are an exact match.

    """
    locator_text = get_text(locator, timeout, anchor, **kwargs)
    strict = util.par2bool(kwargs.get('strict', False))
    if strict:  # exact match
        if text_to_find == locator_text:
            return
        raise QWebValueError(f'"{text_to_find}" != "{locator_text}"')
    if text_to_find in locator_text:
        return
    raise QWebValueError(f'"{text_to_find}" not in "{locator_text}"')


@decorators.timeout_decorator
def get_text(locator, timeout=0, anchor="1", **kwargs):  # pylint: disable=unused-argument
    r"""Get text from element specified by xpath.

    Examples
    --------
    .. code-block:: robotframework

        GetText          //*[@id\="click_me"]
        #uses text as a locator:
        GetText          click_me       between=click???me #returns _
        #uses any attribute of some div as locator:
        GetText          someattr       tag=div     from_start=5  #returns 5 first chars
        GetText          someattr       tag=div     from_end=5    #returns 5 last
        #returns last 5 chars before text Foo
        GetText          someattr       tag=div     between=???Foo  from_end=5
        #returns first 5 chars before text Foo
        GetText          someattr       tag=div     between=Foo???  from_start=5
        #returns first 5 chars before text Foo and text Foo
        GetText          someattr    tag=div   between=Foo???  from_start=5  include_locator=True
        #returns last 5 chars before text Foo and text Foo
        GetText          someattr       tag=div     between=???Foo  from_start=5  exclude_post=False
        GetText          someattr       tag=div     int=True    #return integer
        GetText          someattr       tag=div     from_start=3    float=True  #return float
    Parameters
    ----------
    locator : str
        Visible text, some attribute of wanted element or Xpath expression without xpath= prefix.
        When using XPaths, the equal sign "=" must be escaped with a "\".
    timeout : int
        How long we wait that element is found before failing.
    anchor : str
        Text near the element to be clicked or index.
    kwargs :
        |  Accepted kwargs:
        |       between : str/int - Start???End - Return all chars between texts Start and End.
        |       from_start : int - Return x amount of chars. Starting from first char
        |       from_end : int - Return x amount of chars. Starting from last char
        |       include_locator : True - Starting text is part of returned string
        |       exclude_post : False - Ending text is part of returned string
        |       int : True - Return integer instead of string
        |       float : int - Return float instead of string
    Returns
    -------
    text : Xpath value text
    """
    tag = kwargs.get('tag', None)
    if tag:
        try:
            anchor = int(anchor) - 1
            kwargs['element_kw'] = True
            web_element = element.get_elements_by_attributes(tag, locator, **kwargs)[anchor]
        except ValueError:
            raise QWebValueError(
                'Only index is allowed anchor when searching element by it\'s attribute')
    elif '//' not in locator:
        web_element = internal_text.get_text_using_anchor(locator, anchor)
    else:
        web_element = element.get_unique_element_by_xpath(locator)
    text = web_element.text
    return util.get_substring(text, **kwargs)


@decorators.timeout_decorator
def click_item(text, anchor="1", timeout=0, js=False, **kwargs):
    """Click item (usually icon or picture) on webpage.

    Finds webelement by it's tooltip text (title or alt) or some another
    attribute.
    Available attributes: any
    Available element types without using tag attribute:
    a, span, img, li, h1, h2, h3, h4, h5, h6, div, svg, p, button, input*
    (*submit buttons only).

    Keyword tries to click element until it succeeds or timeout has passed.
    If timeout is not specified, it uses default timeout that can be adjusted
    with DefaultTimeout keyword.

    Examples
    --------
    .. code-block:: robotframework

        ClickItem        Canis

    In the above example the ClickItem keyword will click the word Canis.
    If there are multiple instances of the word Canis on the page, first one
    will be clicked unless 'anchor' is given. You can
    specific which one should be clicked by either:

    - a number or
    - a word that is near to the word Canis

    For example

    .. code-block:: robotframework

        ClickItem    Canis    3     # clicks the third "Canis" on the page
        ClickItem    Canis    Dog   # clicks the "Canis" near to the word "Dog"

    Parameters
    ----------
    text : str
        Text to be clicked.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it.  (default 1)
    timeout : str | int
        How long we wait for element to be ready for click
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    kwargs :
        |  Accepted kwargs:
        |       tag : html tag of preferred element -
        |           If tag is used then element is found
        |           by some of it's attribute
        |       partial_match: False. If only full match is accepted set
        |       partial_match to False.
    """
    web_element = internal_text.get_item_using_anchor(text, anchor, **kwargs)
    if execute_click_and_verify_condition(web_element, timeout=timeout, js=js, **kwargs):
        return


@decorators.timeout_decorator
def verify_item(text, anchor="1", timeout=0, **kwargs):  # pylint: disable=unused-argument
    """Verify Item (usually icon or picture) exist.

    Finds webelement by it's tooltip text (title or alt) or some another
    attribute.
    Available attributes: any
    Available element types without using tag attribute:
    a, span, img, li, h1, h2, h3, h4, h5, h6, div, svg, p, button, input*
    (*submit buttons only)

    Keyword waits until timeout has passed. If timeout is not specified, it
    uses default timeout that can be adjusted with DefaultTimeout keyword.

    VerifyItem does not require for the text to be unique.

    Examples
    --------
    .. code-block:: robotframework

        VerifyItem        Canis

    In the above example the VerifyItem keyword verifies that element which
    has attribute Canis exist.
    If there are multiple instances of such of elements you can
    specific which one is looking for by either:

    - a number or
    - a word that is near to the word Canis

    Parameters
    ----------
    text : str
        Text to be clicked.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long we wait for element to be ready for click
     kwargs :
        |  Accepted kwargs:
        |       tag : html tag of preferred element -
        |           If tag is used then element is found
        |           by some of it's attribute
        |       partial_match: False. If only full match is accepted set
        |       partial_match to False.
    """
    web_element = internal_text.get_item_using_anchor(text, anchor, **kwargs)
    if web_element:
        return


@decorators.timeout_decorator
def verify_no_item(text, anchor="1", timeout=0, **kwargs):  # pylint: disable=unused-argument
    """Verify Item (usually icon or picture) is not exist.

    Finds webelement by it's tooltip text (title or alt) or some another
    attribute.
    Available attributes: any
    Available element types without using tag attribute:
    a, span, img, li, h1, h2, h3, h4, h5, h6, div, svg, p, button, input*
    (*submit buttons only)

    Keyword waits until timeout has passed. If timeout is not specified, it
    uses default timeout that can be adjusted with DefaultTimeout keyword.

    VerifyItem does not require for the attribute to be unique.

    Examples
    --------
    .. code-block:: robotframework

        VerifyNoItem        Canis

    In the above example the VerifyItem keyword verifies that element which
    has attribute Canis is not exist.

    Parameters
    ----------
    text : str
        Attribute value of item.
    anchor : str
        Parameter not used with this kw.
    timeout : str | int
        How long we wait for element to be ready for click
     kwargs :
        |  Accepted kwargs:
        |       tag : html tag of preferred element -
        |           If tag is used then element is found
        |           by some of it's attribute
        |       partial_match: False. If only full match is accepted set
        |       partial_match to False.
    """
    kwargs['allow_non_existent'] = True
    web_element = internal_text.get_item_using_anchor(text, anchor, **kwargs)
    if not web_element:
        return
    raise QWebValueError('Element with attribute value {} still exists'.format(text))


@decorators.timeout_decorator
def scroll_text(text, anchor="1", timeout=0, **kwargs):
    """Scroll page until text is on top.

    Finds text on page and scrolls until it is on top. This is used with visual testing
    tools to align page properly.

    Keyword tries to scroll to element until it succeeds or timeout has passed.
    If timeout is not specified, it uses default timeout that can be adjusted
    with DefaultTimeout keyword.

    Examples
    --------
    .. code-block:: robotframework

        ScrollText       Address
        ScrollText       Address    Billing
    """
    web_element = internal_text.get_element_by_locator_text(text, anchor, **kwargs)
    scroll(web_element, timeout=timeout)


def write_text(text):
    """Type text with single-character keys.

    Parameters
    ----------
    text : str
        Text to type.

    Examples
    --------
    .. code-block:: robotframework

        WriteText    Hello World!
    """
    if CONFIG.get_value("Headless") or os.getenv('QWEB_HEADLESS', None):
        raise QWebEnvironmentError(
            'Running in headless environment. Pynput is unavailable.')
    keyboard = Controller()
    keyboard.type(text)


@decorators.timeout_decorator
def verify_texts(texts_to_verify, timeout=0):
    r"""*DEPRECATED!!* Use keyword `VerifyAll` instead."""
    logger.warn(r"""*DEPRECATED!!* Use keyword `VerifyAll` instead.""")
    if isinstance(texts_to_verify, list):
        for text in texts_to_verify:
            logger.info('Verifying text "{}".'.format(text), also_console=True)
            verify_text(text, timeout)
    elif texts_to_verify.endswith('.txt'):
        file = download.get_path(texts_to_verify)
        with open(file, 'rb') as txt_file:
            clean_data = [line.rstrip() for line in txt_file]
            for x in clean_data:
                x = x.decode('utf-8')
                logger.info('Verifying text "{}".'.format(x), also_console=True)
                verify_text(x, timeout)
    else:
        texts = texts_to_verify.split(',')
        for text in texts:
            clean_text = text.strip()
            logger.info('Verifying text "{}".'.format(clean_text), also_console=True)
            verify_text(clean_text, timeout)


@decorators.timeout_decorator
def verify_any(texts_to_verify, timeout=0):
    """Verify any of the given texts.

    Verify that at least one of the texts is found. Useful for handling
    session dependent states, such as logins or popups.

    Other Parameters
    ----------------
    <other_parameters>

    Examples
    --------
    .. code-block:: robotframework

        VerifyAny    Login    Front Page

        # Follow up to check which state
        ${login}=    IsText       Login
    """
    if isinstance(texts_to_verify, list):
        for text in texts_to_verify:
            logger.info('Verifying text "{}".'.format(text), also_console=True)
            if is_text(text, timeout):
                return text

        raise QWebValueError('Could not find any of the texts: '
                             f'{texts_to_verify}')

    if texts_to_verify.endswith('.txt'):
        file = download.get_path(texts_to_verify)
        with open(file, 'rb') as txt_file:
            clean_data = [line.rstrip() for line in txt_file]
            for x in clean_data:
                x = x.decode('utf-8')
                if is_text(x, timeout):
                    return x

            raise QWebValueError('Could not find any of the texts: '
                                 f'{clean_data}')

    else:
        texts = texts_to_verify.split(',')
        for text in texts:
            clean_text = text.strip()
            logger.info('Verifying text "{}".'.format(clean_text), also_console=True)
            if is_text(clean_text, timeout):
                return clean_text

        raise QWebValueError('Could not find any of the texts: '
                             f'{texts}')


@decorators.timeout_decorator
def verify_all(texts_to_verify, timeout=0):
    """Verify page contains given texts.

    The texts should be separated with a comma.

    Also accepts a .txt file or Robot FW list as a parameter. Each row in the text file will be
    verified, or each item in the Robot FW list.

    Examples
    --------
    .. code-block:: robotframework

        VerifyTexts      Cat, Mouse, Dog, Lion, iddqd66402
        VerifyTexts      list_of_cats.txt
        VerifyTexts      C:/Users/pace/Desktop/textfile.txt

        ${cool_list}=    Create List    Cat    Mouse    Dog    Lion    iddqd66402
        VerifyTexts      ${cool_list}
    """
    if isinstance(texts_to_verify, list):
        for text in texts_to_verify:
            logger.info('Verifying text "{}".'.format(text), also_console=True)
            verify_text(text, timeout)
    elif texts_to_verify.endswith('.txt'):
        file = download.get_path(texts_to_verify)
        with open(file, 'rb') as txt_file:
            clean_data = [line.rstrip() for line in txt_file]
            for x in clean_data:
                x = x.decode('utf-8')
                logger.info('Verifying text "{}".'.format(x), also_console=True)
                verify_text(x, timeout)
    else:
        texts = texts_to_verify.split(',')
        for text in texts:
            clean_text = text.strip()
            logger.info('Verifying text "{}".'.format(clean_text), also_console=True)
            verify_text(clean_text, timeout)


@decorators.timeout_decorator
def scroll_to(text_to_find, locator=None, anchor='1', scroll_length=None,
              timeout=120, **kwargs):  # pylint: disable=unused-argument
    """Scroll a dynamic web page or scrollbar.

    Parameters
    ----------
    text_to_find : str
        Text to find by scrolling a page or an element.
    locator : str
        Locator text for a scrollable element.
    anchor : str
        Anchor used for the locator.
    scroll_length : str
        Amount of pixels per one scroll.
    timeout : int
        How long to scroll in seconds, before timing out.

    Examples
    --------
    .. code-block:: robotframework

        ScrollTo       Cat

    In the above example, the web page is scrolled until the text "Cat" is found.

    .. code-block:: robotframework

        ScrollTo       Cat      scroll_length=2000

    In the above example, the web page is scrolled 2000 pixels per scroll, until the text "Cat" is
    found.

    .. code-block:: robotframework

        ScrollTo       Cat      List of cats

    In the above example, a scrollbar located by a text "List of cats", is scrolled until the text
    "Cat" is found.

    .. code-block:: robotframework

        ScrollTo       Cat      List of cats    scroll_length=2000

    In the above example, a scrollbar located by a text "List of cats", is scrolled 2000 pixels
    per scroll until the text "Cat" is found.
    """
    visible = is_text(text_to_find)
    if visible:
        scroll_text(text_to_find)
        return
    slow_mode = util.par2bool(kwargs.get('slow_mode', False))
    if locator:  # If we are trying to scroll a specific element
        scroll_first_scrollable_parent_element(
            locator, anchor, text_to_find, scroll_length, slow_mode, timeout)
    else:  # if we are just scrolling the web page
        scroll_dynamic_web_page(text_to_find, scroll_length, slow_mode, timeout)


def copy_text(text):
    """Perform a copy.

    Copies whatever is active at the UI to the clipboard. If text is
    provided copies that to the clipboard.

    Parameters
    ----------
    text : str, optional
        Text to copy to the clipboard

    Examples
    --------
    .. code-block:: robotframework

        # Copy the provided text
        CopyText        text to clipboard

    """
    pyperclip.copy(text)


def click_while(text_to_disappear, text_to_click=None, anchor="1", timeout=0, interval=None,
                parent=None, child=None, js=False, **kwargs):
    """Click text until a text or element disappears.

    This keyword is required on slow pages where it takes time for a button
    listener to start. This clicks button and waits until certain text or
    element disappears.

    If text_to_disappear is not entered, keyword will wait until clicked text disappears.

    For example

    .. code-block:: robotframework

        # If text to disappear is same as clickable text. ClickText Cart while it exists:
        ClickWhile    Cart
        # ClickText Button while text Cart exists. Timeout after 5s:
        ClickWhile    Cart          Button          1    5s
        # ClickText Cart contents while element with attr some_attr exists:
        ClickWhile    some_attr     Cart contents   element=True
        # ClickText Go to cart once/second while text Cart exists:
        ClickWhile    Cart    Go to cart      interval=1s

    Parameters
    ----------
    text_to_disappear : str
        Text that appears after click
    text_to_click : str
        Text to be clicked.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long to button is clicked if text has not disappeared
    interval : str
       Interval between clicks until element disappears (default=5s)
    parent : str
        tag name for clickable parent.
    child : str
        tag name for clickable child.
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    Accepted kwargs:
        element=True: Use this if element is expected to disappear instead of visible text
        css=False/off: Use this to bypass css search when finding elements
        by visible text
        tag=html tag: Use this if element to disappear is not default type of item element.
        force_click=True: Use this to bypass checks (istext/isnotext) before click.
    """
    el = util.par2bool(kwargs.get('element', False))
    forced = util.par2bool(kwargs.get('force_click', False))
    if not forced:
        if not text_to_click:
            text_to_click = text_to_disappear
        if el:
            try:
                verify_item(text_to_disappear, timeout=timeout, **kwargs)
            except QWebElementNotFoundError:
                raise QWebValueError('Element to disappear is not visible before click.')
        elif not is_text(text_to_disappear, timeout):
            raise QWebValueError('Text to disappear is not visible before click.')
    try:
        _retry_while(text_to_click, text_to_disappear, anchor, timeout, interval,
                     parent, child, js, **kwargs)
    except QWebElementNotFoundError as orig_err:
        err = CONFIG.get_value('RetryError')
        CONFIG.reset_value('RetryError')
        raise err or orig_err


def click_until(text_to_appear, text_to_click, anchor="1", timeout=0, interval=None,
                parent=None, child=None, js=False, **kwargs):
    """Click text until a text appears.

    This keyword is required on slow pages where it takes time for a button
    listener to start. This clicks button and waits until text appears.
    Keyword is also handful in situations where we are waiting for some process
    to be ready and there is some button to press for getting results

    For example

    .. code-block:: robotframework

        # ClickText Get Data until Order 1234 exists on page:
        ClickUntil      Order 1234         Get Data
        # ClickText Update until there is text Process finished available.
        # Wait eight seconds between clicks:
        ClickUntil      Process finished   Update      interval=8s
        # ClickText Add near to text Main Cart until there is 10 items in carts.
        # Timeout after 20 seconds if attempts are unsuccessful. Interval 1 second:
        ClickUntil      10 items            Add    Main Cart     20s   1s
        # ClickText Submit until element with attr confirm_box appears
        ClickUntil      confirm_box         Submit    element=True

    Parameters
    ----------
    text_to_appear : str
        Text that appears after click
    text_to_click : str
        Text to be clicked.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long button is clicked if text does not appear
    interval : str
        Interval between clicks until element disappears (default=5s)
    parent : str
        tag name for clickable parent.
    child : str
        tag name for clickable child.
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    Accepted kwargs:
        element=True: Use this if element is expected to disappear instead of visible text
        css=False/off: Use this to bypass css search when finding elements
        by visible text
        tag=html tag: Use this if element to disappear is not default type of item element.
        force_click=True: Use this to bypass checks (istext/isnotext) before click.
    """
    el = util.par2bool(kwargs.get('element', False))
    forced = util.par2bool(kwargs.get('force_click', False))
    if not forced:
        if el:
            try:
                verify_no_item(text_to_appear, **kwargs)
            except QWebValueError:
                raise QWebValueError('Element to appear is already visible.')
        elif not is_no_text(text_to_appear):
            raise QWebValueError('Text to appear is already visible.')
    try:
        _retry_until(text_to_click, text_to_appear, anchor, timeout, interval,
                     parent, child, js, **kwargs)
    except QWebElementNotFoundError as orig_err:
        err = CONFIG.get_value('RetryError')
        CONFIG.reset_value('RetryError')
        raise err or orig_err


def click_item_while(text_to_disappear, locator=None, anchor="1", timeout=0,
                     interval=None, js=False, **kwargs):
    """Click Item until a text or element disappears.

    This keyword is required on slow pages where it takes time for a button
    listener to start. This clicks button and waits until certain text or
    element disappears.

    If text_to_disappear is not entered, keyword will wait until clicked element disappears.

    For example

    .. code-block:: robotframework

        # If element to disappear is same as clickable item. ClickItem with Add attribute
        # while it exists:
        ClickItemWhile    Add      element=True
        # ClickItem add while text Empty Cart exists. Timeout after 5s:
        ClickItemWhile    Empty Cart         Add           5s
        # ClickItem Cart contents while h1 type element with attr some_attr exists:
        ClickItemWhile    some_attr     Cart contents   element=True  tag=h1
        # ClickItem Go to cart once/second while text Cart exists:
        ClickItemWhile    Cart    Go to cart      interval=1s

    Parameters
    ----------
    text_to_disappear : str
        Text that appears after click
    locator : str
        Some attr value to locate element.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long to button is clicked if text has not disappeared
    interval : str
        Interval between clicks until element disappears (default=5s)
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    Accepted kwargs:
        element=True: Use this if element is expected to disappear instead of visible text
        css=False/off: Use this to bypass css search when finding elements
        by visible text
        tag=html tag: Use this if element to disappear is not default type of item element.
        force_click=True: Use this to bypass checks (istext/isnotext) before click.
    """
    kwargs['item'] = True
    el = kwargs.get('element', False)
    forced = util.par2bool(kwargs.get('force_click', False))
    if not forced:
        if not locator:
            locator = text_to_disappear
        if el:
            try:
                verify_item(text_to_disappear, timeout=timeout, **kwargs)
            except QWebElementNotFoundError:
                raise QWebValueError('Element to disappear is not visible before click.')
        elif not is_text(text_to_disappear, timeout):
            raise QWebValueError('Text to disappear is not visible before click.')
    try:
        _retry_while(locator, text_to_disappear, anchor, timeout, interval, js=js, **kwargs)
    except QWebElementNotFoundError as orig_err:
        err = CONFIG.get_value('RetryError')
        CONFIG.reset_value('RetryError')
        raise err or orig_err


def click_item_until(text_to_appear, locator, anchor="1", timeout=0,
                     interval=None, js=False, **kwargs):
    """Click text until a text appears.

    This keyword is required on slow pages where it takes time for a button
    listener to start. This clicks button and waits until text appears.
    Keyword is also handful in situations where we are waiting for some process
    to be ready and there is some button to press for getting results

    For example

    .. code-block:: robotframework

        # ClickItem submit until Order 1234 exists on page:
        ClickItemUntil     Order 1234         submit
        # ClickItem counter once/second until text Done appears.
        ClickItemUntil     Done                counter      interval=1s
        # ClickItem ++ near to text Main Cart until there is 10 items in carts.
        ClickItemUntil     10 items            ++    Main Cart     20s   1s
        # ClickItem save until element with attr confirm_box appears
        ClickItemUntil     confirm_box         save    element=True

    Parameters
    ----------
    text_to_appear : str
        Text that appears after click
    locator : str
        Some attr value to locate element.
    anchor : str
        Text near the element to be clicked or index. If the page contains many
        places where the text argument is then anchor is used to get the
        one that is closest to it. (default 1)
    timeout : str | int
        How long button is clicked if text does not appear
    interval : str
        Interval between clicks until element disappears (default=5s)
    js : boolean
        If set to true, uses javascript instead of selenium to click element.
    Accepted kwargs:
        element=True: Use this if element is expected to disappear instead of visible text
        css=False/off: Use this to bypass css search when finding elements
        by visible text
        tag=html tag: Use this if element to disappear is not default type of item element.
        force_click=True: Use this to bypass checks (istext/isnotext) before click.
    """
    kwargs['item'] = True
    el = kwargs.get('element', False)
    forced = util.par2bool(kwargs.get('force_click', False))
    if not forced:
        if el:
            try:
                verify_no_item(text_to_appear, **kwargs)
            except QWebValueError:
                raise QWebValueError('Element to appear is already visible.')
        elif not is_no_text(text_to_appear):
            raise QWebValueError('Text to appear is already visible.')
    try:
        _retry_until(locator, text_to_appear, anchor, timeout, interval, js=js, **kwargs)
    except QWebElementNotFoundError as orig_err:
        err = CONFIG.get_value('RetryError')
        CONFIG.reset_value('RetryError')
        raise err or orig_err


@decorators.timeout_decorator
def _retry_while(text, text_to_disappear, anchor, timeout, interval,  # pylint: disable=unused-argument
                 parent=None, child=None, js=False, **kwargs):
    if not interval:
        interval = CONFIG['RetryInterval']
    item = kwargs.get('item', False)
    el = kwargs.get('element', False)
    try:
        if item:
            click_item(text, anchor, interval, js, **kwargs)
        else:
            click_text(text, anchor, interval, parent, child, js, **kwargs)
    except (QWebElementNotFoundError, QWebDriverError, QWebValueError) as e:
        CONFIG.set_value('RetryError', e)
        logger.info('Got {} from click part. Action probably triggered'.format(e))
    try:
        if el:
            verify_no_item(text_to_disappear, timeout=interval, **kwargs)
        else:
            verify_no_text(text_to_disappear, timeout=interval)
    except QWebValueError as e:
        logger.info('Got {} from verify part.'.format(e))
        CONFIG.set_value('RetryError', e)
        raise e


@decorators.timeout_decorator
def _retry_until(text, text_to_appear, anchor, timeout, interval,  # pylint: disable=unused-argument
                 parent=None, child=None, js=False, **kwargs):
    if not interval:
        interval = CONFIG['RetryInterval']
    item = kwargs.get('item', False)
    el = kwargs.get('element', False)
    try:
        if item:
            click_item(text, anchor, interval, js, **kwargs)
        else:
            click_text(text, anchor, interval, parent, child, js, **kwargs)
    except (QWebElementNotFoundError, QWebDriverError, QWebValueError) as e:
        CONFIG.set_value('RetryError', e)
        logger.info('Got {} from click part. Action probably triggered'.format(e))
    try:
        if el:
            verify_item(text_to_appear, timeout=interval, **kwargs)
        else:
            verify_text(text_to_appear, timeout=interval)
    except QWebElementNotFoundError as e:
        logger.info('Got {} from verify part.'.format(e))
        CONFIG.set_value('RetryError', e)
        raise e
