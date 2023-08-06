import logging
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from QWeb.internal import browser, util
from QWeb.internal.config_defaults import CONFIG
from robot.api import logger

LOGGER = logging.getLogger(__name__)

NAMES = ["firefox", "ff"]


def open_browser(profile_dir=None,
                 capabilities=None,
                 proxy=None,
                 headless=False,
                 binary=None,
                 executable_path="geckodriver",
                 firefox_args=None,
                 timeout=30,
                 log_path="geckodriver.log",
                 **kwargs):
    """Open Firefox browser and cache the driver.

    Parameters
    ----------
    binary : FirefoxBinary or str
        If string then is needs to be the absolute path to the binary. If
        undefined, the system default Firefox installation will be used.
    timeout : int
        Time to wait for Firefox to launch when using the extension connection.
    capabilities : dict
        Dictionary of desired capabilities.
    executable_path : str (Default geckodriver)
        Full path to override which geckodriver binary to use for Firefox
        47.0.1 and greater, which defaults to picking up the binary from the
        system path.
    log_path : str (Default "geckdriver.log")
        Where to log information from the driver.
    firefox_args : list
        Optional arguments to modify browser settings.
        https://developer.mozilla.org/en-US/docs/Mozilla/Command_Line_Options
    """
    options = Options()
    if headless:
        logger.warn('Deprecated.\n'
                    'Headless mode can be activated just like any other firefox option:\n'
                    '"OpenBrowser   https://qentinel.com    ${BROWSER}   -headless"')
        options.add_argument('-headless')
        CONFIG.set_value("Headless", True)
    if profile_dir:
        logger.warn('Deprecated.\n'
                    'Profile directory can be selected like any other firefox option:\n'
                    '"OpenBrowser   https://qentinel.com   ${BROWSER}  -profile /path/to/profile"')
        options.add_argument('-profile {}'.format(profile_dir))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", browser.MIME_TYPES)
    options.set_preference("extensions.update.enabled", False)
    options.set_preference("app.update.enabled", False)
    options.set_preference("app.update.auto", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("privacy.socialtracking.block_cookies.enabled", False)
    kwargs = {k.lower(): v for k, v in kwargs.items()}  # Kwargs keys to lowercase
    if 'prefs' in kwargs:
        if isinstance(kwargs.get('prefs'), dict):
            prefs = kwargs.get('prefs')
        else:
            prefs = util.prefs_to_dict(kwargs.get('prefs').strip())
        for item in prefs.items():
            key, value = item[0], item[1]
            logger.info('Using prefs: {} = {}'.format(key, value), also_console=True)
            if not isinstance(value, int) and value.isdigit():
                value = int(value)
            options.set_preference(key, value)
    if firefox_args:
        if any('headless' in _.lower() for _ in firefox_args):
            CONFIG.set_value("Headless", True)
        for option in firefox_args:
            option = option.strip()
            options.add_argument(option)
    driver = webdriver.Firefox(executable_path=executable_path, proxy=proxy, firefox_binary=binary,
                               desired_capabilities=capabilities, options=options, timeout=timeout,
                               log_path=log_path)
    if os.name == 'nt':  # Maximize window if running on windows, doesn't work on linux
        driver.maximize_window()
    browser.cache_browser(driver)
    return driver
