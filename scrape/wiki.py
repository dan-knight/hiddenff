from scrape.base import RequestsScraper, SeleniumScraper, driver

from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import json
import re


class PlayerListScraper(SeleniumScraper):
    pass

    def interact_with_page(self):
        super().wait_for_condition(cond.presence_of_element_located(
            (By.CLASS_NAME, 'mw-category')
        ))

    def get_links(self, full_name):
        player_links = []
        container = self.soup.find('div', attrs={'class': 'mw-category'})

        try:
            a = container.find_all('a', text=re.compile(full_name))
            player_links = [prepend_link(link['href']) for link in a]
        except TypeError:
            self.add_error('player_link')

        self.data['player_links'] = player_links


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


def get_player_links(first, last, position):
    positions = {
        'RB': 'running_backs',
        'WR': 'wide_receivers',
        'QB': 'quarterbacks',
        'TE': 'tight_ends'
    }

    def format_position_url():
        position_suffix = positions.pop(position)
        print(positions)
        last_name_suffix = last[0]
        return 'https://en.wikipedia.org/wiki/Category:American_football_%s?from=%s' % \
               (position_suffix, last_name_suffix)

    scraper = PlayerListScraper(format_position_url())
    full_name = '%s %s' % (first, last)
    scraper.get_links(full_name)
    print(scraper.data)


# Utilities
with open('./scrape/error/wiki.json') as file:
    errors = json.load(file)


def prepend_link(link):
    return 'https://en.wikipedia.org' + link




