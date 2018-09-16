# -*- coding: utf-8 -*-

"""Module for web element(s) extraction with selenium.

Functions:
element_class: extract text content of a web element by class name and returns
it as a string.

elements_class: extract web elements by class name and returns them as a list.

elements_xpath: extract web elements by xpath and returns them as a list.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def element_class(driverwait, drivercrawl, class_name):
    """
    Extract attribute of a web element by class name.

    Arguments:
    driverwait: driver for WebDriverWait
    drivercrawl: driver for find_element_by_class_name
    class_name: class name of web element

    Returns:
    element: text content of the web element as a string
    """
    try:
        WebDriverWait(driverwait, 2).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except (NoSuchElementException, TimeoutException):
        element = None
        return element
    else:
        element = drivercrawl.find_element_by_class_name(class_name).text
        return element


def elements_class(driverwait, drivercrawl, class_name):
    """
    Extract attributes of a web element by class name.

    Arguments:
    driverwait: driver for WebDriverWait
    drivercrawl: driver for find_elements_by_class_name
    class_name: class name of web elements

    Returns:
    elements: web elements as a list
    """
    try:
        WebDriverWait(driverwait, 2).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except (NoSuchElementException, TimeoutException):
        elements = None
        return elements
    else:
        elements = drivercrawl.find_elements_by_class_name(class_name)
        return elements


def elements_xpath(driverwait, drivercrawl, xpath):
    """
    Extract attributes of a web element by class name.

    Arguments:
    driverwait: driver for WebDriverWait
    drivercrawl: driver for find_element_by_xpath
    xpath: xpath of web elements

    Returns:
    elements: web elements as a list
    """
    try:
        WebDriverWait(driverwait, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except (NoSuchElementException, TimeoutException):
        elements = None
        return elements
    else:
        elements = drivercrawl.find_elements_by_xpath(xpath)
        return elements


"""The version number"""
__version__ = "0.1"
