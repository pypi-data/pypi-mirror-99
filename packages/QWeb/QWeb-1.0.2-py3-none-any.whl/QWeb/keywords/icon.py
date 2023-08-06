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

import pyautogui
from QWeb.internal import icon, decorators, screenshot, util, text, element
from QWeb.internal.exceptions import QWebElementNotFoundError, QWebIconNotFoundError
from PIL import Image
from robot.api import logger
import io
import os


@decorators.timeout_decorator
def click_icon(image, template_res_w=1920, browser_res_w=1920,
               timeout=0):  # pylint: disable=unused-argument
    """Click the icon on the screen.

    In case you want to click icons you always have to have reference images.

    If reference picture are not in default folders (images, files, downloads) then
    BASE_IMAGE_PATH should be defined in a robot file before using this keyword

    Examples
    --------
    .. code-block:: robotframework

        *** Variables ***
        ${BASE_IMAGE_PATH}          ${CURDIR}${/}..${/}resources${/}images

    BASE_IMAGE_PATH should lead to the folder where all your reference icons are

    .. code-block:: robotframework

        ClickIcon                   plane

    """
    template_res_w, browser_res_w = int(template_res_w), int(browser_res_w)
    image_path = icon.get_full_image_path(image)
    x, y = icon.image_recognition(image_path, template_res_w, browser_res_w, pyautog=True)
    if x == -1:
        raise QWebElementNotFoundError("Couldn't find the icon from the screen")
    pyautogui.moveTo(x, y)
    pyautogui.click()


def is_icon(image, template_res_w=1920, browser_res_w=1920):
    """Check is the icon on the screen.

    In case you want to use this keyword you always have to have reference images.
    If reference image are not in default folders (images, files, downloads) then
    BASE_IMAGE_PATH should be defined in a robot file before using this keyword.

    Examples
    --------
    .. code-block:: robotframework

        *** Variables ***
        ${BASE_IMAGE_PATH}          ${CURDIR}${/}..${/}resources${/}images

    BASE_IMAGE_PATH should lead to the folder where all your reference icons are

    .. code-block:: robotframework

        ${status}                   IsIcon                   plane

    ${status} will be True or False.

    """
    template_res_w, browser_res_w = int(template_res_w), int(browser_res_w)
    image_path = icon.get_full_image_path(image)
    x, _y = icon.image_recognition(image_path, template_res_w, browser_res_w, pyautog=False)
    if x == -1:
        return False
    return True


@decorators.timeout_decorator
def verify_icon(image, template_res_w=1920, browser_res_w=1920,
                timeout=0):  # pylint: disable=unused-argument
    """Verify page contains icon.

    In case you want to use this keyword you always have to have reference images.
    If reference image are not in default folders (images, files, downloads) then
    BASE_IMAGE_PATH should be defined in a robot file before using this keyword.

    Examples
    --------
    .. code-block:: robotframework

        *** Variables ***
        ${BASE_IMAGE_PATH}          ${CURDIR}${/}..${/}resources${/}images

    BASE_IMAGE_PATH should lead to the folder where all your reference icons are

    .. code-block:: robotframework

        VerifyIcon                   plane
    """
    template_res_w, browser_res_w = int(template_res_w), int(browser_res_w)
    image_path = icon.get_full_image_path(image)
    x, _y = icon.image_recognition(image_path, template_res_w, browser_res_w, pyautog=False)
    if x == -1:
        raise QWebIconNotFoundError("Couldn't find the icon from the screen")
    return True


@decorators.timeout_decorator
def capture_icon(locator, folder='screenshots', filename='screenshot_{}.png',
                 timeout=0, **kwargs):  # pylint: disable=unused-argument
    r"""Take a screenshot of an element.

    Examples
    --------
    .. code-block:: robotframework

        ${some_xpath}=       //*[@value\="Button3"]
        CaptureIcon          ${some_xpath}

        CaptureIcon          Button3
        CaptureIcon          Button3    custom_screenshot_name_123.png
        CaptureIcon          Button3    custom_screenshot_name_123.png      C:/custom/folder/path

    Parameters
    ----------
    locator : str
        Locator for the element we are trying to capture, XPath or attribute value. When using
        XPaths, the equal sign "=" must be escaped with a "\".
    folder : str
        Optional folder path. Default value is the screenshots folder.
    filename : str
        Optional filename.
    timeout : int
        How long we try to find the element for.
    """
    if util.xpath_validator(locator):
        web_element = element.get_unique_element_by_xpath(locator)
    else:
        web_element = text.get_item_using_anchor(locator, anchor='1', **kwargs)
    img = Image.open(io.BytesIO(web_element.screenshot_as_png))
    filepath = os.path.join(screenshot.save_screenshot(filename, folder))
    logger.info('Screenshot path: {}'.format(filepath.replace('\\', '/')), also_console=True)
    img.save(filepath)
    screenshot.log_screenshot_file(filepath)
