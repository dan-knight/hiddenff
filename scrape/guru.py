from config import current_season, current_week

from scrape.base import RequestsScraper, SeleniumScraper

from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By

import re


class PlayerListScraper(SeleniumScraper):
    def __init__(self, season, week):
        url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week=%s&year=%s&game=dk' % (week, season)
        super().__init__(url)
        self.data.update({'season': season})

    def interact_with_page(self):
        SeleniumScraper.wait_for_condition(cond.presence_of_element_located((By.XPATH, '//table//p/table')))

    def get_player_links(self):
        def get_table():
            p = self.soup.find(text=re.compile('DFS salaries')).parent
            return p.find('table').find('table')

        def get_rows():
            rows = []

            defense_title = get_table().find('b', text=re.compile('Defenses')).find_parent('tr')

            for sibling_row in defense_title.previous_siblings:
                rows.append(sibling_row)

            return rows

        links = set()

        for row in get_rows():
            try:
                a = row.find('a', {'target': '_blank'})
                links.add(a['href'])
            except TypeError:
                continue

        return links


class PlayerPageScraper(RequestsScraper):
    pass

    def scrape_basic_info(self):
        def get_name():
            first_text = ''
            last_text = ''

            container = self.soup.find('font', size=3)

            def add_error():
                self.add_error('name')

            try:
                full_name = container.find('b').text

                try:
                    def get_player_name():
                        split_text = full_name.split(', ')
                        return split_text[1], split_text[0]

                    first_text, last_text = get_player_name()
                except IndexError:
                    if 'Defense' in full_name:
                        def get_defense_name():
                            split_text = full_name.split(' ')
                            defense = split_text.pop()
                            location = ' '.join(split_text)
                            return location, defense

                        first_text, last_text = get_defense_name()
                    else:
                        add_error()
            except AttributeError:
                add_error()

            return first_text, last_text

        def get_position():
            text = ''
            label = self.soup.find(text='DraftKings position: ')

            try:
                text = label.next_sibling.text
            except AttributeError:
                self.add_error('position')

            return text

        first, last = get_name()

        self.data.update({
            'first': first,
            'last': last,
            'position': get_position()
        })


def get_player_links(season_weeks_pairs):
    links = set()

    for season, weeks in season_weeks_pairs.items():
        def scrape_season(week_list):
            try:
                for week in week_list:
                    links.update(PlayerListScraper(season, week).get_player_links())
            except TypeError:
                scrape_season([week_list])

        if int(season) >= 2014:
            scrape_season(weeks)

    return links


def scrape_player(link):
    player = PlayerPageScraper(link)
    player.scrape_basic_info()
    return player.data


# Utilities
def prepend_link(link):
    return 'http://rotoguru1.com/cgi-bin/' + link
