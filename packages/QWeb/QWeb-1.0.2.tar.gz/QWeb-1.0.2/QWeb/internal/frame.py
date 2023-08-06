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

import os
import time
from functools import wraps
from robot.api import logger
from robot.utils import timestr_to_secs
from robot.libraries.BuiltIn import BuiltIn
from selenium.common.exceptions import NoSuchWindowException, \
                                       StaleElementReferenceException, \
                                       WebDriverException, InvalidSessionIdException
from QWeb.keywords import config
import QWeb.internal.frame_checker as fc
from QWeb.internal.exceptions import QWebDriverError, QWebElementNotFoundError, \
                                     QWebTimeoutError, QWebBrowserError, FATAL_MESSAGES
from QWeb.internal import xhr, browser
from QWeb.internal.config_defaults import CONFIG


def wait_page_loaded():
    """Wait for webpage to be loaded.

    Examples
    --------
    .. code-block:: robotframework

        WaitPageLoaded

    Each keyword should have this in the beginning since it is crucial that
    page has been loaded fully.

    Monkeypatch this method to have different wait.
    """
    if CONFIG["DefaultDocument"]:
        driver = browser.get_current_browser()
        if driver is None:
            raise QWebDriverError("No browser open. Use OpenBrowser keyword"
                                  " to open browser first")
        try:
            driver.switch_to_default_content()
        except InvalidSessionIdException:
            CONFIG.set_value("OSScreenshots", True)
            raise QWebBrowserError("Browser session lost. Did browser crash?")
        except (NoSuchWindowException, WebDriverException) as e:
            logger.warn(
                'Cannot switch to default context, maybe window is closed. Err: {}'.format(e))
            if any(s in str(e) for s in FATAL_MESSAGES):
                CONFIG.set_value("OSScreenshots", True)
                raise QWebBrowserError(e)
            driver.switch_to_default_content()
    timeout = CONFIG['XHRTimeout']
    if timeout.lower() == "none":
        return
    try:
        xhr.wait_xhr(timestr_to_secs(timeout))
    except(WebDriverException, QWebDriverError) as e:
        logger.info('Unable to check AJAX requests due error: {}'.format(e))


def get_raw_html():
    driver = browser.get_current_browser()
    return driver.page_source


def save_source(raw_html, folder, count):
    """Save the html source to a file.

    Parameters
    ----------
    raw_html : str
        Current page source as unicode string.
    folder : str
        The folder where the file is saved
    count : int
        Determine the index of the file. Should use self.html_source_count.

    Returns
    -------
    str
        Filepath to the created file.

    TODO
    ----
    Figure out how to get a page encoding so that writing the html to a
    file has the correct encoding. At the moment assuming it is utf-8.
    """
    filename = "source_{}.html".format(count)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as htmlfile:
        htmlfile.write(raw_html.encode("utf-8"))
    return filepath


def link_source_to_log(count, filepath):
    """Link the source html file to an iframe in Robot Framework log.

    Using tbody tag to hack rf log. This way the content can be on larger
    area to the left.

    Parameters
    ----------
    count : int
        Determine the index of the file. Should use self.html_source_count.
    filepath : str
        Filepath to the html which will be linked in the Robot Framework
        log.

    Todo
    ----
    Replace relative paths in the src and href attributes with the actual
    source. This way we get css properties and icons.

    Works only local log file, implement Jenkins (or some other) in the
    javascript.
    """
    filename = os.path.basename(filepath)
    logger.info('''<tbody>
<a id="sourceLink{0}">{1}</a>
<br />
<iframe id="source{0}" width="1220px" height="650px"></iframe>
<script type="text/javascript">
element = document.getElementById("sourceLink{0}");
var url = window.location.href;
document.getElementById("sourceLink{0}").setAttribute("href", "{2}")
document.getElementById("source{0}").setAttribute("src", "{1}")
</script>
</tbody>'''.format(count, filename, filepath.replace("\\", "\\\\")), html=True)


def get_output_dir():
    return BuiltIn().get_variable_value("${OUTPUT_DIR}")


def get_html_source_count():
    return BuiltIn().get_variable_value("${html_source_count}")


def set_html_source_count(value):
    BuiltIn().set_global_variable("html_source_count", value)


def all_frames(fn):
    """Decorator that takes any func as a parameter.

    search_from_frames is recursive function which goes through
    all found frames until we find our element if that's not in
    main html's dom tree.
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        def search_from_frames(driver=None, current_frame=None):
            keep_frame = kwargs.get('stay_in_current_frame', CONFIG['StayInCurrentFrame'])
            if keep_frame:
                return fn(*args, **kwargs)
            err = None
            if not driver:
                driver = browser.get_current_browser()
                driver.switch_to_default_content()
            if current_frame:
                try:
                    driver.switch_to_frame(current_frame)
                    logger.debug('switching to childframe {}'.format(str(fn)))
                except (StaleElementReferenceException, WebDriverException) as e:
                    logger.warn(e)
                    driver.switch_to_default_content()
                    raise e
            try:
                web_element = fn(*args, **kwargs)
            except QWebElementNotFoundError as e:
                err = e
                web_element = None
            if is_valid(web_element):
                return web_element
            start = time.time()
            timeout = CONFIG['FrameTimeout']
            while time.time() < timeout + start:
                frames = fc.check_frames(driver)
                for frame in frames:
                    web_element = search_from_frames(driver=driver, current_frame=frame)
                    if is_valid(web_element):
                        logger.debug('Found webelement = {}'.format(web_element))
                        return web_element
                    try:
                        driver.switch_to.parent_frame()
                    except WebDriverException as e:
                        driver.switch_to_default_content()
                        raise e
                    config.set_config('FrameTimeout', float(timeout + start - time.time()))
                    logger.trace('Frame timeout: {}'.format(timeout))
                if err:
                    raise err
                return web_element
            driver.switch_to_default_content()
            raise QWebTimeoutError('From frame decorator: Unable to locate element in given time')
        return search_from_frames()
    logger.debug('wrapped = {}'.format(wrapped))
    return wrapped


def is_valid(web_element):
    if web_element and not isinstance(web_element, tuple):
        return True
    if isinstance(web_element, tuple) and any(web_element):
        return True
    return False
