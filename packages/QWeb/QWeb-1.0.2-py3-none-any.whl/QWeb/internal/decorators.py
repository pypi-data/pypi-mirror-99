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

import time
from inspect import signature
from functools import wraps
from robot.utils import timestr_to_secs
from robot.api import logger
from selenium.common.exceptions import InvalidSelectorException, \
    NoSuchElementException, StaleElementReferenceException, WebDriverException, \
    UnexpectedAlertPresentException, InvalidSessionIdException
from QWeb.keywords import config
from QWeb.internal import frame
from QWeb.internal.config_defaults import CONFIG, SHORT_DELAY, LONG_DELAY
from QWeb.internal.exceptions import QWebElementNotFoundError, \
    QWebStalingElementError, QWebDriverError, QWebTimeoutError, QWebValueError, \
    QWebUnexpectedConditionError, QWebValueMismatchError, QWebSearchingMode, QWebUnexpectedAlert, \
    QWebIconNotFoundError, QWebBrowserError, FATAL_MESSAGES


# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
def timeout_decorator(fn):
    @wraps(fn)
    def get_elements_from_dom_content(*args, **kwargs):
        try:
            args, kwargs, locator = _equal_sign_handler(args, kwargs, fn)
            msg = None
            params = signature(fn).parameters
            args, kwargs = _args_to_kwargs(params, args, kwargs)
            timeout = get_timeout(**kwargs)
            logger.debug('Timeout is {} sec'.format(timeout))

            try:
                if 'go_to' not in str(fn) and 'switch_window' not in str(fn):
                    frame.wait_page_loaded()
            except UnexpectedAlertPresentException as e:
                if not CONFIG["HandleAlerts"]:
                    raise QWebUnexpectedAlert(str(e))
                logger.debug('Got {}. Trying to retry..'.format(e))
                time.sleep(SHORT_DELAY)
            start = time.time()
            while time.time() < timeout + start:
                try:
                    kwargs['timeout'] = float(timeout + start - time.time())
                    config.set_config('FrameTimeout', float(timeout + start - time.time()))
                    return fn(*args, **kwargs)
                except (QWebUnexpectedConditionError, QWebTimeoutError) as e:
                    logger.warn('Got {}'.format(e))
                except (InvalidSelectorException, NoSuchElementException,
                        QWebElementNotFoundError, UnexpectedAlertPresentException,
                        QWebStalingElementError, StaleElementReferenceException,
                        QWebIconNotFoundError) as e:
                    time.sleep(SHORT_DELAY)
                    logger.debug('Got exception: {}. Trying to retry..'.format(e))
                except InvalidSessionIdException:
                    CONFIG.set_value("OSScreenshots", True)
                    raise QWebBrowserError("Browser session lost. Did browser crash?")
                except (WebDriverException, QWebDriverError) as e:
                    if any(s in str(e) for s in FATAL_MESSAGES):
                        CONFIG.set_value("OSScreenshots", True)
                        raise QWebBrowserError(e)
                    logger.info('From timeout decorator: Webdriver exception. Retrying..')
                    logger.info(e)
                    time.sleep(SHORT_DELAY)
                    err = QWebDriverError
                    msg = e
                except QWebValueError as ve:
                    logger.debug('Got QWebValueError: {}. Trying to retry..'.format(ve))
                    err = QWebValueError
                    msg = ve
                    time.sleep(SHORT_DELAY)
            if msg:
                raise err(msg)
            if 'count' in str(fn):
                return 0
            if 'is_text' in str(fn) or 'is_no_text' in str(fn):
                return False
            raise QWebElementNotFoundError(
                'Unable to find element for locator {} in {} sec'.format(locator, timeout))
        except QWebSearchingMode:
            pass

    return get_elements_from_dom_content


def timeout_decorator_for_actions(fn):
    @wraps(fn)
    def perform(*args, **kwargs):
        params = signature(fn).parameters
        args, kwargs = _args_to_kwargs(params, args, kwargs)
        timeout = get_timeout(**kwargs)
        err = None
        msg = None
        performed = False
        logger.debug('time to run {}'.format(timeout))
        start = time.time()
        while time.time() < timeout + start:
            try:
                return fn(*args, **kwargs)
            except QWebValueMismatchError as mismatch:
                if 'text_appearance' not in str(fn) and 'get_or_compare_text' not in str(fn):
                    err = QWebValueError
                    msg = mismatch
                logger.trace('Value mismatch: {}'.format(mismatch))
                continue
            except (QWebElementNotFoundError, UnexpectedAlertPresentException):
                logger.debug('Not found')
                time.sleep(SHORT_DELAY)
            except QWebValueError as ve:
                if performed:
                    break
                raise ve
            except (QWebStalingElementError, StaleElementReferenceException) as S:
                if 'execute_click' in str(fn) or 'text_appearance' in str(fn):
                    logger.info('Got staling element err from retry click.'
                                'Action is probably triggered.')
                    raise QWebUnexpectedConditionError(S)
                raise QWebStalingElementError('Staling element')
            except (WebDriverException, QWebDriverError) as wde:
                if 'alert' in str(fn):
                    time.sleep(LONG_DELAY)
                    logger.info("Got webdriver exception..{}. Retrying..".format(wde))
                    err = QWebDriverError
                    msg = wde
                else:
                    raise QWebDriverError(wde)
        if msg:
            raise err(msg)
        raise QWebTimeoutError('Timeout exceeded')

    return perform


def get_timeout(**kwargs):
    timeout = timestr_to_secs(CONFIG["DefaultTimeout"])
    if 'timeout' in kwargs:
        if timestr_to_secs(kwargs['timeout']) != 0:
            timeout = timestr_to_secs(kwargs['timeout'])
    return timeout


def _args_to_kwargs(params, args, kwargs):
    if 'timeout' not in kwargs:
        for i, p in enumerate(params.values()):
            if p.name not in kwargs:
                if len(args) > i:
                    kwargs[p.name] = args[i]
                else:
                    kwargs[p.name] = p.default
        args = ''
    return args, kwargs


def _equal_sign_handler(args, kwargs, function_name):
    if 'go_to' in str(function_name):
        if kwargs:
            new_args = []
            for k, v in kwargs.items():
                new_args.append(k)
                new_args.append(v)
            args = tuple(["=".join(map(str, new_args))])
            kwargs.clear()
    try:
        locator = args[0]
    except IndexError:
        raise QWebElementNotFoundError("Use \\= instead of = in xpaths")
    return args, kwargs, locator
