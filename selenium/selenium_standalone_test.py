#! /usr/bin/env python

import logging
import os
import sys
import time

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

logging.basicConfig(format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(threadName)s: %(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%S",
                    level=logging.INFO,
                    stream=sys.stdout)


def save_screenshot(driver, file_name, msg=''):
    screenshot_dir = '/src/screenshot'
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, file_name)
    ret = driver.get_screenshot_as_file(screenshot_path)
    if ret:
        logger.info('Save %s at "%s"', msg, screenshot_path)


def test_title_in_google(driver):
    driver.get('http://www.google.com')
    logger.info('Test Google.com title')
    assert 'Google' in driver.title
    save_screenshot(driver, 'google', msg='Google Homepage')
    logger.info('Test Pass')


def test_title_in_python_org(driver):
    driver.get('http://www.python.org')
    logger.info('Test python.org title')
    assert 'Python' in driver.title
    save_screenshot(driver, 'python', msg='Python Homepage')
    logger.info('Test Pass')


def test_search_applatix(driver):
    is_firefox = bool(driver.capabilities.get('browserName', '').lower() == 'firefox')
    wait = WebDriverWait(driver, 30)

    logger.info('Go to www.google.com')
    driver.get('http://www.google.com')
    if is_firefox:
        time.sleep(3)

    logger.info('Search for "applatix"')
    elem = driver.find_element_by_name('q')
    elem.send_keys('applatix')
    elem.send_keys(Keys.RETURN)

    if is_firefox:
        logger.info('Test Pass')
        save_screenshot(driver, 'applatix', msg='Applatix')
        return

    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Applatix')))
    logger.info('Go to Applatix Homepage')
    applatix_elem = driver.find_element_by_partial_link_text('Applatix')
    applatix_elem.click()
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'About')))

    logger.info('Go to Applatix About page')
    about_elem = driver.find_element_by_partial_link_text('About')
    about_elem.click()

    logger.info('Search Applatix Mission')
    mission_selector = '#u11931'
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, mission_selector)))

    try:
        mission_elem = driver.find_element_by_css_selector(mission_selector)
        mission = mission_elem.text.strip()
        if not mission:
            save_screenshot(driver, 'failure', msg='failure')
            logger.info('Test Fail')
            return
        else:
            logger.info('Applatix Inc. Mission: " %s "', mission)
    except Exception:
        save_screenshot(driver, 'failure', msg='failure')
        logger.info('Test Failure')
        return

    save_screenshot(driver, 'applatix', msg='Applatix')
    logger.info('Test Pass')
