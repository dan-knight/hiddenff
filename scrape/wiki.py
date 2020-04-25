from scrape.base import RequestsScraper, SeleniumScraper, driver

from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import json
import re


class PlayerListScraper(SeleniumScraper):
    def __init__(self, url):
        super().__init__(url)
        self.data['player_links'] = []

        def get_container():
            category = self.soup.find('div', attrs={'class': 'mw-category'})
            return category if category else self.soup.find('div', attrs={'class': 'mw-category-generated'})

        self.container = get_container()

    def interact_with_page(self):
        try:
            super().wait_for_condition(cond.presence_of_element_located(
                (By.CLASS_NAME, 'mw-category')
            ))
        except TimeoutException:
            super().wait_for_condition(cond.presence_of_element_located(
                (By.CLASS_NAME, 'mw-category-generated')
            ))

    def get_links(self, full_name):
        player_links = []

        try:
            a = self.container.find_all('a', text=re.compile(full_name))
            player_links = [prepend_link(link['href']) for link in a]
        except TypeError:
            pass

        self.data['player_links'] = player_links

    def get_next_page_url(self):
        div = self.soup.find('div', id='mw-pages')
        a = div.find('a', text='next page')
        return prepend_link(a['href'])

    def check_last_link(self, last):
        def get_last_player():
            links = self.container.find_all('li')
            li = links[len(links) - 1]
            a = li.find('a')
            name = a.text

            def get_last_name():
                name_no_parenthesis = name.split(' (')[0]
                return name_no_parenthesis.split(' ')[-1]

            return get_last_name()

        last_player = get_last_player()
        return last > last_player


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

    def get_name():
        error_name = errors['player_names'].get(get_full_name(first, last))
        return (error_name['first'], error_name['last']) if error_name else (first, last)

    first_name, last_name = get_name()
    full_name = get_full_name(first_name, last_name)

    def scrape_position(position_suffix):
        def format_url():
            last_name_suffix = last_name[0]
            return 'https://en.wikipedia.org/wiki/Category:American_football_%s?from=%s' % \
                   (position_suffix, last_name_suffix)

        scraper = PlayerListScraper(format_url())

        def scrape_list():
            scraper.get_links(full_name)
            links = scraper.data['player_links']
            return links

        links = scrape_list()

        if not links:
            while scraper.check_last_link(last_name):
                next_page = scraper.get_next_page_url()
                scraper = PlayerListScraper(next_page)
                links = scrape_list()

        return links

    guru_position = positions.pop(position)
    player_links = scrape_position(guru_position)

    if not player_links:
        def scrape_other_positions():
            links = []

            for position_key in positions.keys():
                links = scrape_position(positions[position_key])

                if links:
                    break

            return links

        player_links = scrape_other_positions()

    return player_links

# Utilities
with open('./scrape/error/wiki.json') as file:
    errors = json.load(file)


def prepend_link(link):
    return 'https://en.wikipedia.org' + link


def get_full_name(first, last):
    full_name = '%s %s' % (first, last)
    return full_name.strip()




