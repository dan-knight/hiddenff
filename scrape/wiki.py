from scrape.base import RequestsScraper, SeleniumScraper, driver

from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import json
import re


class PlayerPageScraper(RequestsScraper):
    def __init__(self, url):
        super().__init__(url)
        self.card = self.soup.find('table', attrs={'class': 'vcard'})

    def get_team(self):
        team_text = ''

        try:
            span = self.card.find('span', attrs={'class': 'org'})
            team_text = span.text
        except AttributeError:
            self.add_error('team')

        self.data['team'] = team_text

    def get_birthdate(self):
        year = ''
        month = ''
        day = ''

        try:
            th = self.card.find('th', text=re.compile('Born'))
            td = th.next_sibling
            span = td.find('span', attrs={'class': 'bday'})
            birthdate_text = span.text

            def split_birthdate():
                split_date = ('', '', '')
                split_text = birthdate_text.split('-')
                try:
                    split_date = (split_text[0], split_text[1], split_text[2])
                except IndexError:
                    self.add_error('birthdate')

                return split_date

            year, month, day = split_birthdate()

        except AttributeError:
            self.add_error('birthdate')

        self.data['birth_year'] = year
        self.data['birth_month'] = month
        self.data['birth_day'] = day


def scrape_player(link):
    scraper = PlayerPageScraper(link)
    scraper.get_team()
    scraper.get_birthdate()
    return scraper.data


# Utilities
with open('./scrape/error/wiki.json') as file:
    errors = json.load(file)


def prepend_link(link):
    return 'https://en.wikipedia.org' + link




