"""
Created on Mar 02, 2021

@author: Siro

"""

import os
import time
import platform

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import \
    expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from atframework.web.common.selenium.taiji import Taiji
from atframework.drivers.drivers_settings import DriversSettings
from atframework.tools.log.config import logger


class Seleniumhq301(Taiji):
    """
    Set environment information while creating instance
    """
    def __init__(self):
        logger.info('[AtLog] ----- init Seleniumhq301')
        self.browser = None

    def __del__(self):
        pass

    def is_linux_system(self):
        return 'Linux' in platform.system()

    def is_windows_system(self):
        return 'Windows' in platform.system()

    def is_mac_system(self):
        return 'Darwin' in platform.system()

    '''
    At first: Open browser, default open browser via firefox.
    '''

    def _open_browser(self, browser_name):
        self.browser = None
        if 'safari' == browser_name:
            browser = webdriver.Safari()
        elif 'chrome' == browser_name:
            if self.is_mac_system() is True:
                # print("current is Mac system")
                # browser = webdriver.Chrome(executable_path=os.path.abspath(os.path.dirname(os.getcwd())) + DriversSettings.LOCAL_MAC_CHROME_DRIVER)
                browser = webdriver.Chrome(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_MAC_CHROME_DRIVER)
            elif self.is_windows_system() is True:
                # print("current is Windows system")
                browser = webdriver.Chrome(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_WINDOWS_CHROME_DRIVER)
            else:
                browser = webdriver.Remote(
                    options=webdriver.ChromeOptions(),
                    command_executor=DriversSettings.REMOTE_CHROME_DRIVER)
                # ,
                # desired_capabilities=DesiredCapabilities.CHROME)
        else:
            if self.is_mac_system() is True:
                browser = webdriver.Firefox(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_MAC_FIREFOX_DRIVER)
            elif self.is_windows_system() is True:
                # print("current is Windows system")
                browser = webdriver.Firefox(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_WINDOWS_FIREFOX_DRIVER)
            else:
                browser = webdriver.Remote(
                    options=webdriver.FirefoxOptions(),
                    command_executor=DriversSettings.REMOTE_FIREFOX_DRIVER)
                # ,
                # desired_capabilities=DesiredCapabilities.FIREFOX)

        self.browser = browser
        return self.browser

    '''
    Finally: Close browser
    '''

    def _close_browser(self):
        if self.browser is not None:
            self.browser.quit()
            self.browser = None
            #             __instance = None
            logger.info('[AtLog] ----- set the browser and instance to None')
        else:
            logger.info('[AtLog] ----- the browser is None')

    '''
    refresh the current page.
    '''

    def _refresh_page(self):
        # self.browser.execute_script("location.reload()")
        self.browser.refresh()

    '''
    click Specific Link By css_selector
    '''

    def _click_link_by_css(self, css_selector):
        self.browser.find_element_by_css_selector(css_selector).click()

    '''
    access website until loading time
    '''

    def _access_website_till_one_time(self, site_address):
        self.browser.implicitly_wait(15)  # seconds
        self.browser.get(site_address)

    '''
    click Text Field By CSS
    '''

    def _type_in_text_field_by_css(self, field_css, input_text):
        elem = self.browser.find_element_by_css_selector(field_css)
        elem.send_keys(input_text)

    '''
    click Specific button by CSS and javascript
    @param element - css_selector
    '''

    def _click_element_by_locator_script(self, css_selector):
        element = self.browser.find_element_by_css_selector(css_selector)
        self.browser.execute_script("arguments[0].click()", element)

    '''
    click element by locator
    @param element - text, locator
    '''

    def _click_element_by_locator(self, css_selector):
        self.browser.find_element_by_css_selector(css_selector).click()

    '''
    find Specific Link By css
    '''

    def _find_link_by_css(self, css_selector):
        try:
            if self.browser.find_element_by_css_selector(
                    css_selector).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    Click Element By XPath
    @param element - text, XPath
    '''

    def _click_element_by_xpath(self, xpath):
        self.browser.find_element_by_xpath(xpath).click()

    '''
    wait for id shown and sleep 2s.
    @param element - id_name, wait_time, sleep_time
    '''

    def _wait_for_id_shown_and_sleep_2s(self,
                                        id_name,
                                        wait_time=60,
                                        sleep_time=2):
        WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((By.ID, id_name)))
        time.sleep(sleep_time)

    '''
    pause by time.sleep method
    @param - wait_seconds
    '''

    def _pause(self, wait_seconds):
        time.sleep(wait_seconds)

    '''
    wait for css shown and sleep default 5s.
    @param element - css_selector, wait_time, sleep_time
    '''

    def _wait_for_css_shown_and_sleep(self,
                                      css_selector,
                                      wait_time=60,
                                      sleep_time=5):
        WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        time.sleep(sleep_time)

    '''
    Wait for xpath shown and sleep default 5s.
    @param element - xpath, wait_time, sleep_time
    '''

    def _wait_for_xpath_shown_and_sleep(self,
                                        xpath,
                                        wait_time=60,
                                        sleep_time=5):
        WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(sleep_time)

    '''
    Wait 2 mins for xpath shown and sleep default 2s.
    @param element - xpath, wait_time, sleep_time
    '''

    def _wait_for_xpath_shown2_and_sleep(self,
                                         xpath,
                                         wait_time=120,
                                         sleep_time=2):
        # WebDriverWait(self.browser, wait_time).until(lambda x: x.find_element_by_xpath(xpath))
        element = WebDriverWait(
            self.browser,
            wait_time).until(lambda x: x.find_element_by_xpath(xpath))
        time.sleep(sleep_time)
        if element:
            return True
        else:
            return False

    '''
    Wait for CSS shown and click.
    @param element -  wait_time, CSS
    '''

    def _wait_for_css_shown_and_click(self, css_selector, wait_time=60):
        self.browser.implicitly_wait(wait_time)
        self.browser.find_element_by_css_selector(css_selector).click()

    '''
    Get elements's URL By Text
    @param element - link_text
    '''

    def _get_element_url_by_text(self, link_text):
        return self.browser.find_element_by_link_text(link_text).get_attribute(
            "href")

    '''
    find Specific Link By Text
    '''

    def _find_link_by_text(self, link_text):
        try:
            if self.browser.find_element_by_link_text(
                    link_text).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    click Text Field By XPath and click Enter on keyborad
    '''

    def _type_in_text_field_by_xpath_and_click_enter(self, field_xpath,
                                                     input_text):
        elem = self.browser.find_element_by_xpath(field_xpath)
        elem.send_keys(input_text, Keys.ENTER)