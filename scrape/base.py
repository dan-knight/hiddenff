import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException

from bs4 import BeautifulSoup


class Scraper(object):
    def __init__(self, url):
        print(url)
        self.data = {'errors': set(),
                     'url': url}
        self.soup = self.get_soup()

    def get_soup(self):
        try:
            return BeautifulSoup(self.get_html(), 'html.parser')
        except TypeError:
            return None

    def get_html(self):
        return ''

    def add_error(self, error_name):
        self.data['errors'].add(error_name)


class RequestsScraper(Scraper):
    def __init__(self, url):
        super(RequestsScraper, self).__init__(url)

    def get_html(self):
        try:
            return requests.get(self.data['url']).content
        except requests.exceptions.MissingSchema:
            return None


class SeleniumScraper(Scraper):
    def __init__(self, url):
        super(SeleniumScraper, self).__init__(url)

    def get_html(self):
        self.setup_page()
        return driver.page_source

    def setup_page(self):
        try:
            driver.get(self.data['url'])
            self.__class__.interact_with_page(self)
        except (TimeoutException, ElementNotInteractableException):
            restart_driver()
            driver.get(self.data['url'])
            self.__class__.interact_with_page(self)

    def interact_with_page(self):
        pass

    @staticmethod
    def wait_and_click_loop(how_to_find):
        while True:
            try:
                element = SeleniumScraper.wait_for_condition(cond.element_to_be_clickable(how_to_find))
                SeleniumScraper.click(element)
            except (TimeoutException, StaleElementReferenceException):
                break

    @staticmethod
    def find_all_and_click(how_to_find):
        find_by, find_value = how_to_find
        elements = driver.find_elements(find_by, find_value)

        for element in elements:
            element.click()

    @staticmethod
    def wait_for_condition(condition, timeout=10):
        return WebDriverWait(driver, timeout).until(condition)

    @staticmethod
    def js_click(element):
        driver.execute_script("arguments[0].click();", element)


driver = webdriver.Firefox()


def restart_driver():
    global driver
    driver.close()
    driver = webdriver.Firefox()
