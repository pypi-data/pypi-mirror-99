#!/usr/bin/env python
from selenium.webdriver import PhantomJS
from selenium.webdriver.phantomjs.webdriver import WebDriver

class ACMEBrowser(object):
    """
    DESCRIPTION
    -----------
    Wrapper class that calls PhantomJS browser
    """

    def __init__(self):
        self.url: str = ""
        self.driver = None

    def __browser__(self, url: str):
        try:
            self.driver.get(url=url)
            return self.driver

        except ConnectionError as e:
            raise ConnectionError(f"Unable to connect to the following URLs {url}") from e

    def browser(self, url: str) -> WebDriver:
        if not url:
            raise ValueError(f"Please provide the right URL.")

        self.url = url
        try:
            self.driver = PhantomJS()

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Unable to find phantomjs binary") from e

        else:
            return self.__browser__(url=self.url)